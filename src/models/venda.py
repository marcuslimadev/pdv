"""
Modelo de dados para Venda.
"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class Venda:
    """Representa uma venda no sistema."""
    
    STATUS_ABERTA = 'aberta'
    STATUS_FINALIZADA = 'finalizada'
    STATUS_CANCELADA = 'cancelada'
    
    def __init__(
        self,
        id: Optional[int] = None,
        numero_venda: str = "",
        usuario_id: Optional[int] = None,
        caixa_id: Optional[int] = None,
        data_hora: Optional[datetime] = None,
        subtotal: Decimal = Decimal('0.00'),
        desconto: Decimal = Decimal('0.00'),
        total: Decimal = Decimal('0.00'),
        status: str = STATUS_ABERTA,
        observacoes: str = ""
    ):
        self.id = id
        self.numero_venda = numero_venda
        self.usuario_id = usuario_id
        self.caixa_id = caixa_id
        self.data_hora = data_hora or datetime.now()
        self.subtotal = subtotal
        self.desconto = desconto
        self.total = total
        self.status = status
        self.observacoes = observacoes
        
        # Campos auxiliares (não persistidos)
        self.itens: List['ItemVenda'] = []
        self.usuario_nome = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'numero_venda': self.numero_venda,
            'usuario_id': self.usuario_id,
            'caixa_id': self.caixa_id,
            'data_hora': self.data_hora,
            'subtotal': float(self.subtotal) if self.subtotal else 0.00,
            'desconto': float(self.desconto) if self.desconto else 0.00,
            'total': float(self.total) if self.total else 0.00,
            'status': self.status,
            'observacoes': self.observacoes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Venda':
        """Cria um objeto Venda a partir de um dicionário."""
        venda = cls(
            id=data.get('id'),
            numero_venda=data.get('numero_venda', ''),
            usuario_id=data.get('usuario_id'),
            caixa_id=data.get('caixa_id'),
            data_hora=data.get('data_hora'),
            subtotal=Decimal(str(data.get('subtotal', 0))),
            desconto=Decimal(str(data.get('desconto', 0))),
            total=Decimal(str(data.get('total', 0))),
            status=data.get('status', cls.STATUS_ABERTA),
            observacoes=data.get('observacoes', '')
        )
        
        if 'usuario_nome' in data:
            venda.usuario_nome = data['usuario_nome']
        
        return venda
    
    def adicionar_item(self, item: 'ItemVenda'):
        """Adiciona um item à venda e recalcula totais."""
        self.itens.append(item)
        self.recalcular_totais()
    
    def remover_item(self, index: int):
        """Remove um item da venda e recalcula totais."""
        if 0 <= index < len(self.itens):
            self.itens.pop(index)
            self.recalcular_totais()
    
    def recalcular_totais(self):
        """Recalcula subtotal e total da venda."""
        self.subtotal = sum(item.subtotal for item in self.itens)
        self.total = self.subtotal - self.desconto
    
    def aplicar_desconto(self, desconto: Decimal):
        """Aplica desconto e recalcula total."""
        self.desconto = desconto
        self.total = self.subtotal - self.desconto
    
    def finalizar(self):
        """Marca a venda como finalizada."""
        self.status = self.STATUS_FINALIZADA
    
    def cancelar(self):
        """Marca a venda como cancelada."""
        self.status = self.STATUS_CANCELADA
    
    def __repr__(self) -> str:
        return f"Venda(id={self.id}, numero='{self.numero_venda}', total=R${self.total})"


class ItemVenda:
    """Representa um item de uma venda."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        venda_id: Optional[int] = None,
        produto_id: Optional[int] = None,
        quantidade: Decimal = Decimal('1.000'),
        preco_unitario: Decimal = Decimal('0.00'),
        desconto: Decimal = Decimal('0.00'),
        subtotal: Decimal = Decimal('0.00')
    ):
        self.id = id
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.desconto = desconto
        self.subtotal = subtotal
        
        # Campos auxiliares (não persistidos)
        self.produto_nome = None
        self.produto_codigo_barras = None
        
        # Calcula subtotal se não foi informado
        if subtotal == Decimal('0.00'):
            self.calcular_subtotal()
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'venda_id': self.venda_id,
            'produto_id': self.produto_id,
            'quantidade': float(self.quantidade) if self.quantidade else 0.000,
            'preco_unitario': float(self.preco_unitario) if self.preco_unitario else 0.00,
            'desconto': float(self.desconto) if self.desconto else 0.00,
            'subtotal': float(self.subtotal) if self.subtotal else 0.00
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ItemVenda':
        """Cria um objeto ItemVenda a partir de um dicionário."""
        item = cls(
            id=data.get('id'),
            venda_id=data.get('venda_id'),
            produto_id=data.get('produto_id'),
            quantidade=Decimal(str(data.get('quantidade', 1))),
            preco_unitario=Decimal(str(data.get('preco_unitario', 0))),
            desconto=Decimal(str(data.get('desconto', 0))),
            subtotal=Decimal(str(data.get('subtotal', 0)))
        )
        
        if 'produto_nome' in data:
            item.produto_nome = data['produto_nome']
        if 'produto_codigo_barras' in data:
            item.produto_codigo_barras = data['produto_codigo_barras']
        
        return item
    
    def calcular_subtotal(self):
        """Calcula o subtotal do item."""
        self.subtotal = (self.quantidade * self.preco_unitario) - self.desconto
    
    def __repr__(self) -> str:
        return f"ItemVenda(id={self.id}, produto_id={self.produto_id}, qtd={self.quantidade})"
