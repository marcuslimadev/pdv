"""
Modelo de dados para Caixa.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class Caixa:
    """Representa um caixa operacional."""
    
    STATUS_ABERTO = 'aberto'
    STATUS_FECHADO = 'fechado'
    
    def __init__(
        self,
        id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        data_abertura: Optional[datetime] = None,
        data_fechamento: Optional[datetime] = None,
        valor_abertura: Decimal = Decimal('0.00'),
        valor_fechamento: Optional[Decimal] = None,
        status: str = STATUS_ABERTO,
        observacoes: str = ""
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.data_abertura = data_abertura or datetime.now()
        self.data_fechamento = data_fechamento
        self.valor_abertura = valor_abertura
        self.valor_fechamento = valor_fechamento
        self.status = status
        self.observacoes = observacoes
        
        # Campos auxiliares
        self.usuario_nome = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'data_abertura': self.data_abertura,
            'data_fechamento': self.data_fechamento,
            'valor_abertura': float(self.valor_abertura) if self.valor_abertura else 0.00,
            'valor_fechamento': float(self.valor_fechamento) if self.valor_fechamento else None,
            'status': self.status,
            'observacoes': self.observacoes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Caixa':
        """Cria um objeto Caixa a partir de um dicionário."""
        caixa = cls(
            id=data.get('id'),
            usuario_id=data.get('usuario_id'),
            data_abertura=data.get('data_abertura'),
            data_fechamento=data.get('data_fechamento'),
            valor_abertura=Decimal(str(data.get('valor_abertura', 0))),
            valor_fechamento=Decimal(str(data['valor_fechamento'])) if data.get('valor_fechamento') else None,
            status=data.get('status', cls.STATUS_ABERTO),
            observacoes=data.get('observacoes', '')
        )
        
        if 'usuario_nome' in data:
            caixa.usuario_nome = data['usuario_nome']
        
        return caixa
    
    def fechar(self, valor_fechamento: Decimal):
        """Fecha o caixa com o valor final."""
        self.status = self.STATUS_FECHADO
        self.data_fechamento = datetime.now()
        self.valor_fechamento = valor_fechamento
    
    def calcular_diferenca(self) -> Optional[Decimal]:
        """Calcula a diferença entre valor esperado e contado."""
        if self.valor_fechamento is not None:
            return self.valor_fechamento - self.valor_abertura
        return None
    
    def __repr__(self) -> str:
        return f"Caixa(id={self.id}, usuario_id={self.usuario_id}, status='{self.status}')"
