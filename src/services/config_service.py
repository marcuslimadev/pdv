"""Serviço para gestão de configurações dinâmicas do sistema."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Tuple

from src.config.database import DatabaseConnection


class ConfigService:
    """Fornece acesso centralizado às configurações persistidas."""

    _TABLE_NAME = "configuracoes_sistema"
    _CACHE: dict[str, str] = {}
    _TABLE_READY = False
    _DEFAULTS = {
        "pix_platform_percent": "1.00",
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

    @classmethod
    def get_pix_split_percentages(cls) -> Tuple[Decimal, Decimal]:
        """Retorna percentuais (cliente, plataforma)."""
        raw = cls.get_config("pix_platform_percent", cls._DEFAULTS["pix_platform_percent"])
        try:
            plataforma = Decimal(str(raw or "0"))
        except (InvalidOperation, TypeError):
            plataforma = Decimal(cls._DEFAULTS["pix_platform_percent"])

        plataforma = max(
            Decimal("0"),
            min(Decimal("100"), plataforma.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        )
        cliente = (Decimal("100") - plataforma).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return cliente, plataforma

    @classmethod
    def set_pix_platform_percent(cls, plataforma: Decimal) -> Tuple[Decimal, Decimal]:
        """Atualiza percentual da plataforma e devolve (cliente, plataforma)."""
        plataforma = max(
            Decimal("0"),
            min(Decimal("100"), plataforma.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        )
        cliente = (Decimal("100") - plataforma).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        cls.set_config("pix_platform_percent", f"{plataforma:.2f}")
        return cliente, plataforma


config_service = ConfigService
