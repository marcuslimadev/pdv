"""
DAO para operações com Caixa no banco de dados.
"""

from typing import List, Optional
from datetime import date
from src.config.database import DatabaseConnection
from src.models.caixa import Caixa


class CaixaDAO:
    """Data Access Object para Caixa."""
    
    @staticmethod
    def criar(caixa: Caixa) -> Optional[int]:
        """Cria um novo caixa (abertura)."""
        sql = """
            INSERT INTO caixa (
                usuario_id, valor_abertura, status, observacoes
            ) VALUES (%s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    caixa.usuario_id,
                    caixa.valor_abertura,
                    caixa.status,
                    caixa.observacoes
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao abrir caixa: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Caixa]:
        """Busca um caixa por ID."""
        sql = """
            SELECT c.*, u.nome_completo as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    return Caixa.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar caixa: {e}")
            return None
    
    @staticmethod
    def buscar_caixa_aberto(usuario_id: int = None) -> Optional[Caixa]:
        """
        Busca o caixa aberto.
        
        Args:
            usuario_id: Se informado, busca o caixa aberto do usuário específico
            
        Returns:
            Caixa aberto ou None
        """
        sql = """
            SELECT c.*, u.nome_completo as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.status = 'aberto'
        """
        
        params = []
        if usuario_id:
            sql += " AND c.usuario_id = %s"
            params.append(usuario_id)
        
        sql += " ORDER BY c.data_abertura DESC LIMIT 1"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, tuple(params))
                row = cursor.fetchone()
                
                if row:
                    return Caixa.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar caixa aberto: {e}")
            return None
    
    @staticmethod
    def buscar_por_usuario(usuario_id: int) -> List[Caixa]:
        """Busca todos os caixas de um usuário."""
        sql = """
            SELECT c.*, u.nome_completo as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.usuario_id = %s
            ORDER BY c.data_abertura DESC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (usuario_id,))
                rows = cursor.fetchall()
                
                return [Caixa.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar caixas por usuário: {e}")
            return []
    
    @staticmethod
    def buscar_por_periodo(data_inicio: date, data_fim: date) -> List[Caixa]:
        """Busca caixas por período."""
        sql = """
            SELECT c.*, u.nome_completo as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE DATE(c.data_abertura) BETWEEN %s AND %s
            ORDER BY c.data_abertura DESC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (data_inicio, data_fim))
                rows = cursor.fetchall()
                
                return [Caixa.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar caixas por período: {e}")
            return []
    
    @staticmethod
    def fechar_caixa(caixa_id: int, valor_fechamento: float, observacoes: str = "") -> bool:
        """Fecha um caixa."""
        sql = """
            UPDATE caixa 
            SET status = 'fechado',
                data_fechamento = NOW(),
                valor_fechamento = %s,
                observacoes = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (valor_fechamento, observacoes, caixa_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao fechar caixa: {e}")
            return False
    
    @staticmethod
    def tem_caixa_aberto() -> bool:
        """Verifica se existe algum caixa aberto."""
        caixa = CaixaDAO.buscar_caixa_aberto()
        return caixa is not None
