# Script PowerShell para testar API do Mercado Pago
# Execute: .\testar_mercadopago_curl.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TESTE DE API - MERCADO PAGO PIX" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Ler access token do config.ini
$configPath = "config.ini"
if (Test-Path $configPath) {
    $config = Get-Content $configPath
    $accessTokenLine = $config | Where-Object { $_ -match "^access_token\s*=" }
    if ($accessTokenLine) {
        $accessToken = ($accessTokenLine -split "=", 2)[1].Trim()
        if ($accessToken -eq "") {
            Write-Host "❌ Access token não configurado no config.ini!" -ForegroundColor Red
            Write-Host "`nPara configurar:" -ForegroundColor Yellow
            Write-Host "1. Acesse: https://www.mercadopago.com.br/developers/panel" -ForegroundColor White
            Write-Host "2. Crie uma aplicação" -ForegroundColor White
            Write-Host "3. Copie o Access Token" -ForegroundColor White
            Write-Host "4. Cole no arquivo config.ini na linha 'access_token ='" -ForegroundColor White
            exit
        }
        Write-Host "✓ Access token encontrado: $($accessToken.Substring(0, 20))..." -ForegroundColor Green
    }
} else {
    Write-Host "❌ Arquivo config.ini não encontrado!" -ForegroundColor Red
    exit
}

Write-Host "`n1️⃣  TESTANDO CREDENCIAIS..." -ForegroundColor Yellow
Write-Host "Endpoint: GET /v1/users/me`n" -ForegroundColor Gray

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.mercadopago.com/v1/users/me" -Method Get -Headers $headers
    Write-Host "✓ Credenciais válidas!" -ForegroundColor Green
    Write-Host "  ID: $($response.id)" -ForegroundColor White
    Write-Host "  Email: $($response.email)" -ForegroundColor White
    Write-Host "  Nickname: $($response.nickname)" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao validar credenciais:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit
}

Write-Host "`n2️⃣  TESTANDO CRIAÇÃO DE PAGAMENTO PIX..." -ForegroundColor Yellow
Write-Host "Endpoint: POST /v1/payments`n" -ForegroundColor Gray

$paymentData = @{
    transaction_amount = 0.01
    description = "Teste PDV - PIX"
    payment_method_id = "pix"
    payer = @{
        email = "teste@teste.com"
    }
} | ConvertTo-Json

try {
    $paymentResponse = Invoke-RestMethod -Uri "https://api.mercadopago.com/v1/payments" -Method Post -Headers $headers -Body $paymentData
    
    Write-Host "✓ Pagamento PIX criado com sucesso!" -ForegroundColor Green
    Write-Host "  Payment ID: $($paymentResponse.id)" -ForegroundColor White
    Write-Host "  Status: $($paymentResponse.status)" -ForegroundColor White
    Write-Host "  Valor: R$ $($paymentResponse.transaction_amount)" -ForegroundColor White
    
    if ($paymentResponse.point_of_interaction.transaction_data.qr_code) {
        Write-Host "  QR Code: $($paymentResponse.point_of_interaction.transaction_data.qr_code.Substring(0, 50))..." -ForegroundColor White
        Write-Host "`n✅ API DO MERCADO PAGO FUNCIONANDO CORRETAMENTE!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  QR Code não retornado" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Erro ao criar pagamento PIX:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "`nDetalhes do erro:" -ForegroundColor Yellow
        Write-Host ($errorDetails | ConvertTo-Json -Depth 5) -ForegroundColor Gray
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "FIM DO TESTE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
