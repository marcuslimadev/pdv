"""
DAO para operações com Produtos no banco de dados.
"""

from typing import List, Optional
from src.config.database import DatabaseConnection
from src.models.produto import Produto


class ProdutoDAO:
    """Data Access Object para Produto."""
    
    @staticmethod
    def criar(produto: Produto) -> Optional[int]:
        """Cria um novo produto no banco de dados."""
        sql = """
            INSERT INTO produtos (
                codigo_barras, nome, descricao, categoria_id,
                preco_custo, preco_venda, estoque_atual, estoque_minimo,
                unidade_medida, ativo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    produto.codigo_barras,
                    produto.nome,
                    produto.descricao,
                    produto.categoria_id,
                    produto.preco_custo,
                    produto.preco_venda,
                    produto.estoque_atual,
                    produto.estoque_minimo,
                    produto.unidade_medida,
                    produto.ativo
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar produto: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Produto]:
        """Busca um produto por ID."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    return Produto.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            return None
    
    @staticmethod
    def buscar_por_codigo_barras(codigo_barras: str) -> Optional[Produto]:
        """Busca um produto por código de barras."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.codigo_barras = %s AND p.ativo = TRUE
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (codigo_barras,))
                row = cursor.fetchone()
                
                if row:
                    return Produto.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar produto por código de barras: {e}")
            return None
    
    @staticmethod
    def buscar_todos(apenas_ativos: bool = True) -> List[Produto]:
        """Busca todos os produtos."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """
        
        if apenas_ativos:
            sql += " WHERE p.ativo = TRUE"
        
        sql += " ORDER BY p.nome"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                return [Produto.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []
    
    @staticmethod
    def buscar_por_nome(nome: str) -> List[Produto]:
        """Busca produtos por nome (busca parcial)."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nome LIKE %s AND p.ativo = TRUE
            ORDER BY p.nome
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (f"%{nome}%",))
                rows = cursor.fetchall()
                
                return [Produto.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar produtos por nome: {e}")
            return []
    
    @staticmethod
    def buscar_por_categoria(categoria_id: int) -> List[Produto]:
        """Busca produtos por categoria."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.categoria_id = %s AND p.ativo = TRUE
            ORDER BY p.nome
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (categoria_id,))
                rows = cursor.fetchall()
                
                return [Produto.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar produtos por categoria: {e}")
            return []
    
    @staticmethod
    def buscar_estoque_baixo() -> List[Produto]:
        """Busca produtos com estoque abaixo do mínimo."""
        sql = """
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.estoque_atual <= p.estoque_minimo AND p.ativo = TRUE
            ORDER BY p.estoque_atual ASC
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                return [Produto.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar produtos com estoque baixo: {e}")
            return []
    
    @staticmethod
    def atualizar(produto: Produto) -> bool:
        """Atualiza um produto existente."""
        sql = """
            UPDATE produtos 
            SET codigo_barras = %s, nome = %s, descricao = %s,
                categoria_id = %s, preco_custo = %s, preco_venda = %s,
                estoque_atual = %s, estoque_minimo = %s,
                unidade_medida = %s, ativo = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    produto.codigo_barras,
                    produto.nome,
                    produto.descricao,
                    produto.categoria_id,
                    produto.preco_custo,
                    produto.preco_venda,
                    produto.estoque_atual,
                    produto.estoque_minimo,
                    produto.unidade_medida,
                    produto.ativo,
                    produto.id
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            return False
    
    @staticmethod
    def atualizar_estoque(produto_id: int, quantidade: int) -> bool:
        """Atualiza o estoque de um produto."""
        sql = "UPDATE produtos SET estoque_atual = %s WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (quantidade, produto_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar estoque: {e}")
            return False
    
    @staticmethod
    def excluir(id: int) -> bool:
        """Exclui logicamente um produto (marca como inativo)."""
        sql = "UPDATE produtos SET ativo = FALSE WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            return False
