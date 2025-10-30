# Alteração: Separador Decimal - Vírgula em vez de Ponto

## 📝 Resumo
Todos os valores monetários e numéricos do sistema agora usam **vírgula (,)** como separador decimal, seguindo o padrão brasileiro.

## ✅ Arquivos Alterados

### 1. **src/utils/formatters.py**
- ✅ Já estava correto
- `formatar_moeda()` e `formatar_quantidade()` já usavam vírgula

### 2. **src/ui/caixa/venda_window.py**
- ✅ Total a pagar na tela de pagamento
- ✅ Valor sugerido nos botões (R$ 20, R$ 50, R$ 100, R$ 200)
- ✅ Mensagem de troco
- ✅ Mensagem de valor insuficiente
- ✅ Exibição de troco final
- ✅ Total no PIX

### 3. **src/ui/caixa/pagamento_window.py**
- ✅ Valor inicial no campo de pagamento em dinheiro

### 4. **src/ui/caixa/main_caixa.py**
- ✅ Mensagem de abertura de caixa
- ✅ Valor de abertura exibido na tela
- ✅ Confirmação de fechamento (abertura, fechamento e diferença)

### 5. **src/ui/caixa/busca_produto_window.py**
- ✅ Preço dos produtos na listagem de busca

### 6. **src/ui/admin/produtos_window.py**
- ✅ Preço de custo ao editar produto
- ✅ Preço de venda ao editar produto

### 7. **src/ui/admin/estorno_window.py**
- ✅ Quantidade de itens na listagem

### 8. **src/services/venda_service.py**
- ✅ Log de desconto aplicado

### 9. **src/services/mercado_pago_service.py**
- ✅ Log de split de valores (cliente/plataforma)

### 10. **src/services/pix_service.py**
- ✅ Código PIX gerado

### 11. **src/utils/logger.py**
- ✅ Log de vendas
- ✅ Log de pagamentos
- ✅ Log de abertura de caixa
- ✅ Log de fechamento de caixa

## 🔄 Como Funciona

### Antes:
```python
f"R$ {valor:.2f}"  # Resultado: R$ 14.98
```

### Depois:
```python
Formatters.formatar_moeda(valor)  # Resultado: R$ 14,98
# OU
f"R$ {valor:.2f}".replace('.', ',')  # Resultado: R$ 14,98
```

## 📊 Exemplos de Exibição

| Situação | Formato Anterior | Formato Atual |
|----------|------------------|---------------|
| Total da venda | R$ 14.98 | **R$ 14,98** |
| Troco | R$ 35.02 | **R$ 35,02** |
| Abertura de caixa | R$ 100.00 | **R$ 100,00** |
| Preço unitário | R$ 2.50 | **R$ 2,50** |
| Quantidade | 1.500 | **1,500** |

## ⚠️ Importante

### Entrada de Dados
O sistema **aceita tanto ponto quanto vírgula** na entrada:
- Usuário digita: `50` ou `50,00` ou `50.00`
- Sistema converte internamente para Decimal
- Sistema exibe: `R$ 50,00`

### Conversão Interna
```python
# Ao ler do campo de texto:
valor = entry.get().replace(",", ".")  # Converte vírgula para ponto
decimal_valor = Decimal(valor)  # Converte para Decimal

# Ao exibir na tela:
Formatters.formatar_moeda(decimal_valor)  # Exibe com vírgula
```

## 🧪 Testado em:
- ✅ Tela de venda (PDV)
- ✅ Pagamento em dinheiro
- ✅ Pagamento PIX
- ✅ Abertura/Fechamento de caixa
- ✅ Cadastro de produtos
- ✅ Estornos
- ✅ Logs do sistema

## 📸 Exemplo Visual

**Tela de Pagamento em Dinheiro:**
```
┌─────────────────────────────────┐
│  PAGAMENTO EM DINHEIRO          │
│                                 │
│  Total: R$ 14,98                │
│                                 │
│  Valor Pago:                    │
│  ┌──────────┐                   │
│  │   50     │                   │
│  └──────────┘                   │
│                                 │
│  Troco: R$ 35,02                │
│                                 │
│  Valores Sugeridos:             │
│  [R$ 20] [R$ 50] [R$ 100] [R$ 200]
└─────────────────────────────────┘
```

## ✨ Benefícios
1. **Padrão Brasileiro**: Segue o formato monetário usado no Brasil
2. **Consistência**: Todos os valores exibidos da mesma forma
3. **Profissionalismo**: Interface mais polida e profissional
4. **Usabilidade**: Usuários brasileiros estão acostumados com vírgula
