"""
Script para aplicar migração de configurações de aparência
"""
import mysql.connector
from src.config.database import DatabaseConnection
from src.utils.logger import Logger

logger = Logger()

def aplicar_migracao():
    """Aplica a migração de aparência"""
    try:
        # Inicializa pool
        DatabaseConnection.initialize_pool()
        
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        logger.info("Aplicando migração de aparência...")
        
        # Lê o arquivo SQL
        with open('database/migrations/003_add_aparencia_config.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Separa os comandos
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for command in commands:
            if command:
                try:
                    cursor.execute(command)
                    logger.info(f"✓ Comando executado")
                except mysql.connector.Error as e:
                    if 'Duplicate column' in str(e):
                        logger.info(f"⚠ Coluna já existe, pulando...")
                    else:
                        logger.error(f"Erro: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✓ Migração aplicada com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao aplicar migração: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    aplicar_migracao()
