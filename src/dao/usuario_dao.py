"""
DAO para operações com Usuários no banco de dados.
"""

from typing import List, Optional
from datetime import datetime
from src.config.database import DatabaseConnection
from src.models.usuario import Usuario


class UsuarioDAO:
    """Data Access Object para Usuario."""
    
    @staticmethod
    def criar(usuario: Usuario) -> Optional[int]:
        """Cria um novo usuário no banco de dados."""
        sql = """
            INSERT INTO usuarios (
                username, senha_hash, nome_completo, tipo, ativo
            ) VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    usuario.username,
                    usuario.senha_hash,
                    usuario.nome_completo,
                    usuario.tipo,
                    usuario.ativo
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id: int) -> Optional[Usuario]:
        """Busca um usuário por ID."""
        sql = "SELECT * FROM usuarios WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row:
                    return Usuario.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
    
    @staticmethod
    def buscar_por_username(username: str) -> Optional[Usuario]:
        """Busca um usuário por username."""
        sql = "SELECT * FROM usuarios WHERE username = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (username,))
                row = cursor.fetchone()
                
                if row:
                    return Usuario.from_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário por username: {e}")
            return None
    
    @staticmethod
    def buscar_todos(apenas_ativos: bool = True) -> List[Usuario]:
        """Busca todos os usuários."""
        sql = "SELECT * FROM usuarios"
        
        if apenas_ativos:
            sql += " WHERE ativo = TRUE"
        
        sql += " ORDER BY nome_completo"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                return [Usuario.from_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar usuários: {e}")
            return []
    
    @staticmethod
    def atualizar(usuario: Usuario) -> bool:
        """Atualiza um usuário existente."""
        sql = """
            UPDATE usuarios 
            SET username = %s, senha_hash = %s, nome_completo = %s,
                tipo = %s, ativo = %s
            WHERE id = %s
        """
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (
                    usuario.username,
                    usuario.senha_hash,
                    usuario.nome_completo,
                    usuario.tipo,
                    usuario.ativo,
                    usuario.id
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False
    
    @staticmethod
    def atualizar_ultimo_acesso(usuario_id: int) -> bool:
        """Atualiza a data do último acesso do usuário."""
        sql = "UPDATE usuarios SET ultimo_acesso = %s WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (datetime.now(), usuario_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar último acesso: {e}")
            return False
    
    @staticmethod
    def excluir(id: int) -> bool:
        """Exclui logicamente um usuário (marca como inativo)."""
        sql = "UPDATE usuarios SET ativo = FALSE WHERE id = %s"
        
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(sql, (id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            return False
    
    @staticmethod
    def autenticar(username: str, senha: str) -> Optional[Usuario]:
        """
        Autentica um usuário.
        
        Args:
            username: Nome de usuário
            senha: Senha em texto plano
            
        Returns:
            Objeto Usuario se autenticado, None caso contrário
        """
        usuario = UsuarioDAO.buscar_por_username(username)
        
        if usuario and usuario.ativo and usuario.verificar_senha(senha):
            UsuarioDAO.atualizar_ultimo_acesso(usuario.id)
            return usuario
        
        return None
