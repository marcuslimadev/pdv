# 💰 Split de Pagamento PIX - Mercado Pago

## 📋 Como Funciona

O sistema PDV implementa um **split automático** de pagamentos PIX via Mercado Pago, dividindo o valor da venda em duas partes:

- **99% para o Cliente** (dono do estabelecimento)
- **1% para a Plataforma** (taxa de uso do sistema)

### Exemplo Prático

Em uma venda de **R$ 100,00**:
- **R$ 99,00** vai para a chave PIX do cliente
- **R$ 1,00** vai para a chave PIX da plataforma

---

## ⚙️ Configuração

### 1️⃣ Configurar Token do Mercado Pago

Primeiro, configure o token de acesso do Mercado Pago:

```bash
python configurar_mp.py
```

**Token atual:** `APP_USR-5277822483126127-102809-a09cb83773553fe2d363c5ed29d26d78-223753899`

### 2️⃣ Configurar Chave PIX do Cliente

Para ativar o split, você PRECISA configurar a chave PIX que receberá os 99%:

```bash
python configurar_pix_cliente.py
```

O script irá solicitar:
- Chave PIX (pode ser CPF, CNPJ, Email, Telefone ou Chave Aleatória)
- Confirmação da configuração

**Importante:** Sem essa configuração, o split NÃO será aplicado e 100% do valor irá para a conta do Mercado Pago.

### 3️⃣ Testar o Split

Após configurar, teste se está funcionando:

```bash
python testar_split_pix.py
```

O teste irá:
1. Verificar as configurações
2. Criar um pagamento PIX de teste
3. Mostrar a divisão dos valores
4. Verificar se o split foi aplicado
5. Cancelar o pagamento de teste

---

## 🔍 Constantes do Sistema

As seguintes constantes estão definidas em `src/services/config_service.py` e **NÃO PODEM** ser alteradas pelo usuário:

```python
PIX_PLATAFORMA = "92992287144"  # Chave PIX fixa da plataforma
PERCENTUAL_CLIENTE = 99         # 99% para o cliente
PERCENTUAL_PLATAFORMA = 1       # 1% para a plataforma
```

---

## 📊 Como o Split é Aplicado

### No Backend (mercado_pago_service.py)

Quando um pagamento PIX é criado:

1. **Calcula os valores:**
   ```python
   valor_plataforma = valor_total * 1%
   valor_cliente = valor_total - valor_plataforma
   ```

2. **Adiciona ao payload da API:**
   ```python
   payment_data["application_fee"] = valor_plataforma
   ```

3. **Registra metadata:**
   ```python
   payment_data["metadata"] = {
       "split_cliente": valor_cliente,
       "split_plataforma": valor_plataforma,
       "chave_pix_cliente": chave_configurada,
       "chave_pix_plataforma": PIX_PLATAFORMA
   }
   ```

### Logs

O sistema registra todas as operações de split:

```
[MercadoPago] SPLIT_CALCULADO - Total: R$ 100.00 | Cliente (99%): R$ 99.00 | Plataforma (1%): R$ 1.00
[MercadoPago] SPLIT_CONFIGURADO - Split ativado - Cliente: 12345678900 | Plataforma: 92992287144
[MercadoPago] PIX_CRIADO - Payment ID: 131689044420
```

---

## ⚠️ Avisos Importantes

### Split Desabilitado

Se a chave PIX do cliente NÃO estiver configurada:

```
[MercadoPago] SPLIT_DESABILITADO - Chave PIX do cliente não configurada
```

Neste caso:
- ❌ O split NÃO será aplicado
- ❌ 100% do valor fica na conta do Mercado Pago
- ❌ Não haverá divisão automática

### Requisitos do Mercado Pago

Para que o split funcione via API do Mercado Pago:

1. ✅ Conta do Mercado Pago ativa e verificada
2. ✅ Chave PIX cadastrada na conta
3. ✅ Token de acesso válido (configurado)
4. ✅ Permissões adequadas no token

