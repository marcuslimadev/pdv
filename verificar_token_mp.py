"""
Verifica se o access token do Mercado Pago está configurado no banco
"""
from src.services.config_service import config_service

print("=" * 60)
print("VERIFICAÇÃO DE CONFIGURAÇÃO - MERCADO PAGO")
print("=" * 60)

# Buscar access token
access_token = config_service.get_mercadopago_access_token()

print(f"\nAccess Token no banco: ", end="")
if access_token:
    # Mostra apenas os primeiros 20 caracteres por segurança
    print(f"✓ Configurado ({access_token[:20]}...)")
    print(f"  Tamanho: {len(access_token)} caracteres")
else:
    print("✗ NÃO CONFIGURADO")
    print("\nPara configurar, execute:")
    print("  python configurar_mp.py")

print("\n" + "=" * 60)
