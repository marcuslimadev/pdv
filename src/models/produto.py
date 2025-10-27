"""
Modelo de dados para Produto.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class Produto:
    """Representa um produto do sistema."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        codigo_barras: str = "",
        nome: str = "",
        descricao: str = "",
        categoria_id: Optional[int] = None,
        preco_custo: Decimal = Decimal('0.00'),
        preco_venda: Decimal = Decimal('0.00'),
        estoque_atual: int = 0,
        estoque_minimo: int = 0,
        unidade_medida: str = "UN",
        ativo: bool = True,
        data_cadastro: Optional[datetime] = None,
        data_atualizacao: Optional[datetime] = None
    ):
        self.id = id
        self.codigo_barras = codigo_barras
        self.nome = nome
        self.descricao = descricao
        self.categoria_id = categoria_id
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.estoque_atual = estoque_atual
        self.estoque_minimo = estoque_minimo
        self.unidade_medida = unidade_medida
        self.ativo = ativo
        self.data_cadastro = data_cadastro or datetime.now()
        self.data_atualizacao = data_atualizacao or datetime.now()
        
        # Campos auxiliares (não persistidos)
        self.categoria_nome = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'codigo_barras': self.codigo_barras,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria_id': self.categoria_id,
            'preco_custo': float(self.preco_custo) if self.preco_custo else 0.00,
            'preco_venda': float(self.preco_venda) if self.preco_venda else 0.00,
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'unidade_medida': self.unidade_medida,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Produto':
        """Cria um objeto Produto a partir de um dicionário."""
        produto = cls(
            id=data.get('id'),
            codigo_barras=data.get('codigo_barras', ''),
            nome=data.get('nome', ''),
            descricao=data.get('descricao', ''),
            categoria_id=data.get('categoria_id'),
            preco_custo=Decimal(str(data.get('preco_custo', 0))),
            preco_venda=Decimal(str(data.get('preco_venda', 0))),
            estoque_atual=data.get('estoque_atual', 0),
            estoque_minimo=data.get('estoque_minimo', 0),
            unidade_medida=data.get('unidade_medida', 'UN'),
            ativo=data.get('ativo', True),
            data_cadastro=data.get('data_cadastro'),
            data_atualizacao=data.get('data_atualizacao')
        )
        
        # Campos auxiliares
        if 'categoria_nome' in data:
            produto.categoria_nome = data['categoria_nome']
        
        return produto
    
    def estoque_baixo(self) -> bool:
        """Verifica se o estoque está abaixo do mínimo."""
        return self.estoque_atual <= self.estoque_minimo
    
    def margem_lucro(self) -> Decimal:
        """Calcula a margem de lucro percentual."""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return Decimal('0')
    
    def __repr__(self) -> str:
        return f"Produto(id={self.id}, nome='{self.nome}', preco=R${self.preco_venda})"
