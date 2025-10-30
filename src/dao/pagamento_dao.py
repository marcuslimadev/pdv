"""
DAO para operações com Pagamentos no banco de dados.
"""

from typing import List, Optional
from datetime import date
from src.config.database import DatabaseConnection
from src.models.pagamento import Pagamento


class PagamentoDAO:
    """Data Access Object para Pagamento."""
    
    @staticmethod
    def criar(pagamento: Pagamento) -> Optional[int]:
        """Cria um novo pagamento."""
        sql = """
            INSERT INTO pagamentos (
                venda_id, forma_pagamento, valor, numero_parcelas,
                status, nsu, codigo_autorizacao, dados_pix, valor_pago, troco
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    pagamento.venda_id,
                    pagamento.forma_pagamento,
                    pagamento.valor,
                    pagamento.numero_parcelas,
                    pagamento.status,
                    pagamento.nsu,
                    pagamento.codigo_autorizacao,
                    pagamento.dados_pix,
                    pagamento.valor_pago if pagamento.valor_pago else pagamento.valor,
                    pagamento.troco if pagamento.troco else 0
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar pagamento: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Pagamento]:
        """Busca um pagamento por ID."""
        sql = "SELECT * FROM pagamentos WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    return Pagamento.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar pagamento: {e}")
            return None
    
    @staticmethod
    def buscar_por_venda(venda_id: int) -> List[Pagamento]:
        """Busca todos os pagamentos de uma venda."""
        sql = """
            SELECT * FROM pagamentos 
            WHERE venda_id = %s
            ORDER BY data_hora
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (venda_id,))
                rows = cursor.fetchall()
                
                return [Pagamento.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar pagamentos da venda: {e}")
            return []
    
    @staticmethod
    def buscar_por_periodo(data_inicio: date, data_fim: date, forma_pagamento: str = None) -> List[Pagamento]:
        """Busca pagamentos por período."""
        sql = """
            SELECT p.*, v.numero_venda
            FROM pagamentos p
            JOIN vendas v ON p.venda_id = v.id
            WHERE DATE(p.data_hora) BETWEEN %s AND %s
        """
        
        params = [data_inicio, data_fim]
        
        if forma_pagamento:
            sql += " AND p.forma_pagamento = %s"
            params.append(forma_pagamento)
        
        sql += " ORDER BY p.data_hora DESC"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, tuple(params))
                rows = cursor.fetchall()
                
                return [Pagamento.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar pagamentos por período: {e}")
            return []
    
    @staticmethod
    def atualizar_status(pagamento_id: int, status: str, nsu: str = None, codigo_autorizacao: str = None) -> bool:
        """Atualiza o status de um pagamento."""
        sql = """
            UPDATE pagamentos 
            SET status = %s, nsu = %s, codigo_autorizacao = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (status, nsu, codigo_autorizacao, pagamento_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar status do pagamento: {e}")
            return False
    
    @staticmethod
    def obter_total_por_forma_pagamento(data: date = None) -> dict:
        """Obtém o total por forma de pagamento do dia."""
        if data is None:
            data = date.today()
        
        sql = """
            SELECT 
                forma_pagamento,
                SUM(valor) as total,
                COUNT(*) as quantidade
            FROM pagamentos p
            JOIN vendas v ON p.venda_id = v.id
            WHERE DATE(p.data_hora) = %s 
            AND p.status = 'aprovado'
            AND v.status = 'finalizada'
            GROUP BY forma_pagamento
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (data,))
                rows = cursor.fetchall()
                
                resultado = {}
                for row in rows:
                    resultado[row['forma_pagamento']] = {
                        'total': float(row['total']),
                        'quantidade': row['quantidade']
                    }
                
                return resultado
        except Exception as e:
            print(f"Erro ao obter total por forma de pagamento: {e}")
            return {}
