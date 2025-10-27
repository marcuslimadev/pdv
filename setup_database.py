"""
Script para criar o banco de dados PDV.
"""
import mysql.connector
import re

def executar_schema():
    """Cria o banco de dados e tabelas."""
    try:
        # Conecta ao MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        
        print("✓ Conectado ao MySQL")
        
        # Cria o banco
        cursor.execute('CREATE DATABASE IF NOT EXISTS pdv_system')
        cursor.execute('USE pdv_system')
        print("✓ Banco de dados 'pdv_system' criado/selecionado")
        
        # Lê o schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
        
        # Remove comentários
        schema = re.sub(r'--.*$', '', schema, flags=re.MULTILINE)
        
        # Processa DELIMITER (remove triggers por enquanto para simplificar)
        # Separa em partes antes e depois dos triggers
        partes = schema.split('DELIMITER')
        
        # Executa a primeira parte (CREATE TABLEs)
        parte_tabelas = partes[0]
        statements = [s.strip() for s in parte_tabelas.split(';') if s.strip()]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"✓ Executado: {statement[:50]}...")
                except Exception as e:
                    print(f"✗ Erro ao executar: {statement[:50]}...")
                    print(f"  Erro: {e}")
        
        conn.commit()
        print("\n✓ Tabelas criadas com sucesso!")
        
        # Cria usuário admin padrão
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios WHERE username = 'admin'
        """)
        
        if cursor.fetchone()[0] == 0:
            import bcrypt
            senha_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
                VALUES ('admin', %s, 'Administrador', 'admin', 1)
            """, (senha_hash,))
            
            conn.commit()
            print("✓ Usuário admin criado (username: admin, senha: admin123)")
        else:
            print("✓ Usuário admin já existe")
        
        # Cria algumas categorias de exemplo
        cursor.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            categorias = [
                ('Bebidas', 'Refrigerantes, sucos, águas'),
                ('Alimentos', 'Comidas em geral'),
                ('Limpeza', 'Produtos de limpeza'),
                ('Higiene', 'Produtos de higiene pessoal'),
            ]
            
            for nome, desc in categorias:
                cursor.execute("""
                    INSERT INTO categorias (nome, descricao, ativo)
                    VALUES (%s, %s, 1)
                """, (nome, desc))
            
            conn.commit()
            print("✓ Categorias de exemplo criadas")
        
        conn.close()
        print("\n✅ BANCO DE DADOS CONFIGURADO COM SUCESSO!")
        print("\n📝 Credenciais de acesso:")
        print("   Username: admin")
        print("   Senha: admin123")
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    executar_schema()
