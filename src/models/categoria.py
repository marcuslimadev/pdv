"""
Modelo de dados para Categoria.
"""

from datetime import datetime
from typing import Optional


class Categoria:
    """Representa uma categoria de produtos."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        nome: str = "",
        descricao: str = "",
        ativo: bool = True,
        data_cadastro: Optional[datetime] = None
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo
        self.data_cadastro = data_cadastro or datetime.now()
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Categoria':
        """Cria um objeto Categoria a partir de um dicionário."""
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            descricao=data.get('descricao', ''),
            ativo=data.get('ativo', True),
            data_cadastro=data.get('data_cadastro')
        )
    
    def __repr__(self) -> str:
        return f"Categoria(id={self.id}, nome='{self.nome}')"
