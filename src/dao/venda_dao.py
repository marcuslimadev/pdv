"""
DAO para operações com Vendas no banco de dados.
"""

from typing import List, Optional
from datetime import datetime, date
from src.config.database import DatabaseConnection
from src.models.venda import Venda, ItemVenda


class VendaDAO:
    """Data Access Object para Venda."""
    
    @staticmethod
    def criar(venda: Venda) -> Optional[int]:
        """Cria uma nova venda no banco de dados."""
        sql = """
            INSERT INTO vendas (
                numero_venda, usuario_id, caixa_id, subtotal,
                desconto, total, status, observacoes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    venda.numero_venda,
                    venda.usuario_id,
                    venda.caixa_id,
                    venda.subtotal,
                    venda.desconto,
                    venda.total,
                    venda.status,
                    venda.observacoes
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar venda: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Venda]:
        """Busca uma venda por ID."""
        sql = """
            SELECT v.*, u.nome_completo as usuario_nome
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    venda = Venda.from_dict(row)
                    venda.itens = ItemVendaDAO.buscar_por_venda(venda.id)
                    return venda
                return None
        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None
    
    @staticmethod
    def buscar_por_numero(numero_venda: str) -> Optional[Venda]:
        """Busca uma venda por número."""
        sql = """
            SELECT v.*, u.nome_completo as usuario_nome
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.numero_venda = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (numero_venda,))
                row = cursor.fetchone()
                
                if row:
                    venda = Venda.from_dict(row)
                    venda.itens = ItemVendaDAO.buscar_por_venda(venda.id)
                    return venda
                return None
        except Exception as e:
            print(f"Erro ao buscar venda por número: {e}")
            return None
    
    @staticmethod
    def buscar_por_periodo(data_inicio: date, data_fim: date, status: str = None) -> List[Venda]:
        """Busca vendas por período."""
        sql = """
            SELECT v.*, u.nome_completo as usuario_nome
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE DATE(v.data_hora) BETWEEN %s AND %s
        """
        
        params = [data_inicio, data_fim]
        
        if status:
            sql += " AND v.status = %s"
            params.append(status)
        
        sql += " ORDER BY v.data_hora DESC"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, tuple(params))
                rows = cursor.fetchall()
                
                return [Venda.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar vendas por período: {e}")
            return []
    
    @staticmethod
    def buscar_por_caixa(caixa_id: int) -> List[Venda]:
        """Busca vendas por caixa."""
        sql = """
            SELECT v.*, u.nome_completo as usuario_nome
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.caixa_id = %s
            ORDER BY v.data_hora DESC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (caixa_id,))
                rows = cursor.fetchall()
                
                return [Venda.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar vendas por caixa: {e}")
            return []
    
    @staticmethod
    def atualizar(venda: Venda) -> bool:
        """Atualiza uma venda existente."""
        sql = """
            UPDATE vendas 
            SET subtotal = %s, desconto = %s, total = %s,
                status = %s, observacoes = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    venda.subtotal,
                    venda.desconto,
                    venda.total,
                    venda.status,
                    venda.observacoes,
                    venda.id
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar venda: {e}")
            return False
    
    @staticmethod
    def gerar_numero_venda() -> str:
        """Gera um número único para a venda."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"V{timestamp}"
    
    @staticmethod
    def obter_total_vendas_dia(data: date = None) -> float:
        """Obtém o total de vendas do dia."""
        if data is None:
            data = date.today()
        
        sql = """
            SELECT COALESCE(SUM(total), 0) as total
            FROM vendas
            WHERE DATE(data_hora) = %s AND status = 'finalizada'
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (data,))
                row = cursor.fetchone()
                return float(row['total']) if row else 0.0
        except Exception as e:
            print(f"Erro ao obter total de vendas do dia: {e}")
            return 0.0


class ItemVendaDAO:
    """Data Access Object para ItemVenda."""
    
    @staticmethod
    def criar(item: ItemVenda) -> Optional[int]:
        """Cria um novo item de venda."""
        sql = """
            INSERT INTO itens_venda (
                venda_id, produto_id, quantidade, preco_unitario,
                desconto, subtotal
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    item.venda_id,
                    item.produto_id,
                    item.quantidade,
                    item.preco_unitario,
                    item.desconto,
                    item.subtotal
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar item de venda: {e}")
            return None
    
    @staticmethod
    def buscar_por_venda(venda_id: int) -> List[ItemVenda]:
        """Busca todos os itens de uma venda."""
        sql = """
            SELECT iv.*, p.nome as produto_nome, p.codigo_barras as produto_codigo_barras
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = %s
            ORDER BY iv.id
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (venda_id,))
                rows = cursor.fetchall()
                
                return [ItemVenda.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar itens da venda: {e}")
            return []
    
    @staticmethod
    def excluir_por_venda(venda_id: int) -> bool:
        """Exclui todos os itens de uma venda."""
        sql = "DELETE FROM itens_venda WHERE venda_id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (venda_id,))
                return True
        except Exception as e:
            print(f"Erro ao excluir itens da venda: {e}")
            return False
