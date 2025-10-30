"""
Módulo para leitura centralizada de configurações do sistema.
Lê o arquivo config.ini e fornece acesso às configurações.
"""

import configparser
import os
from pathlib import Path
from typing import Optional


class ConfigReader:
    """Leitor centralizado de configurações do sistema."""
    
    _instance = None
    _config = None
    _config_path = None
    
    def __new__(cls):
        """Implementa Singleton para garantir única instância."""
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._carregar_config()
        return cls._instance
    
    def _carregar_config(self):
        """Carrega o arquivo de configuração."""
        # Procura config.ini na raiz do projeto
        base_path = Path(__file__).parent.parent.parent
        self._config_path = base_path / "config.ini"
        
        if not self._config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self._config_path}\n"
                f"Por favor, copie config.ini.example para config.ini e configure adequadamente."
            )
        
        self._config = configparser.ConfigParser()
        self._config.read(self._config_path, encoding='utf-8')
    
    def recarregar(self):
        """Recarrega o arquivo de configuração."""
        self._carregar_config()
    
    # ========== DATABASE ==========
    
    def get_db_host(self) -> str:
        """Retorna o host do banco de dados."""
        return self._config.get('database', 'host', fallback='localhost')
    
    def get_db_port(self) -> int:
        """Retorna a porta do banco de dados."""
        return self._config.getint('database', 'port', fallback=3306)
    
    def get_db_user(self) -> str:
        """Retorna o usuário do banco de dados."""
        return self._config.get('database', 'user', fallback='root')
    
    def get_db_password(self) -> str:
        """Retorna a senha do banco de dados."""
        return self._config.get('database', 'password', fallback='')
    
    def get_db_name(self) -> str:
        """Retorna o nome do banco de dados."""
        return self._config.get('database', 'database', fallback='pdv_sistema')
    
    def get_db_pool_size(self) -> int:
        """Retorna o tamanho do pool de conexões."""
        return self._config.getint('database', 'pool_size', fallback=5)
    
    # ========== MERCADO PAGO ==========
    
    def get_mp_access_token(self) -> Optional[str]:
        """Retorna o access token do Mercado Pago."""
        token = self._config.get('mercadopago', 'access_token', fallback='')
        return token if token else None
    
    def get_mp_public_key(self) -> Optional[str]:
        """Retorna a public key do Mercado Pago."""
        key = self._config.get('mercadopago', 'public_key', fallback='')
        return key if key else None
    
    def get_mp_percentual_plataforma(self) -> float:
        """Retorna o percentual de comissão da plataforma."""
        return self._config.getfloat('mercadopago', 'percentual_plataforma', fallback=1.0)
    
    def get_mp_webhook_url(self) -> Optional[str]:
        """Retorna a URL de webhook do Mercado Pago."""
        url = self._config.get('mercadopago', 'webhook_url', fallback='')
        return url if url else None
    
    # ========== PIX ==========
    
    def get_pix_chave(self) -> Optional[str]:
        """Retorna a chave PIX."""
        chave = self._config.get('pix', 'chave_pix', fallback='')
        return chave if chave else None
    
    def get_pix_nome_recebedor(self) -> str:
        """Retorna o nome do recebedor PIX."""
        return self._config.get('pix', 'nome_recebedor', fallback='PDV Sistema')
    
    def get_pix_cidade_recebedor(self) -> str:
        """Retorna a cidade do recebedor PIX."""
        return self._config.get('pix', 'cidade_recebedor', fallback='São Paulo')
    
    # ========== SISTEMA ==========
    
    def get_nome_empresa(self) -> str:
        """Retorna o nome da empresa."""
        return self._config.get('sistema', 'nome_empresa', fallback='PDV Sistema')
    
    def get_cnpj(self) -> Optional[str]:
        """Retorna o CNPJ da empresa."""
        cnpj = self._config.get('sistema', 'cnpj', fallback='')
        return cnpj if cnpj else None
    
    def get_endereco(self) -> Optional[str]:
        """Retorna o endereço da empresa."""
        endereco = self._config.get('sistema', 'endereco', fallback='')
        return endereco if endereco else None
    
    def get_telefone(self) -> Optional[str]:
        """Retorna o telefone da empresa."""
        telefone = self._config.get('sistema', 'telefone', fallback='')
        return telefone if telefone else None
    
    def get_log_path(self) -> str:
        """Retorna o caminho para os logs."""
        return self._config.get('sistema', 'log_path', fallback='logs')
    
    def get_backup_path(self) -> str:
        """Retorna o caminho para os backups."""
        return self._config.get('sistema', 'backup_path', fallback='backups')
    
    def get_reports_path(self) -> str:
        """Retorna o caminho para os relatórios."""
        return self._config.get('sistema', 'reports_path', fallback='reports')
    
    def get_log_level(self) -> str:
        """Retorna o nível de log."""
        return self._config.get('sistema', 'log_level', fallback='INFO')
    
    def get_estoque_minimo_padrao(self) -> int:
        """Retorna o estoque mínimo padrão."""
        return self._config.getint('sistema', 'estoque_minimo_padrao', fallback=5)
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def get(self, section: str, key: str, fallback=None):
        """Método genérico para obter qualquer configuração."""
        return self._config.get(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback=None):
        """Método genérico para obter configuração inteira."""
        return self._config.getint(section, key, fallback=fallback)
    
    def getfloat(self, section: str, key: str, fallback=None):
        """Método genérico para obter configuração float."""
        return self._config.getfloat(section, key, fallback=fallback)
    
    def getboolean(self, section: str, key: str, fallback=None):
        """Método genérico para obter configuração booleana."""
        return self._config.getboolean(section, key, fallback=fallback)


# Instância global para fácil acesso
config = ConfigReader()
