import os
import sys
from decimal import Decimal

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.mercado_pago_service import mercado_pago_service
from src.utils.logger import Logger

def testar_geracao_pix_mp():
    """
    Testa a criação de um pagamento PIX e a obtenção do QR Code
    usando o MercadoPagoService.
    """
    print("Iniciando teste de integração com o PIX do Mercado Pago...")
    
    # Desabilita o logger para não poluir a saída do teste
    Logger.ATIVO = False
    
    # 1. Verificar se o token está configurado
    token = mercado_pago_service.access_token
    if not token:
        print("\n❌ ERRO: O access token do Mercado Pago não está configurado.")
        print("   - Execute o script 'configurar_mp.py' primeiro.")
        return
        
    print(f"🔑 Usando Access Token: ...{token[-10:]}")

    # 2. Tentar criar um pagamento PIX
    valor_teste = Decimal("0.01")
    descricao_teste = "Teste de Integracao PDV"
    
    print(f"\n1. Tentando criar um pagamento PIX de R$ {valor_teste}...")
    
    dados_pagamento = mercado_pago_service.criar_pagamento_pix(
        valor=valor_teste,
        descricao=descricao_teste
    )
    
    if not dados_pagamento:
        print("\n❌ FALHA: Não foi possível criar o pagamento PIX.")
        print("   - Verifique o log de erros em 'logs/erros.log' para mais detalhes.")
        print("   - Possíveis causas: token inválido, sem conexão com a internet.")
        return
        
    payment_id = dados_pagamento.get("id")
    print(f"   ✅ Sucesso! Pagamento criado com ID: {payment_id}")

    # 3. Tentar obter o QR Code
    print("\n2. Tentando obter o QR Code (Copia e Cola)...")
    
    dados_qr = mercado_pago_service.obter_qr_code_pix(dados_pagamento)
    
    if not dados_qr or not dados_qr.get("qr_code"):
        print("\n❌ FALHA: Não foi possível obter o QR Code do pagamento.")
        print("   - A resposta da API do Mercado Pago pode ter mudado.")
        return
        
    print("   ✅ Sucesso! QR Code obtido.")
    
    # 4. Exibir resultados
    print("\n" + "="*50)
    print("🎉 TESTE DE INTEGRAÇÃO CONCLUÍDO COM SUCESSO! 🎉")
    print("="*50)
    print(f"\nID do Pagamento: {dados_qr.get('payment_id')}")
    print("\nCódigo PIX (Copia e Cola):")
    print("-" * 30)
    print(dados_qr.get('qr_code'))
    print("-" * 30)
    
    # 5. Cancelar o pagamento criado para não deixar lixo
    print("\n3. Cancelando o pagamento de teste...")
    cancelado = mercado_pago_service.cancelar_pagamento(payment_id)
    if cancelado:
        print("   ✅ Pagamento de teste cancelado com sucesso.")
    else:
        print("   ⚠️ Não foi possível cancelar o pagamento de teste.")


if __name__ == "__main__":
    testar_geracao_pix_mp()
