"""
Módulo de configuração do banco de dados MySQL.
Utiliza config.ini para credenciais e configurações.
"""

import mysql.connector
from mysql.connector import pooling, Error
from contextlib import contextmanager
from .config_reader import config


class DatabaseConfig:
    """Configuração centralizada do banco de dados."""
    
    @staticmethod
    def get_host():
        return config.get_db_host()
    
    @staticmethod
    def get_port():
        return config.get_db_port()
    
    @staticmethod
    def get_user():
        return config.get_db_user()
    
    @staticmethod
    def get_password():
        return config.get_db_password()
    
    @staticmethod
    def get_database():
        return config.get_db_name()
    
    @staticmethod
    def get_pool_size():
        return config.get_db_pool_size()
    
    POOL_NAME = 'pdv_pool'


class DatabaseConnection:
    """Gerenciador de conexão com pool de conexões."""
    
    _pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Inicializa o pool de conexões."""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name=DatabaseConfig.POOL_NAME,
                    pool_size=DatabaseConfig.get_pool_size(),
                    pool_reset_session=True,
                    host=DatabaseConfig.get_host(),
                    port=DatabaseConfig.get_port(),
                    user=DatabaseConfig.get_user(),
                    password=DatabaseConfig.get_password(),
                    database=DatabaseConfig.get_database(),
                    charset='utf8mb4',
                    collation='utf8mb4_unicode_ci',
                    autocommit=False
                )
                print(f"✓ Pool de conexões criado com sucesso ({DatabaseConfig.get_pool_size()} conexões)")
            except Error as e:
                print(f"✗ Erro ao criar pool de conexões: {e}")
                raise
    
    @classmethod
    def get_connection(cls, retry_count=3, retry_delay=1):
        """
        Obtém uma conexão do pool com retry logic.
        
        Args:
            retry_count: Número máximo de tentativas
            retry_delay: Delay em segundos entre tentativas
            
        Returns:
            Conexão do pool
            
        Raises:
            Error: Se falhar após todas as tentativas
        """
        import time
        from src.utils.logger import Logger
        
        if cls._pool is None:
            cls.initialize_pool()
        
        last_error = None
        for tentativa in range(1, retry_count + 1):
            try:
                connection = cls._pool.get_connection()
                
                # Testa se a conexão está válida
                if connection.is_connected():
                    return connection
                    
            except Error as e:
                last_error = e
                Logger.warning(
                    f"Tentativa {tentativa}/{retry_count} falhou ao obter conexão: {e}"
                )
                
                if tentativa < retry_count:
                    time.sleep(retry_delay)
                    # Tenta reinicializar o pool
                    try:
                        cls._pool = None
                        cls.initialize_pool()
                    except:
                        pass
        
        # Após todas as tentativas
        Logger.error(f"Falha ao conectar após {retry_count} tentativas: {last_error}")
        raise last_error
    
    @classmethod
    @contextmanager
    def get_cursor(cls, dictionary=True):
        """
        Context manager para obter cursor com gerenciamento automático.
        
        Args:
            dictionary (bool): Se True, retorna resultados como dicionário
            
        Yields:
            cursor: Cursor do banco de dados
        """
        from src.utils.logger import Logger
        
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()  # Usa retry logic
            cursor = connection.cursor(dictionary=dictionary)
            yield cursor
            connection.commit()
            
        except Error as e:
            if connection:
                connection.rollback()
            
            # Log detalhado do erro
            Logger.error(f"Erro na transação do banco de dados: {e}")
            import traceback
            Logger.error(f"Stack trace:\n{traceback.format_exc()}")
            
            raise
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def test_connection(cls):
        """Testa a conexão com o banco de dados."""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.get_host(),
                port=DatabaseConfig.get_port(),
                user=DatabaseConfig.get_user(),
                password=DatabaseConfig.get_password(),
                database=DatabaseConfig.get_database()
            )
            
            if connection.is_connected():
                db_info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                database = cursor.fetchone()[0]
                cursor.close()
                connection.close()
                
                print(f"✓ Conectado ao MySQL Server v{db_info}")
                print(f"✓ Banco de dados ativo: {database}")
                return True
        except Error as e:
            print(f"✗ Erro ao conectar ao banco de dados: {e}")
            return False
    
    @classmethod
    def execute_script(cls, script_path):
        """
        Executa um script SQL do arquivo.
        
        Args:
            script_path (str): Caminho do arquivo SQL
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Dividir por statement (separado por ;)
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            connection = cls.get_connection()
            cursor = connection.cursor()
            
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        print(f"Aviso: {e}")
            
            connection.commit()
            cursor.close()
            connection.close()
            print(f"✓ Script SQL executado com sucesso")
            
        except FileNotFoundError:
            print(f"✗ Arquivo não encontrado: {script_path}")
        except Error as e:
            print(f"✗ Erro ao executar script: {e}")


# Inicializar pool ao importar o módulo
try:
    DatabaseConnection.initialize_pool()
except Exception as e:
    print(f"⚠ Aviso: Pool não inicializado. Execute test_connection() para verificar.")
