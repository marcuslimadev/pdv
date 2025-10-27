"""
Serviço de integração com Pinpad (POS).
Este é um mock para desenvolvimento. Para produção, integrar com SDK do fabricante.
"""

from decimal import Decimal
from typing import Optional
import random
import time
from datetime import datetime


class PinpadResponse:
    """Resposta de uma transação no pinpad."""
    
    def __init__(
        self,
        sucesso: bool,
        mensagem: str,
        nsu: str = "",
        codigo_autorizacao: str = "",
        bandeira: str = "",
        ultimos_digitos: str = ""
    ):
        self.sucesso = sucesso
        self.mensagem = mensagem
        self.nsu = nsu
        self.codigo_autorizacao = codigo_autorizacao
        self.bandeira = bandeira
        self.ultimos_digitos = ultimos_digitos


class PinpadService:
    """
    Serviço de integração com Pinpad.
    
    ATENÇÃO: Esta é uma implementação MOCK para desenvolvimento/testes.
    Para produção, substituir pela integração real com o SDK do fabricante do pinpad
    (Gertec, Ingenico, PAX, etc.) e credenciais da adquirente (Stone, Cielo, Rede, etc.).
    """
    
    def __init__(self):
        self.conectado = False
        self.porta = "COM1"  # Porta padrão
        self.timeout = 60  # Timeout em segundos
    
    def conectar(self, porta: str = "COM1") -> tuple[bool, str]:
        """
        Conecta ao pinpad.
        
        Args:
            porta: Porta de comunicação (COM1, COM2, etc.)
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        self.porta = porta
        
        # Simulação de conexão
        time.sleep(0.5)
        self.conectado = True
        
        return True, f"Pinpad conectado na porta {porta}"
    
    def desconectar(self):
        """Desconecta do pinpad."""
        self.conectado = False
    
    def venda_debito(self, valor: Decimal) -> PinpadResponse:
        """
        Realiza uma venda no débito.
        
        Args:
            valor: Valor da transação
            
        Returns:
            PinpadResponse com resultado da transação
        """
        if not self.conectado:
            return PinpadResponse(
                sucesso=False,
                mensagem="Pinpad não conectado"
            )
        
        # Simulação de processamento
        print(f"[PINPAD] Processando venda débito: R$ {valor}")
        time.sleep(2)  # Simula tempo de processamento
        
        # Simula aprovação (90% de chance)
        if random.random() < 0.9:
            nsu = self._gerar_nsu()
            codigo_aut = self._gerar_codigo_autorizacao()
            
            return PinpadResponse(
                sucesso=True,
                mensagem="Transação aprovada",
                nsu=nsu,
                codigo_autorizacao=codigo_aut,
                bandeira="VISA",
                ultimos_digitos="1234"
            )
        else:
            return PinpadResponse(
                sucesso=False,
                mensagem="Transação recusada"
            )
    
    def venda_credito(self, valor: Decimal, parcelas: int = 1) -> PinpadResponse:
        """
        Realiza uma venda no crédito.
        
        Args:
            valor: Valor da transação
            parcelas: Número de parcelas
            
        Returns:
            PinpadResponse com resultado da transação
        """
        if not self.conectado:
            return PinpadResponse(
                sucesso=False,
                mensagem="Pinpad não conectado"
            )
        
        # Simulação de processamento
        print(f"[PINPAD] Processando venda crédito: R$ {valor} em {parcelas}x")
        time.sleep(2)
        
        # Simula aprovação (90% de chance)
        if random.random() < 0.9:
            nsu = self._gerar_nsu()
            codigo_aut = self._gerar_codigo_autorizacao()
            
            return PinpadResponse(
                sucesso=True,
                mensagem=f"Transação aprovada - {parcelas}x",
                nsu=nsu,
                codigo_autorizacao=codigo_aut,
                bandeira="MASTERCARD",
                ultimos_digitos="5678"
            )
        else:
            return PinpadResponse(
                sucesso=False,
                mensagem="Transação recusada"
            )
    
    def cancelar_transacao(self, nsu: str) -> PinpadResponse:
        """
        Cancela uma transação anterior.
        
        Args:
            nsu: NSU da transação a ser cancelada
            
        Returns:
            PinpadResponse com resultado do cancelamento
        """
        if not self.conectado:
            return PinpadResponse(
                sucesso=False,
                mensagem="Pinpad não conectado"
            )
        
        print(f"[PINPAD] Cancelando transação NSU: {nsu}")
        time.sleep(1.5)
        
        # Simula cancelamento bem-sucedido
        if random.random() < 0.95:
            return PinpadResponse(
                sucesso=True,
                mensagem="Transação cancelada com sucesso",
                nsu=nsu
            )
        else:
            return PinpadResponse(
                sucesso=False,
                mensagem="Erro ao cancelar transação"
            )
    
    def teste_comunicacao(self) -> bool:
        """
        Testa a comunicação com o pinpad.
        
        Returns:
            True se comunicação OK
        """
        if not self.conectado:
            return False
        
        print("[PINPAD] Testando comunicação...")
        time.sleep(0.5)
        return True
    
    def _gerar_nsu(self) -> str:
        """Gera um NSU simulado."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"{timestamp}{random_num}"
    
    def _gerar_codigo_autorizacao(self) -> str:
        """Gera um código de autorização simulado."""
        return f"{random.randint(100000, 999999)}"
    
    @staticmethod
    def formatar_valor_pinpad(valor: Decimal) -> str:
        """
        Formata valor para envio ao pinpad (geralmente em centavos).
        
        Args:
            valor: Valor em reais
            
        Returns:
            String com valor em centavos
        """
        centavos = int(valor * 100)
        return str(centavos)


# NOTAS PARA INTEGRAÇÃO REAL:
# 
# 1. Gertec (PPC920, Mobi Pin 10):
#    - SDK: Gertec GEDI (Python disponível)
#    - Documentação: https://www.gertec.com.br/
#
# 2. Ingenico (iWL250, Link2500):
#    - SDK: Ingenico Telium
#    - Requer certificação da adquirente
#
# 3. PAX (D195, S920):
#    - SDK: PAX PROLIN
#    - Suporte a múltiplas adquirentes
#
# 4. Integração com Adquirentes:
#    - Stone: Stone SDK
#    - Cielo: Cielo LIO / E-Commerce API
#    - Rede: Rede E-Commerce API
#    - Cada adquirente possui seu próprio SDK e credenciais
#
# 5. Certificação:
#    - Transações reais requerem certificação pela adquirente
#    - Testes devem ser feitos em ambiente de homologação
