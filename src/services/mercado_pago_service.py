"""
Serviço de integração com Mercado Pago para PIX.
"""

import requests
import json
import time
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.utils.logger import Logger
from src.services.config_service import config_service, PERCENTUAL_PLATAFORMA, PIX_PLATAFORMA


class MercadoPagoService:
    """Serviço para integração com Mercado Pago."""
    
    def __init__(self):
        # Access token vem das configurações do banco de dados
        self.base_url = "https://api.mercadopago.com"
        self.webhook_url = "https://your-domain.com/webhook/mercadopago"  # URL do webhook
    
    @property
    def access_token(self) -> str:
        """Obtém o access token do Mercado Pago das configurações."""
        return config_service.get_mercadopago_access_token()
        
    def criar_pagamento_pix(self, valor: Decimal, descricao: str = "Venda PDV") -> Optional[Dict[str, Any]]:
        """
        Cria um pagamento PIX no Mercado Pago com split automático.
        99% vai para a chave PIX do cliente
        1% vai para a chave PIX da plataforma
        
        Args:
            valor: Valor do pagamento
            descricao: Descrição do pagamento
            
        Returns:
            Dados do pagamento criado ou None se erro
        """
        try:
            if not self.access_token:
                Logger.log_erro("MercadoPago", "Access token não configurado")
                return None
            
            # Calcula o split de valores
            valor_float = float(valor)
            valor_plataforma = round(valor_float * (PERCENTUAL_PLATAFORMA / 100), 2)  # 1%
            valor_cliente = round(valor_float - valor_plataforma, 2)  # 99%
            
            Logger.log_operacao("MercadoPago", "SPLIT_CALCULADO", 
                              f"Total: R$ {valor_float:.2f} | Cliente (99%): R$ {valor_cliente:.2f} | Plataforma (1%): R$ {valor_plataforma:.2f}".replace('.', ','))
            
            url = f"{self.base_url}/v1/payments"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Idempotency-Key": f"PDV_{int(time.time() * 1000)}"  # Header obrigatório
            }
            
            # Data de expiração: formato ISO 8601 com timezone
            expiration_date = datetime.now() + timedelta(minutes=15)
            date_str = expiration_date.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")  # Formato com timezone BR
            
            # Obtém a chave PIX do cliente das configurações
            chave_pix_cliente = config_service.get_pix_chave_cliente()
            
            # Monta o payload do pagamento
            payment_data = {
                "transaction_amount": valor_float,
                "description": descricao,
                "payment_method_id": "pix",
                "payer": {
                    "email": "cliente@pdv.com"  # Email genérico
                },
                "date_of_expiration": date_str,
                "external_reference": f"PDV_{int(time.time())}",  # Referência única
            }
            
            # Adiciona split de pagamento se a chave PIX do cliente estiver configurada
            if chave_pix_cliente:
                payment_data["application_fee"] = valor_plataforma  # Taxa para a plataforma (1%)
                
                # Metadata para rastreamento
                payment_data["metadata"] = {
                    "split_cliente": valor_cliente,
                    "split_plataforma": valor_plataforma,
                    "percentual_cliente": 99,
                    "percentual_plataforma": 1,
                    "chave_pix_cliente": chave_pix_cliente,
                    "chave_pix_plataforma": PIX_PLATAFORMA
                }
                
                Logger.log_operacao("MercadoPago", "SPLIT_CONFIGURADO", 
                                  f"Split ativado - Cliente: {chave_pix_cliente} | Plataforma: {PIX_PLATAFORMA}")
            else:
                Logger.log_operacao("MercadoPago", "SPLIT_DESABILITADO", 
                                  "Chave PIX do cliente não configurada - Split desabilitado")
                
                # Metadata sem split
                payment_data["metadata"] = {
                    "split_habilitado": False,
                    "motivo": "Chave PIX do cliente não configurada"
                }
            
            response = requests.post(url, headers=headers, json=payment_data)
            
            if response.status_code == 201:
                payment_data = response.json()
                Logger.log_operacao("MercadoPago", "PIX_CRIADO", f"Payment ID: {payment_data['id']}")
                return payment_data
            else:
                Logger.log_erro("MercadoPago", f"Erro ao criar PIX: {response.text}")
                return None
                
        except Exception as e:
            Logger.log_erro("MercadoPago", f"Erro na integração PIX: {str(e)}")
            return None
    
    def obter_qr_code_pix(self, payment_data: Dict[str, Any]) -> Optional[str]:
        """
        Obtém o código PIX Copia e Cola.
        
        Args:
            payment_data: Dados do pagamento criado
            
        Returns:
            Código PIX Copia e Cola ou None se erro
        """
        try:
            # O código PIX está no campo point_of_interaction
            pix_data = payment_data.get("point_of_interaction", {})
            transaction_data = pix_data.get("transaction_data", {})
            
            qr_code = transaction_data.get("qr_code")
            qr_code_base64 = transaction_data.get("qr_code_base64")
            
            return {
                "qr_code": qr_code,  # Código copia e cola
                "qr_code_base64": qr_code_base64,  # QR Code em base64
                "payment_id": payment_data["id"]
            }
            
        except Exception as e:
            Logger.log_erro("MercadoPago", f"Erro ao obter QR Code: {str(e)}")
            return None
    
    def verificar_status_pagamento(self, payment_id: str) -> Optional[str]:
        """
        Verifica o status de um pagamento.
        
        Args:
            payment_id: ID do pagamento
            
        Returns:
            Status do pagamento ou None se erro
        """
        try:
            url = f"{self.base_url}/v1/payments/{payment_id}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                payment_data = response.json()
                status = payment_data.get("status")
                
                Logger.log_operacao("MercadoPago", "STATUS_VERIFICADO", 
                                  f"Payment {payment_id}: {status}")
                
                return status
            else:
                Logger.log_erro("MercadoPago", f"Erro ao verificar status: {response.text}")
                return None
                
        except Exception as e:
            Logger.log_erro("MercadoPago", f"Erro ao verificar status: {str(e)}")
            return None
    
    def cancelar_pagamento(self, payment_id: str) -> bool:
        """
        Cancela um pagamento PIX.
        
        Args:
            payment_id: ID do pagamento
            
        Returns:
            True se cancelado com sucesso
        """
        try:
            url = f"{self.base_url}/v1/payments/{payment_id}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Idempotency-Key": f"PDV_CANCEL_{int(time.time() * 1000)}"
            }
            
            data = {"status": "cancelled"}
            
            response = requests.put(url, headers=headers, json=data)
            
            if response.status_code == 200:
                Logger.log_operacao("MercadoPago", "PIX_CANCELADO", f"Payment ID: {payment_id}")
                return True
            else:
                Logger.log_erro("MercadoPago", f"Erro ao cancelar PIX: {response.text}")
                return False
                
        except Exception as e:
            Logger.log_erro("MercadoPago", f"Erro ao cancelar PIX: {str(e)}")
            return False


