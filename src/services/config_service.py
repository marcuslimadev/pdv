"""Serviço para gestão de configurações dinâmicas do sistema."""

from __future__ import annotations

from typing import Optional

from src.config.database import DatabaseConnection


# ==================== CONSTANTES FIXAS DO SISTEMA ====================
# PIX da plataforma (NÃO PODE SER ALTERADO PELO USUÁRIO)
PIX_PLATAFORMA = "92992287144"

# Percentuais fixos de divisão (NÃO PODEM SER ALTERADOS PELO USUÁRIO)
PERCENTUAL_CLIENTE = 99  # 99% para o cliente
PERCENTUAL_PLATAFORMA = 1  # 1% para a plataforma
# =====================================================================


class ConfigService:
    """Fornece acesso centralizado às configurações persistidas."""

    _TABLE_NAME = "configuracoes_sistema"
    _CACHE: dict[str, str] = {}
    _TABLE_READY = False
    _DEFAULTS = {
        "pix_chave_cliente": "",
        "pix_nome_beneficiario": "MEU MERCADINHO",
        "pix_cidade": "SAO PAULO",
        "mercadopago_access_token": "",
    }

    @classmethod
    def _ensure_table(cls) -> None:
        """Garante existência da tabela e valores padrão."""
        if cls._TABLE_READY:
            return

        with DatabaseConnection.get_cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {cls._TABLE_NAME} (
                    chave VARCHAR(100) PRIMARY KEY,
                    valor VARCHAR(255) NOT NULL,
                    descricao VARCHAR(255) NULL,
                    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
            )
        cls._TABLE_READY = True

        for chave, valor in cls._DEFAULTS.items():
            cls.get_config(chave, valor)

    @classmethod
    def get_config(cls, chave: str, default: str | None = None) -> str | None:
        """Obtém configuração como string, com cache simples."""
        cls._ensure_table()

        if chave in cls._CACHE:
            return cls._CACHE[chave]

        with DatabaseConnection.get_cursor() as cursor:
            cursor.execute(
                f"SELECT valor FROM {cls._TABLE_NAME} WHERE chave = %s",
                (chave,)
            )
            row = cursor.fetchone()

        if row and row.get("valor") is not None:
            valor = row["valor"]
        else:
            valor = default
            if default is not None:
                cls.set_config(chave, default)

        if valor is not None:
            cls._CACHE[chave] = valor

        return valor

    @classmethod
    def set_config(cls, chave: str, valor: str, descricao: str | None = None) -> None:
        """Salva configuração e atualiza cache."""
        cls._ensure_table()

        with DatabaseConnection.get_cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {cls._TABLE_NAME} (chave, valor, descricao)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE valor = VALUES(valor), descricao = VALUES(descricao),
                                        atualizado_em = CURRENT_TIMESTAMP
                """,
                (chave, valor, descricao),
            )

        cls._CACHE[chave] = valor

    # ==================== CONFIGURAÇÕES PIX CLIENTE ====================
    
    @classmethod
    def get_pix_chave_cliente(cls) -> str:
        """Obtém a chave PIX do cliente."""
        return cls.get_config("pix_chave_cliente", cls._DEFAULTS["pix_chave_cliente"]) or ""
    
    @classmethod
    def set_pix_chave_cliente(cls, chave: str) -> None:
        """Define a chave PIX do cliente."""
        cls.set_config("pix_chave_cliente", chave, "Chave PIX do estabelecimento")
    
    @classmethod
    def get_pix_nome_beneficiario(cls) -> str:
        """Obtém o nome do beneficiário PIX."""
        return cls.get_config("pix_nome_beneficiario", cls._DEFAULTS["pix_nome_beneficiario"]) or "MEU MERCADINHO"
    
    @classmethod
    def set_pix_nome_beneficiario(cls, nome: str) -> None:
        """Define o nome do beneficiário PIX."""
        cls.set_config("pix_nome_beneficiario", nome, "Nome do beneficiário PIX")
    
    @classmethod
    def get_pix_cidade(cls) -> str:
        """Obtém a cidade do beneficiário PIX."""
        return cls.get_config("pix_cidade", cls._DEFAULTS["pix_cidade"]) or "SAO PAULO"
    
    @classmethod
    def set_pix_cidade(cls, cidade: str) -> None:
        """Define a cidade do beneficiário PIX."""
        cls.set_config("pix_cidade", cidade, "Cidade do beneficiário PIX")
    
    # ==================== CONFIGURAÇÕES MERCADO PAGO ====================
    
    @classmethod
    def get_mercadopago_access_token(cls) -> str:
        """Obtém o access token do Mercado Pago."""
        return cls.get_config("mercadopago_access_token", cls._DEFAULTS["mercadopago_access_token"]) or ""
    
    @classmethod
    def set_mercadopago_access_token(cls, token: str) -> None:
        """Define o access token do Mercado Pago."""
        cls.set_config("mercadopago_access_token", token, "Access Token Mercado Pago")


config_service = ConfigService
