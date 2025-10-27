"""
DAO para operações com Categorias no banco de dados.
"""

from typing import List, Optional
from src.config.database import DatabaseConnection
from src.models.categoria import Categoria


class CategoriaDAO:
    """Data Access Object para Categoria."""
    
    @staticmethod
    def criar(categoria: Categoria) -> Optional[int]:
        """
        Cria uma nova categoria no banco de dados.
        
        Args:
            categoria: Objeto Categoria a ser criado
            
        Returns:
            ID da categoria criada ou None em caso de erro
        """
        sql = """
            INSERT INTO categorias (nome, descricao, ativo)
            VALUES (%s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    categoria.nome,
                    categoria.descricao,
                    categoria.ativo
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar categoria: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Categoria]:
        """Busca uma categoria por ID."""
        sql = "SELECT * FROM categorias WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    return Categoria.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar categoria: {e}")
            return None
    
    @staticmethod
    def buscar_todas(apenas_ativas: bool = True) -> List[Categoria]:
        """
        Busca todas as categorias.
        
        Args:
            apenas_ativas: Se True, retorna apenas categorias ativas
            
        Returns:
            Lista de categorias
        """
        sql = "SELECT * FROM categorias"
        
        if apenas_ativas:
            sql += " WHERE ativo = TRUE"
        
        sql += " ORDER BY nome"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                return [Categoria.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []
    
    @staticmethod
    def atualizar(categoria: Categoria) -> bool:
        """Atualiza uma categoria existente."""
        sql = """
            UPDATE categorias 
            SET nome = %s, descricao = %s, ativo = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    categoria.nome,
                    categoria.descricao,
                    categoria.ativo,
                    categoria.id
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")
            return False
    
    @staticmethod
    def excluir(id: int) -> bool:
        """
        Exclui logicamente uma categoria (marca como inativa).
        
        Args:
            id: ID da categoria
            
        Returns:
            True se excluída com sucesso
        """
        sql = "UPDATE categorias SET ativo = FALSE WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir categoria: {e}")
            return False
    
    @staticmethod
    def buscar_por_nome(nome: str) -> List[Categoria]:
        """Busca categorias por nome (busca parcial)."""
        sql = """
            SELECT * FROM categorias 
            WHERE nome LIKE %s AND ativo = TRUE
            ORDER BY nome
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (f"%{nome}%",))
                rows = cursor.fetchall()
                
                return [Categoria.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar categorias por nome: {e}")
            return []
