"""
Teste simples de PIX com Mercado Pago.
IMPORTANTE: Use credenciais de TESTE, não produção!
"""

import requests
import json
from datetime import datetime, timedelta

# ===================================================================
# CONFIGURE AQUI SEU ACCESS TOKEN DE TESTE
# Obtenha em: https://www.mercadopago.com.br/developers/panel/credentials
# Use a seção: "Credenciais de teste" (não "Produção")
# ===================================================================
ACCESS_TOKEN = "TEST-YOUR-ACCESS-TOKEN-HERE"  # SUBSTITUA!

def test_create_pix():
    """Testa criação de pagamento PIX."""
    
    url = "https://api.mercadopago.com/v1/payments"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Data de expiração
    expiration_date = datetime.now() + timedelta(minutes=15)
    date_str = expiration_date.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
    
    # Payload
    payload = {
        "transaction_amount": 10.50,
        "description": "Teste PDV - PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "test_user_123456@testuser.com"  # Email de teste
        },
        "date_of_expiration": date_str
    }
    
    print("=" * 80)
    print("TESTE DE CRIAÇÃO DE PIX - MERCADO PAGO")
    print("=" * 80)
    print("\n📦 Enviando payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("\n🚀 Fazendo requisição...\n")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print("\n📥 Resposta:")
        print("=" * 80)
        
        response_data = response.json()
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        
        if response.status_code == 201:
            print("\n✅ PIX CRIADO COM SUCESSO!")
            print(f"Payment ID: {response_data['id']}")
            print(f"Status: {response_data.get('status')}")
            
            # QR Code
            point_of_interaction = response_data.get('point_of_interaction', {})
            transaction_data = point_of_interaction.get('transaction_data', {})
            qr_code = transaction_data.get('qr_code')
            
            if qr_code:
                print(f"\n📱 PIX Copia e Cola (primeiros 100 chars):")
                print(qr_code[:100] + "...")
                
        elif response.status_code == 401:
            print("\n❌ ERRO DE AUTENTICAÇÃO!")
            print("Verifique se você está usando TOKEN DE TESTE (não produção)")
            print("Acesse: https://www.mercadopago.com.br/developers/panel/credentials")
            
        else:
            print(f"\n❌ ERRO {response.status_code}")
            if 'message' in response_data:
                print(f"Mensagem: {response_data['message']}")
            if 'cause' in response_data:
                print("Causas:")
                for cause in response_data['cause']:
                    print(f"  - {cause.get('description', '')}")
        
    except Exception as e:
        print(f"\n❌ Exceção: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    if ACCESS_TOKEN == "TEST-YOUR-ACCESS-TOKEN-HERE":
        print("\n⚠️  VOCÊ PRECISA CONFIGURAR O ACCESS TOKEN DE TESTE!")
        print("\n1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials")
        print("2. Vá em 'Credenciais de teste'")
        print("3. Copie o 'Access token'")
        print("4. Cole na variável ACCESS_TOKEN no arquivo test_pix_simple.py")
        print("\n" + "=" * 80)
    else:
        test_create_pix()
