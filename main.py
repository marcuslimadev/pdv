"""
Ponto de entrada do Sistema PDV.
"""

import sys
import tkinter as tk
from tkinter import messagebox

# Adiciona o diretório src ao path
sys.path.insert(0, 'src')

from src.config.database import DatabaseConnection
from src.ui.login_window import LoginWindow
from src.utils.logger import Logger


def main():
    """Função principal."""
    try:
        # Testa conexão com banco de dados
        print("=" * 60)
        print(" Sistema PDV - Inicialização")
        print("=" * 60)
        
        if not DatabaseConnection.test_connection():
            messagebox.showerror(
                "Erro de Conexão",
                "Não foi possível conectar ao banco de dados MySQL.\n\n"
                "Verifique se:\n"
                "1. O MySQL está rodando\n"
                "2. O banco 'pdv_sistema' existe\n"
                "3. As credenciais estão corretas (root sem senha)\n\n"
                "Execute: mysql -u root < database/schema.sql"
            )
            return
        
        Logger.log_operacao("Sistema", "INICIALIZAÇÃO", "Sistema PDV iniciado")
        
        # Cria e exibe janela de login
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        login_window = LoginWindow(root)
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
        Logger.log_operacao("Sistema", "ENCERRAMENTO", "Sistema encerrado")
    except Exception as e:
        Logger.log_erro("MAIN", e)
        messagebox.showerror("Erro Fatal", f"Erro fatal no sistema:\n{str(e)}")


if __name__ == "__main__":
    main()
