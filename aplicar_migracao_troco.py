"""
Script para aplicar migração: adicionar campos valor_pago e troco
"""

import mysql.connector
from src.config.database import DatabaseConnection

def aplicar_migracao():
    """Aplica a migração 001 - adicionar campos de troco."""
    
    # SQL da migração
    sqls = [
        """
        ALTER TABLE pagamentos 
        ADD COLUMN valor_pago DECIMAL(10,2) NULL AFTER dados_pix
        """,
        """
        ALTER TABLE pagamentos 
        ADD COLUMN troco DECIMAL(10,2) DEFAULT 0.00 AFTER valor_pago
        """,
        """
        UPDATE pagamentos 
        SET valor_pago = valor, troco = 0.00 
        WHERE valor_pago IS NULL
        """
    ]
    
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        print("Iniciando migração 001...")
        
        for i, sql in enumerate(sqls, 1):
            try:
                cursor.execute(sql)
                conn.commit()
                print(f"✓ Passo {i}/{len(sqls)} executado com sucesso")
            except mysql.connector.Error as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠ Passo {i}/{len(sqls)} - Coluna já existe (pulando)")
                else:
                    raise
        
        # Verificação
        cursor.execute("""
            SELECT COUNT(*) as total_pagamentos, 
                   COUNT(valor_pago) as com_valor_pago,
                   COUNT(troco) as com_troco
            FROM pagamentos
        """)
        
        resultado = cursor.fetchone()
        print("\n✓ Migração 001 aplicada com sucesso!")
        print(f"Total de pagamentos: {resultado[0]}")
        print(f"Com valor_pago: {resultado[1]}")
        print(f"Com troco: {resultado[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Erro ao aplicar migração: {e}")
        raise

if __name__ == "__main__":
    aplicar_migracao()
