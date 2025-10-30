"""
Script para testar integração PIX com Mercado Pago usando curl.
"""

import subprocess
import json
from datetime import datetime, timedelta

def test_pix_with_curl():
    """Testa criação de PIX usando curl."""
    
    print("=" * 80)
    print("TESTE DE PIX - MERCADO PAGO")
    print("=" * 80)
    
    # IMPORTANTE: Use TEST ACCESS TOKEN, não PRODUCTION!
    # Obtenha em: https://www.mercadopago.com.br/developers/panel/credentials
    # Seção: Credenciais de teste
    
    # Token de TESTE (SANDBOX) - SUBSTITUA pelo seu token de teste
    access_token = input("\n🔑 Cole aqui seu ACCESS TOKEN DE TESTE do Mercado Pago:\n> ").strip()
    
    if not access_token:
        print("❌ Token não fornecido!")
        return
    
    # Data de expiração
    expiration_date = datetime.now() + timedelta(minutes=15)
    date_str = expiration_date.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
    
    # Payload
    payload = {
        "transaction_amount": 10.50,
        "description": "Teste PDV - PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User"
        },
        "date_of_expiration": date_str
    }
    
    # Salva payload em arquivo temporário
    with open('payload_temp.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    
    print("\n📦 Payload:")
    print(json.dumps(payload, indent=2))
    
    # Comando curl
    curl_cmd = [
        'curl',
        '-X', 'POST',
        'https://api.mercadopago.com/v1/payments',
        '-H', f'Authorization: Bearer {access_token}',
        '-H', 'Content-Type: application/json',
        '-d', f'@payload_temp.json'
    ]
    
    print("\n🚀 Executando requisição...")
    print(f"\nComando curl:\n{' '.join(curl_cmd)}\n")
    
    try:
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            shell=True
        )
        
        print("=" * 80)
        print("📥 RESPOSTA:")
        print("=" * 80)
        
        if result.returncode == 0:
            try:
                response_json = json.loads(result.stdout)
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
                
                # Verifica se foi criado com sucesso
                if 'id' in response_json:
                    print("\n✅ PIX CRIADO COM SUCESSO!")
                    print(f"Payment ID: {response_json['id']}")
                    print(f"Status: {response_json.get('status')}")
                    
                    # Tenta obter QR Code
                    point_of_interaction = response_json.get('point_of_interaction', {})
                    transaction_data = point_of_interaction.get('transaction_data', {})
                    
                    qr_code = transaction_data.get('qr_code')
                    if qr_code:
                        print(f"\n📱 PIX Copia e Cola:")
                        print(qr_code[:50] + "...")
                    
                elif 'error' in response_json:
                    print(f"\n❌ ERRO: {response_json.get('message', 'Unknown error')}")
                    if 'cause' in response_json:
                        print("\nDetalhes:")
                        for cause in response_json['cause']:
                            print(f"  - {cause.get('description', '')}")
                
            except json.JSONDecodeError:
                print("Resposta não é JSON válido:")
                print(result.stdout)
        else:
            print("❌ Erro ao executar curl:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    finally:
        # Remove arquivo temporário
        import os
        if os.path.exists('payload_temp.json'):
            os.remove('payload_temp.json')
    
    print("\n" + "=" * 80)
    print("\n💡 DICAS:")
    print("1. Use TOKEN DE TESTE (não produção)")
    print("2. Obtenha em: https://www.mercadopago.com.br/developers/panel/credentials")
    print("3. Na seção 'Credenciais de teste'")
    print("4. Copie o 'Access Token'")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_pix_with_curl()
