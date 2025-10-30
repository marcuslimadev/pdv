import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
# Isso permite que o script encontre os módulos da aplicação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.config_service import config_service

def configurar_token_mercado_pago():
    """
    Configura o access token do Mercado Pago no banco de dados.
    """
    novo_token = "APP_USR-5277822483126127-102809-a09cb83773553fe2d363c5ed29d26d78-223753899"
    
    try:
        print(f"Tentando configurar o novo token do Mercado Pago...")
        config_service.set_mercadopago_access_token(novo_token)
        
        print("Verificando se o token foi salvo corretamente...")
        token_salvo = config_service.get_mercadopago_access_token()
        
        if token_salvo == novo_token:
            print("\n✅ Sucesso! O access token do Mercado Pago foi configurado no sistema.")
            print("A integração com o PIX dinâmico do Mercado Pago deve funcionar agora.")
        else:
            print("\n❌ Erro: O token salvo não corresponde ao token fornecido.")
            print(f"   - Esperado: {novo_token}")
            print(f"   - Encontrado: {token_salvo}")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao tentar configurar o token: {e}")
        print("   - Verifique se o banco de dados está em execução e acessível.")
        print("   - Tente executar o 'setup_database.py' se for a primeira vez.")

if __name__ == "__main__":
    configurar_token_mercado_pago()
