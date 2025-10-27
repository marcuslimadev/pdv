"""
Sistema de logging para o PDV.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """Gerenciador de logs do sistema."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Implementação Singleton."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """Configura o sistema de logging."""
        # Cria diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Nome do arquivo de log com data atual
        log_file = log_dir / f"pdv_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configura o logger
        self._logger = logging.getLogger('PDV')
        self._logger.setLevel(logging.DEBUG)
        
        # Remove handlers existentes
        self._logger.handlers.clear()
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def debug(self, mensagem: str):
        """Registra mensagem de debug."""
        self._logger.debug(mensagem)
    
    def info(self, mensagem: str):
        """Registra mensagem informativa."""
        self._logger.info(mensagem)
    
    def warning(self, mensagem: str):
        """Registra aviso."""
        self._logger.warning(mensagem)
    
    def error(self, mensagem: str):
        """Registra erro."""
        self._logger.error(mensagem)
    
    def critical(self, mensagem: str):
        """Registra erro crítico."""
        self._logger.critical(mensagem)
    
    @staticmethod
    def log_operacao(usuario: str, operacao: str, detalhes: str = ""):
        """
        Registra uma operação do sistema.
        
        Args:
            usuario: Nome do usuário que executou a operação
            operacao: Descrição da operação
            detalhes: Detalhes adicionais
        """
        logger = Logger()
        mensagem = f"[{usuario}] {operacao}"
        if detalhes:
            mensagem += f" - {detalhes}"
        logger.info(mensagem)
    
    @staticmethod
    def log_venda(numero_venda: str, usuario: str, total: float):
        """Registra uma venda."""
        logger = Logger()
        logger.info(f"VENDA: {numero_venda} | Usuário: {usuario} | Total: R$ {total:.2f}")
    
    @staticmethod
    def log_pagamento(forma_pagamento: str, valor: float, status: str):
        """Registra um pagamento."""
        logger = Logger()
        logger.info(f"PAGAMENTO: {forma_pagamento} | Valor: R$ {valor:.2f} | Status: {status}")
    
    @staticmethod
    def log_abertura_caixa(usuario: str, valor_abertura: float):
        """Registra abertura de caixa."""
        logger = Logger()
        logger.info(f"ABERTURA DE CAIXA: Usuário: {usuario} | Valor: R$ {valor_abertura:.2f}")
    
    @staticmethod
    def log_fechamento_caixa(usuario: str, valor_fechamento: float):
        """Registra fechamento de caixa."""
        logger = Logger()
        logger.info(f"FECHAMENTO DE CAIXA: Usuário: {usuario} | Valor: R$ {valor_fechamento:.2f}")
    
    @staticmethod
    def log_erro(contexto: str, erro: Exception):
        """Registra um erro com contexto."""
        logger = Logger()
        logger.error(f"{contexto}: {type(erro).__name__} - {str(erro)}")


# Instância global do logger
app_logger = Logger()