**Nota:** O Mercado Pago pode ter requisitos específicos para split de pagamento. Verifique a documentação oficial.

---

## 🧪 Testando o Sistema

### Teste Completo

```bash
# 1. Configure o token
python configurar_mp.py

# 2. Configure a chave PIX do cliente
python configurar_pix_cliente.py

# 3. Teste o split
python testar_split_pix.py
```

### Teste Real (Venda Completa)

1. Abra o sistema PDV: `python main.py`
2. Faça login
3. Adicione produtos à venda
4. Finalize com PIX (F4)
5. Verifique os logs para confirmar o split

---

## 📁 Arquivos Relacionados

### Serviços
- `src/services/mercado_pago_service.py` - Implementação do split
- `src/services/config_service.py` - Constantes e configurações
- `src/services/pix_service.py` - PIX estático (sem split)

### Scripts de Configuração
- `configurar_mp.py` - Configura token Mercado Pago
- `configurar_pix_cliente.py` - Configura chave PIX do cliente
- `testar_split_pix.py` - Testa o funcionamento do split

### Testes
- `test_mp_integration.py` - Teste de integração básica

---

## 🔧 Solução de Problemas

### Split não está sendo aplicado

**Verificar:**
1. Chave PIX do cliente está configurada?
   ```bash
   python -c "from src.services.config_service import config_service; print(config_service.get_pix_chave_cliente())"
   ```

2. Token do Mercado Pago está correto?
   ```bash
   python -c "from src.services.config_service import config_service; print(config_service.get_mercadopago_access_token()[-10:])"
   ```

3. Logs mostram erro?
   ```bash
   cat logs/pdv_*.log | grep SPLIT
   ```

### Erro "application_fee"

Se o Mercado Pago rejeitar o campo `application_fee`, pode ser:
- Token sem permissões adequadas
- Conta não habilitada para marketplace/split
- Versão da API não suporta split

**Solução alternativa:** Remover o split automático e fazer a divisão manualmente fora do sistema.

---

## 📊 Consulta Rápida

### Valores do Split

| Venda | Cliente (99%) | Plataforma (1%) |
|-------|---------------|-----------------|
| R$ 10,00 | R$ 9,90 | R$ 0,10 |
| R$ 50,00 | R$ 49,50 | R$ 0,50 |
| R$ 100,00 | R$ 99,00 | R$ 1,00 |
| R$ 500,00 | R$ 495,00 | R$ 5,00 |
| R$ 1.000,00 | R$ 990,00 | R$ 10,00 |

### Comandos Úteis

```bash
# Ver chave PIX do cliente
python -c "from src.services.config_service import config_service; print(f'Cliente: {config_service.get_pix_chave_cliente()}')"

# Ver todas as configurações PIX
python -c "from src.services.config_service import config_service, PIX_PLATAFORMA; print(f'Cliente: {config_service.get_pix_chave_cliente()}\nPlataforma: {PIX_PLATAFORMA}')"

# Limpar chave PIX (desabilitar split)
python -c "from src.services.config_service import config_service; config_service.set_pix_chave_cliente(''); print('Split desabilitado')"
```

---

## 📝 Changelog

### 29/10/2025
- ✅ Implementado split automático 99%/1%
- ✅ Criados scripts de configuração
- ✅ Criado script de teste
- ✅ Adicionada documentação completa
- ✅ Implementados logs detalhados

---

## 🎯 Próximos Passos (Futuro)

- [ ] Interface gráfica para configurar chave PIX
- [ ] Relatório de valores divididos (cliente vs plataforma)
- [ ] Histórico de splits realizados
- [ ] Suporte a múltiplas chaves PIX
- [ ] Percentuais configuráveis (se permitido pela plataforma)

---

**Sistema PDV - Split de Pagamento PIX** 💰✨
