"""
Modelo de dados para Usuário.
"""

from datetime import datetime
from typing import Optional
import bcrypt


class Usuario:
    """Representa um usuário do sistema."""
    
    TIPO_ADMIN = 'admin'
    TIPO_OPERADOR = 'operador'
    
    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        senha_hash: str = "",
        nome_completo: str = "",
        tipo: str = TIPO_OPERADOR,
        ativo: bool = True,
        data_cadastro: Optional[datetime] = None,
        ultimo_acesso: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.senha_hash = senha_hash
        self.nome_completo = nome_completo
        self.tipo = tipo
        self.ativo = ativo
        self.data_cadastro = data_cadastro or datetime.now()
        self.ultimo_acesso = ultimo_acesso
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'username': self.username,
            'senha_hash': self.senha_hash,
            'nome_completo': self.nome_completo,
            'tipo': self.tipo,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro,
            'ultimo_acesso': self.ultimo_acesso
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        """Cria um objeto Usuario a partir de um dicionário."""
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            senha_hash=data.get('senha_hash', ''),
            nome_completo=data.get('nome_completo', ''),
            tipo=data.get('tipo', cls.TIPO_OPERADOR),
            ativo=data.get('ativo', True),
            data_cadastro=data.get('data_cadastro'),
            ultimo_acesso=data.get('ultimo_acesso')
        )
    
    @staticmethod
    def hash_senha(senha: str) -> str:
        """Gera o hash bcrypt da senha."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha está correta."""
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
    def is_admin(self) -> bool:
        """Verifica se o usuário é administrador."""
        return self.tipo == self.TIPO_ADMIN
    
    def is_operador(self) -> bool:
        """Verifica se o usuário é operador."""
        return self.tipo == self.TIPO_OPERADOR
    
    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, username='{self.username}', tipo='{self.tipo}')"
