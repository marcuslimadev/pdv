"""
Serviço de geração de QR Code PIX.
"""

import qrcode
from io import BytesIO
from PIL import Image
from decimal import Decimal
from datetime import datetime
import json

from src.services.config_service import config_service


class PixService:
    """Serviço para geração de QR Code PIX."""
    
    @staticmethod
    def _get_chave_pix() -> str:
        """Obtém a chave PIX configurada."""
        return config_service.get_pix_chave_cliente() or "12345678901"
    
    @staticmethod
    def _get_nome_beneficiario() -> str:
        """Obtém o nome do beneficiário configurado."""
        return config_service.get_pix_nome_beneficiario() or "MEU MERCADINHO"
    
    @staticmethod
    def _get_cidade() -> str:
        """Obtém a cidade configurada."""
        return config_service.get_pix_cidade() or "SAO PAULO"
    
    @staticmethod
    def gerar_payload_pix(valor: Decimal, identificador: str = None) -> str:
        """
        Gera o payload PIX (EMV) para QR Code estático.
        
        Args:
            valor: Valor da transação
            identificador: Identificador único da transação
            
        Returns:
            String do payload PIX
        """
        # Simplificação do payload PIX (EMV)
        # Em produção, deve-se usar uma biblioteca específica ou API do banco
        
        if identificador is None:
            identificador = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Formato simplificado do payload PIX
        payload_dict = {
            "pixKey": PixService._get_chave_pix(),
            "description": f"Venda #{identificador}",
            "merchantName": PixService._get_nome_beneficiario(),
            "merchantCity": PixService._get_cidade(),
            "txid": identificador,
            "amount": str(float(valor))
        }
        
        # Retorna como JSON (em produção seria o payload EMV)
        return json.dumps(payload_dict, ensure_ascii=False)
    
    @staticmethod
    def gerar_qrcode_pix(valor: Decimal, identificador: str = None, tamanho: int = 300) -> Image:
        """
        Gera a imagem do QR Code PIX.
        
        Args:
            valor: Valor da transação
            identificador: Identificador único da transação
            tamanho: Tamanho da imagem em pixels
            
        Returns:
            Imagem PIL do QR Code
        """
        payload = PixService.gerar_payload_pix(valor, identificador)
        
        # Cria o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(payload)
        qr.make(fit=True)
        
        # Gera a imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Redimensiona
        img = img.resize((tamanho, tamanho), Image.LANCZOS)
        
        return img
    
    @staticmethod
    def salvar_qrcode(valor: Decimal, caminho: str, identificador: str = None):
        """
        Gera e salva o QR Code PIX em um arquivo.
        
        Args:
            valor: Valor da transação
            caminho: Caminho do arquivo de saída
            identificador: Identificador único da transação
        """
        img = PixService.gerar_qrcode_pix(valor, identificador)
        img.save(caminho)
    
    @staticmethod
    def gerar_qrcode_bytes(valor: Decimal, identificador: str = None) -> bytes:
        """
        Gera o QR Code PIX como bytes.
        
        Args:
            valor: Valor da transação
            identificador: Identificador único da transação
            
        Returns:
            Bytes da imagem PNG
        """
        img = PixService.gerar_qrcode_pix(valor, identificador)
        
        # Converte para bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    
    @staticmethod
    def configurar_chave_pix(chave: str, nome_beneficiario: str = None, cidade: str = None):
        """
        Configura os dados do PIX do estabelecimento.
        
        Args:
            chave: Chave PIX
            nome_beneficiario: Nome do beneficiário
            cidade: Cidade
        """
        config_service.set_pix_chave_cliente(chave)
        
        if nome_beneficiario:
            config_service.set_pix_nome_beneficiario(nome_beneficiario)
        
        if cidade:
            config_service.set_pix_cidade(cidade)
    
    @staticmethod
    def validar_chave_pix(chave: str) -> tuple[bool, str]:
        """
        Valida uma chave PIX.
        
        Args:
            chave: Chave PIX
            
        Returns:
            Tupla (válido, tipo_chave)
        """
        if not chave:
            return False, ""
        
        import re
        
        # Remove espaços
        chave = chave.strip()
        
        # CPF (11 dígitos)
        if re.match(r'^\d{11}$', chave):
            return True, "CPF"
        
        # CNPJ (14 dígitos)
        if re.match(r'^\d{14}$', chave):
            return True, "CNPJ"
        
        # Email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', chave):
            return True, "Email"
        
        # Telefone
        if re.match(r'^\+?\d{10,15}$', chave.replace(' ', '')):
            return True, "Telefone"
        
        # Chave aleatória (UUID)
        if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', chave, re.I):
            return True, "Chave Aleatória"
        
        return False, ""
    
    def gerar_pix_estatico(self, valor: float, descricao: str = "Pagamento PDV") -> dict:
        """
        Gera PIX estático com QR Code.
        
        Args:
            valor: Valor do PIX
            descricao: Descrição do pagamento
            
        Returns:
            Dados do PIX com QR Code
        """
        try:
            from src.services.config_service import config_service
            
            # Obter configurações PIX
            chave_pix = config_service.get_pix_chave_cliente()
            nome_beneficiario = config_service.get_pix_nome_beneficiario()
            cidade = config_service.get_pix_cidade()
            
            if not chave_pix:
                # Usar chave padrão se não configurada
                chave_pix = "92992287144"  # PIX da plataforma como fallback
                nome_beneficiario = "MEU MERCADINHO"
                cidade = "SAO PAULO"
            
            # Gerar código PIX simples
            pix_code = f"PIX:{chave_pix}:R${valor:.2f}:{descricao}".replace('.', ',')
            
            # Gerar QR Code
            qr_code_base64 = self._gerar_qr_code_base64(pix_code)
            
            return {
                "qr_code": pix_code,
                "qr_code_base64": qr_code_base64,
                "chave_pix": chave_pix,
                "nome_beneficiario": nome_beneficiario,
                "cidade": cidade,
                "valor": valor,
                "descricao": descricao
            }
            
        except Exception as e:
            print(f"Erro ao gerar PIX estático: {str(e)}")
            return None
    
    def _gerar_qr_code_base64(self, data: str) -> str:
        """Gera QR Code em base64."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Criar imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para base64
            import base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            print(f"Erro ao gerar QR Code: {str(e)}")
            return "QR_CODE_ERROR"
