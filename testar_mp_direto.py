"""
Testa a API do Mercado Pago com o token do banco
"""
import requests
from src.services.config_service import config_service

print("=" * 60)
print("TESTE DE API - MERCADO PAGO")
print("=" * 60)

# Buscar token
access_token = config_service.get_mercadopago_access_token()

if not access_token:
    print("\n❌ Access token não configurado!")
    exit(1)

print(f"\n✓ Token encontrado: {access_token[:20]}...")

# Teste 1: Validar credenciais
print("\n1️⃣  TESTANDO CREDENCIAIS...")
print("Endpoint: GET /v1/users/me\n")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

try:
    # Tenta endpoint alternativo
    response = requests.get("https://api.mercadopago.com/users/me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Credenciais válidas!")
        print(f"  ID: {data.get('id')}")
        print(f"  Email: {data.get('email')}")
        print(f"  Nickname: {data.get('nickname')}")
    else:
        print(f"❌ Erro: Status {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)

# Teste 2: Criar pagamento PIX
print("\n2️⃣  TESTANDO CRIAÇÃO DE PAGAMENTO PIX...")
print("Endpoint: POST /v1/payments\n")

import time
payment_headers = headers.copy()
payment_headers["X-Idempotency-Key"] = f"TEST_{int(time.time() * 1000)}"

payment_data = {
    "transaction_amount": 0.01,
    "description": "Teste PDV - PIX",
    "payment_method_id": "pix",
    "payer": {
        "email": "teste@teste.com"
    }
}

try:
    response = requests.post(
        "https://api.mercadopago.com/v1/payments",
        headers=payment_headers,
        json=payment_data
    )
    
    if response.status_code == 201:
        data = response.json()
        print("✓ Pagamento PIX criado com sucesso!")
        print(f"  Payment ID: {data.get('id')}")
        print(f"  Status: {data.get('status')}")
        print(f"  Valor: R$ {data.get('transaction_amount')}")
        
        qr_code = data.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code')
        if qr_code:
            print(f"  QR Code: {qr_code[:50]}...")
            print("\n✅ API DO MERCADO PAGO FUNCIONANDO CORRETAMENTE!")
        else:
            print("  ⚠️  QR Code não retornado")
    else:
        print(f"❌ Erro: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
