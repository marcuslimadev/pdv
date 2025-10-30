# INSTRUÇÕES PARA HABILITAR PIX NO MERCADO PAGO

## 🚨 PROBLEMA ATUAL
Erro: "Collector user without key enabled for QR render"
Isso significa que o PIX não está habilitado na sua conta do Mercado Pago.

## ✅ SOLUÇÃO - PASSO A PASSO

### 1. Acesse o Painel do Mercado Pago
- Vá para: https://www.mercadopago.com.br/
- Faça login com sua conta

### 2. Habilite o PIX na sua Conta
- Clique em **"Vender online"** ou **"Integrar pagamentos"**
- Vá em **"Configurações"** → **"Contas digitais"** → **"PIX"**
- Clique em **"Ativar PIX"**

### 3. Configure os Dados Bancários
- Informe seus dados bancários
- Cadastre uma chave PIX (CPF, CNPJ, email ou telefone)
- Aguarde a validação (pode levar algumas horas)

### 4. Teste Novamente
Depois que o PIX estiver habilitado, o sistema funcionará perfeitamente.

## 🔧 CREDENCIAIS CONFIGURADAS
✅ Access Token: APP_USR-5277822483126127-102809-...
✅ Public Key: APP_USR-f078aa48-3dea-42f4-8827-...
✅ Client ID: 5277822483126127
✅ Client Secret: m2jmm278hgWUV4Tlhpc1bKLMEmQcQEnd

## 📱 COMO FUNCIONA DEPOIS DE HABILITADO
1. Pressione F4 no PDV
2. Sistema gera PIX via Mercado Pago
3. Mostra QR Code para o cliente
4. Cliente paga via PIX
5. Mercado Pago confirma pagamento automaticamente

## ⏰ TEMPO DE ATIVAÇÃO
- PIX pessoa física: Instantâneo
- PIX empresa (CNPJ): Até 2 dias úteis

## 🆘 SE CONTINUAR COM ERRO
Entre em contato com o suporte do Mercado Pago:
- https://www.mercadopago.com.br/ajuda
- Informe que quer habilitar PIX para integrações via API

---

**IMPORTANTE:** Não precisa alterar nada no código. Está tudo correto!
O problema é só a habilitação do PIX na conta do Mercado Pago.