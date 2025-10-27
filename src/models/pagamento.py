"""
Modelo de dados para Pagamento.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class Pagamento:
    """Representa um pagamento de uma venda."""
    
    FORMA_DINHEIRO = 'dinheiro'
    FORMA_DEBITO = 'debito'
    FORMA_CREDITO = 'credito'
    FORMA_PIX = 'pix'
    
    STATUS_PENDENTE = 'pendente'
    STATUS_APROVADO = 'aprovado'
    STATUS_RECUSADO = 'recusado'
    
    def __init__(
        self,
        id: Optional[int] = None,
        venda_id: Optional[int] = None,
        forma_pagamento: str = FORMA_DINHEIRO,
        valor: Decimal = Decimal('0.00'),
        numero_parcelas: int = 1,
        status: str = STATUS_PENDENTE,
        nsu: str = "",
        codigo_autorizacao: str = "",
        dados_pix: str = "",
        data_hora: Optional[datetime] = None
    ):
        self.id = id
        self.venda_id = venda_id
        self.forma_pagamento = forma_pagamento
        self.valor = valor
        self.numero_parcelas = numero_parcelas
        self.status = status
        self.nsu = nsu
        self.codigo_autorizacao = codigo_autorizacao
        self.dados_pix = dados_pix
        self.data_hora = data_hora or datetime.now()
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'venda_id': self.venda_id,
            'forma_pagamento': self.forma_pagamento,
            'valor': float(self.valor) if self.valor else 0.00,
            'numero_parcelas': self.numero_parcelas,
            'status': self.status,
            'nsu': self.nsu,
            'codigo_autorizacao': self.codigo_autorizacao,
            'dados_pix': self.dados_pix,
            'data_hora': self.data_hora
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Pagamento':
        """Cria um objeto Pagamento a partir de um dicionário."""
        return cls(
            id=data.get('id'),
            venda_id=data.get('venda_id'),
            forma_pagamento=data.get('forma_pagamento', cls.FORMA_DINHEIRO),
            valor=Decimal(str(data.get('valor', 0))),
            numero_parcelas=data.get('numero_parcelas', 1),
            status=data.get('status', cls.STATUS_PENDENTE),
            nsu=data.get('nsu', ''),
            codigo_autorizacao=data.get('codigo_autorizacao', ''),
            dados_pix=data.get('dados_pix', ''),
            data_hora=data.get('data_hora')
        )
    
    def aprovar(self):
        """Marca o pagamento como aprovado."""
        self.status = self.STATUS_APROVADO
    
    def recusar(self):
        """Marca o pagamento como recusado."""
        self.status = self.STATUS_RECUSADO
    
    def get_forma_pagamento_descricao(self) -> str:
        """Retorna a descrição da forma de pagamento."""
        formas = {
            self.FORMA_DINHEIRO: 'Dinheiro',
            self.FORMA_DEBITO: 'Débito',
            self.FORMA_CREDITO: 'Crédito',
            self.FORMA_PIX: 'PIX'
        }
        return formas.get(self.forma_pagamento, 'Desconhecido')
    
    def __repr__(self) -> str:
        return f"Pagamento(id={self.id}, forma='{self.forma_pagamento}', valor=R${self.valor})"
