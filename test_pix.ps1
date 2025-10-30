# Script PowerShell para testar PIX com Mercado Pago
# IMPORTANTE: Use credenciais de TESTE!

# ===================================================================
# CONFIGURE AQUI SEU ACCESS TOKEN DE TESTE
# Obtenha em: https://www.mercadopago.com.br/developers/panel/credentials
# Use a seção: "Credenciais de teste"
# ===================================================================
$ACCESS_TOKEN = "TEST-YOUR-ACCESS-TOKEN-HERE"

if ($ACCESS_TOKEN -eq "TEST-YOUR-ACCESS-TOKEN-HERE") {
    Write-Host "`n⚠️  VOCÊ PRECISA CONFIGURAR O ACCESS TOKEN DE TESTE!" -ForegroundColor Yellow
    Write-Host "`n1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials" -ForegroundColor Cyan
    Write-Host "2. Vá em 'Credenciais de teste'" -ForegroundColor Cyan
    Write-Host "3. Copie o 'Access token'" -ForegroundColor Cyan
    Write-Host "4. Cole na variável ACCESS_TOKEN no arquivo test_pix.ps1`n" -ForegroundColor Cyan
    exit
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host " TESTE DE PIX - MERCADO PAGO" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Green

# Data de expiração (15 minutos)
$expirationDate = (Get-Date).AddMinutes(15).ToString("yyyy-MM-ddTHH:mm:ss.000-03:00")

# Payload JSON
$payload = @{
    transaction_amount = 10.50
    description = "Teste PDV - PIX"
    payment_method_id = "pix"
    payer = @{
        email = "test_user_123456@testuser.com"
    }
    date_of_expiration = $expirationDate
} | ConvertTo-Json -Depth 10

Write-Host "📦 Payload:" -ForegroundColor Cyan
Write-Host $payload

Write-Host "`n🚀 Fazendo requisição...`n" -ForegroundColor Yellow

# Headers
$headers = @{
    "Authorization" = "Bearer $ACCESS_TOKEN"
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod `
        -Uri "https://api.mercadopago.com/v1/payments" `
        -Method Post `
        -Headers $headers `
        -Body $payload `
        -ErrorAction Stop
    
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host " ✅ SUCESSO!" -ForegroundColor Green
    Write-Host "============================================================`n" -ForegroundColor Green
    
    Write-Host "📥 Resposta:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10 | Write-Host
    
    Write-Host "`nPayment ID: $($response.id)" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Green
    
    if ($response.point_of_interaction.transaction_data.qr_code) {
        $qrCode = $response.point_of_interaction.transaction_data.qr_code
        Write-Host "`n📱 PIX Copia e Cola (primeiros 100 chars):" -ForegroundColor Yellow
        Write-Host $qrCode.Substring(0, [Math]::Min(100, $qrCode.Length))...
    }
    
} catch {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host " ❌ ERRO!" -ForegroundColor Red
    Write-Host "============================================================`n" -ForegroundColor Red
    
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Status Code: $statusCode`n" -ForegroundColor Red
    
    if ($statusCode -eq 401) {
        Write-Host "⚠️  ERRO DE AUTENTICAÇÃO!" -ForegroundColor Yellow
        Write-Host "Verifique se você está usando TOKEN DE TESTE (não produção)" -ForegroundColor Yellow
    }
    
    try {
        $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "Detalhes do erro:" -ForegroundColor Yellow
        $errorBody | ConvertTo-Json -Depth 10 | Write-Host
    } catch {
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

Write-Host "`n============================================================`n"
