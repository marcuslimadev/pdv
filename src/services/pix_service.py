"""
Serviço de geração de QR Code PIX.
"""

import qrcode
from io import BytesIO
from PIL import Image
from decimal import Decimal
from datetime import datetime
import json


class PixService:
    """Serviço para geração de QR Code PIX."""
    
    # Dados do estabelecimento (configuráveis)
    CHAVE_PIX = "12345678901"  # CPF/CNPJ/Email/Telefone/Chave aleatória
    NOME_BENEFICIARIO = "MEU MERCADINHO"
    CIDADE = "SAO PAULO"
    
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
            "pixKey": PixService.CHAVE_PIX,
            "description": f"Venda #{identificador}",
            "merchantName": PixService.NOME_BENEFICIARIO,
            "merchantCity": PixService.CIDADE,
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
        PixService.CHAVE_PIX = chave
        
        if nome_beneficiario:
            PixService.NOME_BENEFICIARIO = nome_beneficiario
        
        if cidade:
            PixService.CIDADE = cidade
    
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
