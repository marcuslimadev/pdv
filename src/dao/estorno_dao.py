"""
DAO para operações com Estornos no banco de dados.
"""

from typing import List, Optional
from datetime import date, datetime
from src.config.database import DatabaseConnection
from src.models.estorno import Estorno


class EstornoDAO:
    """Data Access Object para Estorno."""
    
    @staticmethod
    def criar(estorno: Estorno) -> Optional[int]:
        """
        Cria um novo registro de estorno.
        
        Args:
            estorno: Objeto Estorno
            
        Returns:
            ID do estorno criado ou None em caso de erro
        """
        sql = """
            INSERT INTO estornos (
                venda_id, usuario_id, motivo, valor_estornado, observacoes
            ) VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    estorno.venda_id,
                    estorno.usuario_id,
                    estorno.motivo,
                    estorno.valor_estornado,
                    estorno.observacoes
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar estorno: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(estorno_id: int) -> Optional[Estorno]:
        """
        Busca um estorno por ID.
        
        Args:
            estorno_id: ID do estorno
            
        Returns:
            Objeto Estorno ou None
        """
        sql = "SELECT * FROM estornos WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (estorno_id,))
                row = cursor.fetchone()
                
                if row:
                    return Estorno.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar estorno: {e}")
            return None
    
    @staticmethod
    def buscar_por_venda(venda_id: int) -> List[Estorno]:
        """
        Busca todos os estornos de uma venda.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            Lista de estornos
        """
        sql = """
            SELECT * FROM estornos 
            WHERE venda_id = %s
            ORDER BY data_estorno DESC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (venda_id,))
                rows = cursor.fetchall()
                
                return [Estorno.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar estornos da venda: {e}")
            return []
    
    @staticmethod
    def verificar_venda_estornada(venda_id: int) -> bool:
        """
        Verifica se uma venda já foi estornada.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            True se já foi estornada, False caso contrário
        """
        sql = "SELECT COUNT(*) as total FROM estornos WHERE venda_id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (venda_id,))
                row = cursor.fetchone()
                return row['total'] > 0 if row else False
        except Exception as e:
            print(f"Erro ao verificar estorno: {e}")
            return False
    
    @staticmethod
    def buscar_por_periodo(data_inicio: date, data_fim: date) -> List[Estorno]:
        """
        Busca estornos por período.
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            Lista de estornos
        """
        sql = """
            SELECT e.*, v.numero_venda, u.nome_completo as usuario_nome
            FROM estornos e
            JOIN vendas v ON e.venda_id = v.id
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE DATE(e.data_estorno) BETWEEN %s AND %s
            ORDER BY e.data_estorno DESC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (data_inicio, data_fim))
                rows = cursor.fetchall()
                
                return [Estorno.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar estornos por período: {e}")
            return []
    
    @staticmethod
    def obter_total_estornos_dia(data: date = None) -> dict:
        """
        Obtém o total de estornos do dia.
        
        Args:
            data: Data (usa hoje se None)
            
        Returns:
            dict com total e quantidade
        """
        if data is None:
            data = date.today()
        
        sql = """
            SELECT 
                SUM(valor_estornado) as total,
                COUNT(*) as quantidade
            FROM estornos
            WHERE DATE(data_estorno) = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (data,))
                row = cursor.fetchone()
                
                return {
                    'total': float(row['total']) if row and row['total'] else 0.0,
                    'quantidade': row['quantidade'] if row else 0
                }
        except Exception as e:
            print(f"Erro ao obter total de estornos: {e}")
            return {'total': 0.0, 'quantidade': 0}
