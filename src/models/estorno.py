"""
Model para Estorno de Vendas.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Estorno:
    """Representa um estorno de venda."""
    
    venda_id: int
    usuario_id: int
    motivo: str
    valor_estornado: Decimal
    observacoes: Optional[str] = None
    id: Optional[int] = None
    data_estorno: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            'id': self.id,
            'venda_id': self.venda_id,
            'usuario_id': self.usuario_id,
            'data_estorno': self.data_estorno.isoformat() if self.data_estorno else None,
            'motivo': self.motivo,
            'valor_estornado': float(self.valor_estornado),
            'observacoes': self.observacoes
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Estorno':
        """Cria instância a partir de dicionário."""
        return Estorno(
            id=data.get('id'),
            venda_id=data['venda_id'],
            usuario_id=data['usuario_id'],
            data_estorno=data.get('data_estorno'),
            motivo=data['motivo'],
            valor_estornado=Decimal(str(data['valor_estornado'])),
            observacoes=data.get('observacoes')
        )
