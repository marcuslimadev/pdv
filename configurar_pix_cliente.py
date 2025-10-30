"""
Script para configurar a chave PIX do cliente no sistema.
Essa chave receberá 99% do valor das vendas via PIX Mercado Pago.
"""

import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.config_service import config_service, PIX_PLATAFORMA, PERCENTUAL_CLIENTE, PERCENTUAL_PLATAFORMA

def configurar_chave_pix_cliente():
    """
    Configura a chave PIX do cliente no banco de dados.
    """
    print("=" * 60)
    print("CONFIGURAÇÃO DA CHAVE PIX DO CLIENTE")
    print("=" * 60)
    print()
    print(f"⚠️  IMPORTANTE: O split de pagamento está configurado assim:")
    print(f"   • {PERCENTUAL_CLIENTE}% do valor vai para a CHAVE PIX DO CLIENTE")
    print(f"   • {PERCENTUAL_PLATAFORMA}% do valor vai para a CHAVE PIX DA PLATAFORMA")
    print()
    print(f"📱 Chave PIX da Plataforma (FIXA): {PIX_PLATAFORMA}")
    print()
    print("-" * 60)
    print()
    
    # Mostra a chave atual se existir
    chave_atual = config_service.get_pix_chave_cliente()
    if chave_atual:
        print(f"✓ Chave PIX do Cliente atual: {chave_atual}")
        print()
        resposta = input("Deseja alterar? (S/N): ").strip().upper()
        if resposta != 'S':
            print("\nOperação cancelada.")
            return
        print()
    
    # Solicita nova chave
    print("Digite a CHAVE PIX do CLIENTE:")
    print("(Pode ser CPF, CNPJ, Email, Telefone ou Chave Aleatória)")
    print()
    nova_chave = input("Chave PIX: ").strip()
    
    if not nova_chave:
        print("\n❌ Erro: Chave PIX não pode estar vazia!")
        return
    
    # Confirma
    print()
    print("-" * 60)
    print("CONFIRMAÇÃO:")
    print(f"  Chave PIX do Cliente: {nova_chave}")
    print(f"  Receberá: {PERCENTUAL_CLIENTE}% das vendas PIX")
    print("-" * 60)
    print()
    
    confirmacao = input("Confirma a configuração? (S/N): ").strip().upper()
    
    if confirmacao != 'S':
        print("\nOperação cancelada.")
        return
    
    try:
        # Salva no banco de dados
        config_service.set_pix_chave_cliente(nova_chave)
        
        # Verifica se salvou corretamente
        chave_salva = config_service.get_pix_chave_cliente()
        
        if chave_salva == nova_chave:
            print()
            print("=" * 60)
            print("✅ SUCESSO! Chave PIX do Cliente configurada!")
            print("=" * 60)
            print()
            print("📊 RESUMO DA CONFIGURAÇÃO:")
            print(f"   • Chave PIX Cliente: {chave_salva}")
            print(f"   • Percentual Cliente: {PERCENTUAL_CLIENTE}%")
            print()
            print(f"   • Chave PIX Plataforma: {PIX_PLATAFORMA}")
            print(f"   • Percentual Plataforma: {PERCENTUAL_PLATAFORMA}%")
            print()
            print("⚡ O split automático já está ativo!")
            print("   Todas as vendas via PIX Mercado Pago dividirão")
            print(f"   automaticamente {PERCENTUAL_CLIENTE}% para o cliente e {PERCENTUAL_PLATAFORMA}% para a plataforma.")
            print()
        else:
            print("\n❌ Erro: A chave salva não corresponde à chave informada.")
            print(f"   Esperado: {nova_chave}")
            print(f"   Salvo: {chave_salva}")
    
    except Exception as e:
        print(f"\n❌ Erro ao configurar chave PIX: {e}")
        print("   Verifique se o banco de dados está acessível.")

if __name__ == "__main__":
    configurar_chave_pix_cliente()
