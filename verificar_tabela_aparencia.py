"""
Verifica se a tabela aparencia_config existe no banco
"""
import mysql.connector
from src.config.database import DatabaseConnection

def verificar_tabela():
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    
    print("Verificando tabelas no banco pdv_sistema...")
    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    
    print("\nTabelas encontradas:")
    for tabela in tabelas:
        print(f"  - {tabela[0]}")
    
    print("\n" + "="*60)
    if any('aparencia_config' in str(t) for t in tabelas):
        print("✓ Tabela aparencia_config EXISTE")
        
        # Mostra estrutura
        cursor.execute("DESCRIBE aparencia_config")
        print("\nEstrutura da tabela:")
        for col in cursor.fetchall():
            print(f"  {col[0]}: {col[1]}")
            
        # Mostra dados
        cursor.execute("SELECT * FROM aparencia_config")
        dados = cursor.fetchall()
        print(f"\nRegistros: {len(dados)}")
    else:
        print("✗ Tabela aparencia_config NÃO EXISTE")
        print("\nVou tentar criar agora...")
        
        try:
            with open('database/migrations/003_add_aparencia_config.sql', 'r', encoding='utf-8') as f:
                sql = f.read()
            
            # Remove comentários e quebra por ;
            commands = []
            for line in sql.split('\n'):
                if line.strip() and not line.strip().startswith('--'):
                    commands.append(line)
            
            sql_clean = '\n'.join(commands)
            
            for cmd in sql_clean.split(';'):
                cmd = cmd.strip()
                if cmd and 'USE' not in cmd:  # Pula o USE database
                    print(f"\nExecutando: {cmd[:50]}...")
                    cursor.execute(cmd)
            
            conn.commit()
            print("\n✓ Tabela criada com sucesso!")
            
        except Exception as e:
            print(f"\n✗ Erro ao criar tabela: {e}")
            import traceback
            traceback.print_exc()
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    verificar_tabela()
