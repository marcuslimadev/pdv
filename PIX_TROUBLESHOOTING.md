# PROBLEMA COM PIX DO MERCADO PAGO

## ❌ Erro Atual
```
"Unauthorized use of live credentials"
Status: 401
```

## 🔍 Causa
Você está usando **credenciais de PRODUÇÃO** em um ambiente que o Mercado Pago considera como "teste". Isso é bloqueado por segurança.

## ✅ Soluções

### Opção 1: Usar Credenciais de TESTE (Recomendado para desenvolvimento)

1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials
2. Clique na aba **"Credenciais de teste"**
3. Copie o **"Access token"** (começa com `TEST-`)
4. Configure no sistema:

```python
# Método 1: Via banco de dados
python -c "from src.services.config_service import config_service; config_service.set_mercadopago_access_token('TEST-SEU-TOKEN-AQUI')"

# Método 2: Via SQL direto
INSERT INTO configuracoes_sistema (chave, valor, descricao)
VALUES ('mercadopago_access_token', 'TEST-SEU-TOKEN-AQUI', 'Access Token Mercado Pago')
ON DUPLICATE KEY UPDATE valor = 'TEST-SEU-TOKEN-AQUI';
```

### Opção 2: Usar Credenciais de PRODUÇÃO (Quando for PRD)

Se você realmente quer usar produção:

1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials
2. Clique na aba **"Credenciais de produção"**
3. Copie o **"Access token"** (começa com `APP_USR-`)
4. Configure no sistema (igual acima)

**IMPORTANTE:** Credenciais de produção só funcionam:
- Em domínios autorizados
- Com aplicação homologada
- Em produção real (não localhost)

### Opção 3: Testar PIX Direto (sem Mercado Pago)

Use PIX estático com QR Code gerado localmente (já implementado no sistema):

```python
# No venda_window.py, use processar_pix() em vez de processar_pix_mercado_pago()
```

## 🧪 Como Testar

### Teste 1: PowerShell Script
```powershell
# Edite test_pix.ps1 e coloque seu token de teste
# Depois execute:
.\test_pix.ps1
```

### Teste 2: Python Script
```bash
# Edite test_pix_simple.py e coloque seu token de teste
python test_pix_simple.py
```

### Teste 3: Curl Direto
```powershell
$token = "TEST-SEU-TOKEN-AQUI"
$date = (Get-Date).AddMinutes(15).ToString("yyyy-MM-ddTHH:mm:ss.000-03:00")

$body = @"
{
  "transaction_amount": 10.50,
  "description": "Teste PIX",
  "payment_method_id": "pix",
  "payer": { "email": "test@test.com" },
  "date_of_expiration": "$date"
}
"@

Invoke-RestMethod `
  -Uri "https://api.mercadopago.com/v1/payments" `
  -Method Post `
  -Headers @{"Authorization"="Bearer $token"; "Content-Type"="application/json"} `
  -Body $body
```

## 📚 Documentação Oficial
- https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-test
- https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/test-accounts

## 🎯 Próximos Passos

1. **Obtenha credenciais de teste**
2. **Configure no sistema** (via banco ou script)
3. **Teste** usando um dos scripts acima
4. **Valide** que retorna status 201 com QR Code
5. **Integre** no PDV quando funcionar

---

**Nota:** O sistema PDV está funcionando corretamente. O problema é apenas a configuração das credenciais do Mercado Pago.
