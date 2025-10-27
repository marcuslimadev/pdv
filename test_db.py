import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES LIKE "pdv_system"')
    result = cursor.fetchone()
    
    if result:
        print("✓ Banco 'pdv_system' existe!")
    else:
        print("✗ Banco 'pdv_system' NÃO existe - executando schema.sql...")
        
        # Cria o banco
        cursor.execute('CREATE DATABASE IF NOT EXISTS pdv_system')
        cursor.execute('USE pdv_system')
        
        # Lê e executa o schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
            
        # Executa cada comando separadamente
        for statement in schema.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("✓ Banco criado com sucesso!")
    
    conn.close()
    print("\n✓ MySQL está funcionando corretamente!")
    
except Exception as e:
    print(f"✗ Erro: {e}")
