"""
Menu interativo para testar PIX do Mercado Pago.
"""

import sys
import subprocess

def main_menu():
    """Menu principal."""
    while True:
        print("\n" + "=" * 80)
        print(" 🧪 TESTE DE PIX - MERCADO PAGO")
        print("=" * 80)
        print("\nEscolha uma opção:")
        print("\n1. 🔑 Configurar Access Token no Sistema")
        print("2. 🧪 Testar PIX com Python (test_pix_simple.py)")
        print("3. 🧪 Testar PIX com PowerShell (test_pix.ps1)")
        print("4. 📖 Ver documentação (PIX_TROUBLESHOOTING.md)")
        print("5. ❌ Sair")
        
        choice = input("\n👉 Digite sua escolha (1-5): ").strip()
        
        if choice == "1":
            configure_token()
        elif choice == "2":
            test_with_python()
        elif choice == "3":
            test_with_powershell()
        elif choice == "4":
            show_docs()
        elif choice == "5":
            print("\n👋 Até logo!\n")
            break
        else:
            print("\n❌ Opção inválida!")


def configure_token():
    """Configura o access token."""
    print("\n" + "=" * 80)
    print(" 🔑 CONFIGURAR ACCESS TOKEN")
    print("=" * 80)
    
    print("\n📝 PASSO A PASSO:")
    print("1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials")
    print("2. Clique em 'Credenciais de teste' (para desenvolvimento)")
    print("3. Copie o 'Access token' (começa com TEST-)")
    
    token = input("\n👉 Cole o token aqui (ou ENTER para cancelar): ").strip()
    
    if not token:
        print("\n❌ Cancelado!")
        return
    
    if not token.startswith("TEST-") and not token.startswith("APP_USR-"):
        print("\n⚠️  AVISO: Token não parece válido (deve começar com TEST- ou APP_USR-)")
        confirma = input("Continuar mesmo assim? (s/n): ").strip().lower()
        if confirma != 's':
            print("\n❌ Cancelado!")
            return
    
    try:
        from src.services.config_service import config_service
        config_service.set_mercadopago_access_token(token)
        print("\n✅ Token configurado com sucesso!")
        print(f"Token salvo: {token[:20]}...")
        
    except Exception as e:
        print(f"\n❌ Erro ao configurar: {str(e)}")


def test_with_python():
    """Testa com Python."""
    print("\n" + "=" * 80)
    print(" 🐍 TESTE COM PYTHON")
    print("=" * 80)
    
    print("\n1. Primeiro, edite o arquivo: test_pix_simple.py")
    print("2. Substitua ACCESS_TOKEN = 'TEST-YOUR-ACCESS-TOKEN-HERE'")
    print("3. Cole seu token de teste do Mercado Pago")
    
    confirma = input("\nJá editou o arquivo? (s/n): ").strip().lower()
    
    if confirma == 's':
        print("\n🚀 Executando teste...\n")
        subprocess.run([sys.executable, "test_pix_simple.py"])
    else:
        print("\n📝 Edite primeiro, depois volte aqui!")


def test_with_powershell():
    """Testa com PowerShell."""
    print("\n" + "=" * 80)
    print(" 💻 TESTE COM POWERSHELL")
    print("=" * 80)
    
    print("\n1. Primeiro, edite o arquivo: test_pix.ps1")
    print("2. Substitua $ACCESS_TOKEN = 'TEST-YOUR-ACCESS-TOKEN-HERE'")
    print("3. Cole seu token de teste do Mercado Pago")
    
    confirma = input("\nJá editou o arquivo? (s/n): ").strip().lower()
    
    if confirma == 's':
        print("\n🚀 Executando teste...\n")
        subprocess.run(["pwsh.exe", "-File", "test_pix.ps1"])
    else:
        print("\n📝 Edite primeiro, depois volte aqui!")


def show_docs():
    """Mostra documentação."""
    print("\n" + "=" * 80)
    print(" 📖 DOCUMENTAÇÃO")
    print("=" * 80)
    
    try:
        with open("PIX_TROUBLESHOOTING.md", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("\n❌ Arquivo PIX_TROUBLESHOOTING.md não encontrado!")
    
    input("\nPressione ENTER para voltar...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!\n")
