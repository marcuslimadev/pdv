"""
Script para aplicar migração: criar tabela estornos
"""

import mysql.connector

def aplicar_migracao():
    """Aplica a migração 002 - criar tabela estornos."""
    
    sql = """
    CREATE TABLE IF NOT EXISTS estornos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        venda_id INT NOT NULL,
        usuario_id INT NOT NULL COMMENT 'Admin que autorizou o estorno',
        data_estorno DATETIME DEFAULT CURRENT_TIMESTAMP,
        motivo TEXT NOT NULL,
        valor_estornado DECIMAL(10,2) NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        INDEX idx_venda (venda_id),
        INDEX idx_usuario (usuario_id),
        INDEX idx_data (data_estorno)
    ) ENGINE=InnoDB COMMENT='Registros de estornos de vendas'
    """
    
    try:
        # Conecta direto ao MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pdv_sistema'
        )
        cursor = conn.cursor()
        
        print("Iniciando migração 002...")
        
        cursor.execute(sql)
        conn.commit()
        print("✓ Tabela 'estornos' criada com sucesso")
        
        # Verificação
        cursor.execute("SHOW CREATE TABLE estornos")
        resultado = cursor.fetchone()
        print("\n✓ Migração 002 aplicada com sucesso!")
        print(f"Tabela criada: estornos")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        if "already exists" in str(e).lower():
            print("⚠ Tabela 'estornos' já existe (pulando)")
        else:
            print(f"✗ Erro ao aplicar migração: {e}")
            raise
    except Exception as e:
        print(f"✗ Erro ao aplicar migração: {e}")
        raise

if __name__ == "__main__":
    aplicar_migracao()
