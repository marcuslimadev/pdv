"""
Serviço para processamento de split via PIX interno.
"""

import requests
import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Optional, Dict, Any

from src.utils.logger import Logger
from src.services.config_service import config_service, PERCENTUAL_CLIENTE, PERCENTUAL_PLATAFORMA, PIX_PLATAFORMA


class PIXSplitService:
    """Serviço para processamento de split via PIX interno."""

    def __init__(self):
        self.base_url = "https://api.mercadopago.com"

    @property
    def access_token(self) -> str:
        """Obtém o access token do Mercado Pago."""
        return config_service.get_mercadopago_access_token()

    def calcular_split(self, valor_total: Decimal) -> Dict[str, Decimal]:
        """
        Calcula os valores do split baseado nos percentuais fixos.

        Args:
            valor_total: Valor total do pagamento

        Returns:
            Dicionário com valores calculados
        """
        # Converte para centavos para evitar problemas de arredondamento
        total_centavos = int(valor_total * 100)

        # Calcula valores em centavos
        cliente_centavos = (total_centavos * PERCENTUAL_CLIENTE) // 100
        plataforma_centavos = total_centavos - cliente_centavos  # Garante que some 100%

        # Converte de volta para Decimal
        valor_cliente = Decimal(cliente_centavos) / 100
        valor_plataforma = Decimal(plataforma_centavos) / 100

        return {
            'valor_total': valor_total,
            'valor_cliente': valor_cliente,
            'valor_plataforma': valor_plataforma,
            'percentual_cliente': PERCENTUAL_CLIENTE,
            'percentual_plataforma': PERCENTUAL_PLATAFORMA
        }

    def criar_pix_interno(self, valor: Decimal, chave_pix_destino: str,
                         descricao: str = "Split PDV") -> Optional[Dict[str, Any]]:
        """
        Cria um PIX interno (transferência) para a conta de destino.
        NOTA: Esta funcionalidade pode não estar disponível na API atual do Mercado Pago.

        Args:
            valor: Valor a transferir
            chave_pix_destino: Chave PIX do destinatário
            descricao: Descrição da transferência

        Returns:
            Dados da transferência criada ou None se erro
        """
        Logger.log_operacao("PIXSplit", "TRANSFERENCIA_SIMULADA",
                          f"Valor: R$ {float(valor):.2f} - Destino: {chave_pix_destino} - Descrição: {descricao}")
        return {"id": f"SIMULADO_{int(datetime.now().timestamp())}", "status": "simulado"}

    def processar_split_pagamento(self, payment_id_original: str, valor_total: Decimal) -> bool:
        """
        Processa o split de um pagamento aprovado.

        Args:
            payment_id_original: ID do pagamento original no Mercado Pago
            valor_total: Valor total do pagamento

        Returns:
            True se o split foi processado com sucesso
        """
        try:
            Logger.log_operacao("PIXSplit", "INICIANDO_SPLIT",
                              f"Payment ID: {payment_id_original} - Valor: R$ {float(valor_total):.2f}")

            # Calcula os valores do split
            split_info = self.calcular_split(valor_total)

            Logger.log_operacao("PIXSplit", "CALCULO_SPLIT",
                              f"Cliente: R$ {float(split_info['valor_cliente']):.2f} ({split_info['percentual_cliente']}%) - "
                              f"Plataforma: R$ {float(split_info['valor_plataforma']):.2f} ({split_info['percentual_plataforma']}%)")

            # Por enquanto, apenas registra o split necessário
            # TODO: Implementar transferência PIX automática quando disponível na API do Mercado Pago
            Logger.log_operacao("PIXSplit", "SPLIT_REGISTRADO",
                              f"Payment ID: {payment_id_original} - Valor plataforma: R$ {float(split_info['valor_plataforma']):.2f} - "
                              f"PIX destino: {PIX_PLATAFORMA} - Status: PENDENTE_PROCESSAMENTO_MANUAL")

            # Salvar em arquivo para processamento posterior
            self._salvar_split_pendente(payment_id_original, split_info)

            return True

        except Exception as e:
            Logger.log_erro("PIXSplit", f"Erro no processamento do split: {str(e)}")
            return False

    def _salvar_split_pendente(self, payment_id: str, split_info: Dict[str, Decimal]):
        """Salva informações do split pendente para processamento manual."""
        try:
            import json
            from datetime import datetime

            dados_split = {
                "payment_id": payment_id,
                "valor_total": float(split_info['valor_total']),
                "valor_cliente": float(split_info['valor_cliente']),
                "valor_plataforma": float(split_info['valor_plataforma']),
                "percentual_cliente": split_info['percentual_cliente'],
                "percentual_plataforma": split_info['percentual_plataforma'],
                "pix_plataforma": PIX_PLATAFORMA,
                "data_processamento": datetime.now().isoformat(),
                "status": "PENDENTE"
            }

            # Salvar em arquivo JSON
            arquivo_splits = "splits_pendentes.json"
            try:
                with open(arquivo_splits, 'r', encoding='utf-8') as f:
                    splits = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                splits = []

            splits.append(dados_split)

            with open(arquivo_splits, 'w', encoding='utf-8') as f:
                json.dump(splits, f, indent=2, ensure_ascii=False)

            Logger.log_operacao("PIXSplit", "SPLIT_SALVO_ARQUIVO",
                              f"Payment ID: {payment_id} - Arquivo: {arquivo_splits}")

        except Exception as e:
            Logger.log_erro("PIXSplit", f"Erro ao salvar split pendente: {str(e)}")

    def verificar_status_transferencia(self, transfer_id: str) -> Optional[str]:
        """
        Verifica o status de uma transferência PIX.

        Args:
            transfer_id: ID da transferência

        Returns:
            Status da transferência ou None se erro
        """
        try:
            url = f"{self.base_url}/v1/payments/{transfer_id}"

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                transfer_data = response.json()
                status = transfer_data.get("status")

                Logger.log_operacao("PIXSplit", "STATUS_TRANSFERENCIA_VERIFICADO",
                                  f"Transfer {transfer_id}: {status}")

                return status
            else:
                Logger.log_erro("PIXSplit", f"Erro ao verificar status da transferência: {response.text}")
                return None

        except Exception as e:
            Logger.log_erro("PIXSplit", f"Erro ao verificar status da transferência: {str(e)}")
            return None


# Instância global
pix_split_service = PIXSplitService()