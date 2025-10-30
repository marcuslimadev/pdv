"""
Script de teste para verificar o split de pagamento PIX.
Testa a divisão de 99% para o cliente e 1% para a plataforma.
"""

import os
import sys
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.mercado_pago_service import mercado_pago_service
from src.services.config_service import config_service, PIX_PLATAFORMA, PERCENTUAL_CLIENTE, PERCENTUAL_PLATAFORMA
from src.utils.logger import Logger

def testar_split_pix():
    """
    Testa a criação de um pagamento PIX com split.
    """
    print("=" * 70)
    print("TESTE DE SPLIT DE PAGAMENTO PIX - MERCADO PAGO")
    print("=" * 70)
    print()
    
    # Desabilita logger para não poluir a saída
    Logger.ATIVO = False
    
    # 1. Verifica configurações
    print("1. Verificando configurações...")
    print()
    
    token = mercado_pago_service.access_token
    if not token:
        print("❌ ERRO: Token do Mercado Pago não configurado!")
        print("   Execute: python configurar_mp.py")
        return
    
    print(f"   ✓ Token Mercado Pago: ...{token[-10:]}")
    
    chave_pix_cliente = config_service.get_pix_chave_cliente()
    if not chave_pix_cliente:
        print("   ⚠️  AVISO: Chave PIX do cliente não configurada!")
        print("      O split NÃO será aplicado neste teste.")
        print("      Execute: python configurar_pix_cliente.py")
        print()
        resposta = input("   Continuar mesmo assim? (S/N): ").strip().upper()
        if resposta != 'S':
            return
    else:
        print(f"   ✓ Chave PIX Cliente: {chave_pix_cliente}")
    
    print(f"   ✓ Chave PIX Plataforma: {PIX_PLATAFORMA}")
    print(f"   ✓ Percentuais: {PERCENTUAL_CLIENTE}% Cliente / {PERCENTUAL_PLATAFORMA}% Plataforma")
    print()
    
    # 2. Solicita valor do teste
    print("2. Valor para teste (ou ENTER para R$ 10,00):")
    valor_input = input("   R$ ").strip()
    
    if not valor_input:
        valor = Decimal("10.00")
    else:
        try:
            valor = Decimal(valor_input.replace(",", "."))
        except:
            print("   ❌ Valor inválido! Usando R$ 10,00")
            valor = Decimal("10.00")
    
    print()
    print(f"   Valor do teste: R$ {valor:.2f}")
    print()
    
    # 3. Calcula o split
    print("3. Calculando split de valores...")
    valor_float = float(valor)
    valor_plataforma = round(valor_float * (PERCENTUAL_PLATAFORMA / 100), 2)
    valor_cliente = round(valor_float - valor_plataforma, 2)
    
    print()
    print("   DIVISÃO DO PAGAMENTO:")
    print(f"   ├─ Total da venda: R$ {valor_float:.2f}")
    print(f"   ├─ Cliente ({PERCENTUAL_CLIENTE}%): R$ {valor_cliente:.2f}")
    print(f"   └─ Plataforma ({PERCENTUAL_PLATAFORMA}%): R$ {valor_plataforma:.2f}")
    print()
    
    # 4. Cria o pagamento
    print("4. Criando pagamento PIX no Mercado Pago...")
    print()
    
    dados_pagamento = mercado_pago_service.criar_pagamento_pix(
        valor=valor,
        descricao="Teste de Split PIX - PDV"
    )
    
    if not dados_pagamento:
        print("   ❌ FALHA ao criar pagamento PIX!")
        print("   Verifique os logs em 'logs/' para mais detalhes.")
        return
    
    payment_id = dados_pagamento.get("id")
    print(f"   ✅ Pagamento criado! ID: {payment_id}")
    print()
    
    # 5. Verifica metadata
    print("5. Verificando metadata do pagamento...")
    metadata = dados_pagamento.get("metadata", {})
    
    if metadata:
        print()
        print("   METADATA DO PAGAMENTO:")
        for key, value in metadata.items():
            print(f"   • {key}: {value}")
        print()
        
        # Verifica se o split foi aplicado
        if "split_cliente" in metadata:
            print("   ✅ SPLIT CONFIGURADO COM SUCESSO!")
            print(f"   • Cliente receberá: R$ {metadata['split_cliente']}")
            print(f"   • Plataforma receberá: R$ {metadata['split_plataforma']}")
        else:
            print("   ⚠️  Split NÃO foi aplicado")
            print("   • Motivo:", metadata.get("motivo", "Desconhecido"))
    else:
        print("   ⚠️  Nenhuma metadata encontrada")
    
    print()
    
    # 6. Obtém QR Code
    print("6. Obtendo QR Code...")
    dados_qr = mercado_pago_service.obter_qr_code_pix(dados_pagamento)
    
    if dados_qr and dados_qr.get("qr_code"):
        print("   ✅ QR Code obtido com sucesso!")
        print()
        print("   " + "-" * 60)
        print("   PIX Copia e Cola:")
        print("   " + "-" * 60)
        print(f"   {dados_qr['qr_code'][:80]}...")
        print("   " + "-" * 60)
    else:
        print("   ❌ Não foi possível obter o QR Code")
    
    print()
    
    # 7. Cancela o pagamento
    print("7. Cancelando pagamento de teste...")
    cancelado = mercado_pago_service.cancelar_pagamento(payment_id)
    
    if cancelado:
        print("   ✅ Pagamento cancelado com sucesso!")
    else:
        print("   ⚠️  Não foi possível cancelar o pagamento")
    
    print()
    print("=" * 70)
    print("TESTE CONCLUÍDO!")
    print("=" * 70)
    print()
    
    if chave_pix_cliente and "split_cliente" in metadata:
        print("✅ O split de pagamento está FUNCIONANDO corretamente!")
        print(f"   • Todas as vendas PIX dividirão {PERCENTUAL_CLIENTE}%/{PERCENTUAL_PLATAFORMA}%")
    elif not chave_pix_cliente:
        print("⚠️  Para ativar o split, configure a chave PIX do cliente:")
        print("   python configurar_pix_cliente.py")
    else:
        print("❌ O split NÃO está funcionando. Verifique os logs.")
    
    print()

if __name__ == "__main__":
    testar_split_pix()
