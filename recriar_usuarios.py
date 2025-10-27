"""
Script para recriar os usuários com senhas corretas.
"""

import sys
sys.path.insert(0, 'src')

import mysql.connector
from src.models.usuario import Usuario

def recriar_usuarios():
    """Recria os usuários com senhas corretas."""
    try:
        # Conecta diretamente ao banco
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pdv_sistema'
        )
        cursor = conn.cursor()
        
        print("=== RECRIANDO USUÁRIOS ===")
        
        # Remove usuários existentes
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        print("✓ Usuários antigos removidos")
        
        # Cria hash das senhas usando a função do modelo
        admin_hash = Usuario.hash_senha('admin123')
        operador_hash = Usuario.hash_senha('operador123')
        
        print(f"Admin hash: {admin_hash}")
        print(f"Operador hash: {operador_hash}")
        
        # Insere usuário admin
        cursor.execute("""
            INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
            VALUES (%s, %s, %s, %s, %s)
        """, ('admin', admin_hash, 'Administrador', 'admin', True))
        
        # Insere usuário operador
        cursor.execute("""
            INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo)
            VALUES (%s, %s, %s, %s, %s)
        """, ('operador', operador_hash, 'Operador de Caixa', 'operador', True))
        
        conn.commit()
        print("✓ Usuários criados com sucesso!")
        
        # Testa as senhas
        print("\n=== TESTANDO SENHAS ===")
        
        # Busca o admin
        cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        admin_data = cursor.fetchone()
        if admin_data:
            # Converte para dicionário
            admin_dict = {
                'id': admin_data[0],
                'username': admin_data[1],
                'senha_hash': admin_data[2],
                'nome_completo': admin_data[3],
                'tipo': admin_data[4],
                'ativo': admin_data[5],
                'data_cadastro': admin_data[6],
                'ultimo_acesso': admin_data[7]
            }
            
            admin_obj = Usuario.from_dict(admin_dict)
            
            if admin_obj.verificar_senha('admin123'):
                print("✓ Senha do admin está funcionando!")
            else:
                print("✗ Senha do admin NÃO está funcionando!")
        
        # Busca o operador
        cursor.execute("SELECT * FROM usuarios WHERE username = 'operador'")
        operador_data = cursor.fetchone()
        if operador_data:
            # Converte para dicionário
            operador_dict = {
                'id': operador_data[0],
                'username': operador_data[1],
                'senha_hash': operador_data[2],
                'nome_completo': operador_data[3],
                'tipo': operador_data[4],
                'ativo': operador_data[5],
                'data_cadastro': operador_data[6],
                'ultimo_acesso': operador_data[7]
            }
            
            operador_obj = Usuario.from_dict(operador_dict)
            
            if operador_obj.verificar_senha('operador123'):
                print("✓ Senha do operador está funcionando!")
            else:
                print("✗ Senha do operador NÃO está funcionando!")
        
        cursor.close()
        conn.close()
        
        print("\n✅ USUÁRIOS RECRIADOS COM SUCESSO!")
        print("\n📝 Credenciais:")
        print("   Admin - Username: admin, Senha: admin123")
        print("   Operador - Username: operador, Senha: operador123")
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recriar_usuarios()