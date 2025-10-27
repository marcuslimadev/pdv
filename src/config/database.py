"""
Módulo de configuração do banco de dados MySQL.
"""

import mysql.connector
from mysql.connector import pooling, Error
from contextlib import contextmanager


class DatabaseConfig:
    """Configuração centralizada do banco de dados."""
    
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = ''
    DATABASE = 'pdv_sistema'
    POOL_NAME = 'pdv_pool'
    POOL_SIZE = 5


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
                    pool_size=DatabaseConfig.POOL_SIZE,
                    pool_reset_session=True,
                    host=DatabaseConfig.HOST,
                    user=DatabaseConfig.USER,
                    password=DatabaseConfig.PASSWORD,
                    database=DatabaseConfig.DATABASE,
                    charset='utf8mb4',
                    collation='utf8mb4_unicode_ci',
                    autocommit=False
                )
                print(f"✓ Pool de conexões criado com sucesso ({DatabaseConfig.POOL_SIZE} conexões)")
            except Error as e:
                print(f"✗ Erro ao criar pool de conexões: {e}")
                raise
    
    @classmethod
    def get_connection(cls):
        """Obtém uma conexão do pool."""
        if cls._pool is None:
            cls.initialize_pool()
        
        try:
            connection = cls._pool.get_connection()
            return connection
        except Error as e:
            print(f"✗ Erro ao obter conexão: {e}")
            raise
    
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
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=dictionary)
        
        try:
            yield cursor
            connection.commit()
        except Error as e:
            connection.rollback()
            print(f"✗ Erro na transação: {e}")
            raise
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def test_connection(cls):
        """Testa a conexão com o banco de dados."""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE
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