class PIXMonitor:
    """Monitor para verificar status de pagamentos PIX."""
    
    def __init__(self, mercado_pago_service: MercadoPagoService):
        self.mp_service = mercado_pago_service
        self.pagamentos_monitorados = {}  # payment_id -> callback
        self.monitoring = False
    
    def adicionar_monitoramento(self, payment_id: str, callback_aprovado, callback_erro):
        """
        Adiciona um pagamento para monitoramento.
        
        Args:
            payment_id: ID do pagamento
            callback_aprovado: Função chamada quando aprovado
            callback_erro: Função chamada quando erro/cancelado
        """
        self.pagamentos_monitorados[payment_id] = {
            "callback_aprovado": callback_aprovado,
            "callback_erro": callback_erro,
            "tentativas": 0,
            "max_tentativas": 60  # 5 minutos (5s * 60)
        }
        
        if not self.monitoring:
            self.iniciar_monitoramento()
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento dos pagamentos."""
        import threading
        
        def monitorar():
            self.monitoring = True
            
            while self.pagamentos_monitorados and self.monitoring:
                payments_to_remove = []
                
                for payment_id, data in self.pagamentos_monitorados.items():
                    status = self.mp_service.verificar_status_pagamento(payment_id)
                    
                    if status == "approved":
                        # Pagamento aprovado
                        data["callback_aprovado"]()
                        payments_to_remove.append(payment_id)
                        
                    elif status == "cancelled" or status == "rejected":
                        # Pagamento cancelado/rejeitado
                        data["callback_erro"]("Pagamento " + status)
                        payments_to_remove.append(payment_id)
                        
                    elif data["tentativas"] >= data["max_tentativas"]:
                        # Timeout
                        data["callback_erro"]("Timeout - PIX expirado")
                        payments_to_remove.append(payment_id)
                    
                    else:
                        # Ainda pendente, incrementa tentativas
                        data["tentativas"] += 1
                
                # Remove pagamentos finalizados
                for payment_id in payments_to_remove:
                    del self.pagamentos_monitorados[payment_id]
                
                # Aguarda 5 segundos antes da próxima verificação
                time.sleep(5)
            
            self.monitoring = False
        
        thread = threading.Thread(target=monitorar, daemon=True)
        thread.start()
    
    def parar_monitoramento(self):
        """Para o monitoramento."""
        self.monitoring = False
        self.pagamentos_monitorados.clear()
    
    def remover_monitoramento(self, payment_id: str):
        """Remove um pagamento específico do monitoramento."""
        if payment_id in self.pagamentos_monitorados:
            del self.pagamentos_monitorados[payment_id]


# Instância global
mercado_pago_service = MercadoPagoService()
pix_monitor = PIXMonitor(mercado_pago_service)