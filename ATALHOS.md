# 📋 Guia de Atalhos do Sistema PDV

## 🛒 Tela de Vendas (Principal)

### Operações de Venda
| Tecla | Função | Descrição |
|-------|--------|-----------|
| **F1** | Buscar Produto | Abre janela de busca de produtos |
| **F2** | Adicionar por Código | Foca no campo de código de barras |
| **F3** | Alterar Quantidade | Solicita quantidade para o próximo produto |
| **F4** | Aplicar Desconto | Aplica desconto na venda |
| **F5** | Remover Item | Remove o item selecionado |
| **F6** | Cancelar Venda | Cancela a venda atual |
| **F10** | Finalizar Venda | Avança para tela de pagamento |

### Operações com Autenticação Admin
| Tecla | Função | Descrição |
|-------|--------|-----------|
| **F7** | Editar Quantidade (Admin) | Edita quantidade com senha admin |
| **F8** | Cancelar Item (Admin) | Cancela item com senha admin |
| **F9** | Fechar Caixa | Fecha o caixa (requer admin) |

### Atalhos Alternativos (Ctrl)
| Tecla | Função |
|-------|--------|
| **Ctrl+N** | Nova Venda |
| **Ctrl+F** | Buscar Produto |
| **Ctrl+D** | Aplicar Desconto |
| **Ctrl+Enter** | Finalizar Venda |

### Navegação
| Tecla | Função |
|-------|--------|
| **↑ / ↓** | Navega na lista de produtos |
| **Home** | Vai para o primeiro item |
| **End** | Vai para o último item |
| **Page Up** | Sobe uma página |
| **Page Down** | Desce uma página |
| **Delete** | Remove item selecionado |
| **Esc** | Limpa campo de código |
| **Tab** | Próximo campo |
| **Shift+Tab** | Campo anterior |

---

## 💳 Tela de Pagamento

### Formas de Pagamento
| Tecla | Função | Alternativa |
|-------|--------|-------------|
| **F1** | Dinheiro | **Ctrl+1** |
| **F2** | Cartão Débito | **Ctrl+2** |
| **F3** | Cartão Crédito | **Ctrl+3** |
| **F4** | PIX Mercado Pago | **Ctrl+4** |

### Navegação
| Tecla | Função |
|-------|--------|
| **↑ / ↓** | Navega entre opções |
| **Enter** | Seleciona opção |
| **Esc** | Volta para tela de venda |
| **F9** | Cancelar venda |

---

## ✅ Tela de Venda Finalizada

| Tecla | Função |
|-------|--------|
| **Enter** | Imprimir cupom |
| **Esc** | Próxima venda (sem imprimir) |

---

## 🔍 Janela de Busca de Produtos

| Tecla | Função |
|-------|--------|
| **F1** | Selecionar produto |
| **Enter** | Selecionar produto |
| **Esc** | Fechar janela |
| **↑ / ↓** | Navegar na lista |

---

## 💡 Dicas de Uso

### Fluxo Rápido de Venda
1. Digite o código de barras e pressione **Enter**
2. Continue digitando códigos ou use **F1** para buscar
3. Use **F3** para alterar quantidade antes de adicionar
4. Pressione **F10** para finalizar
5. Use **F1-F4** ou **Ctrl+1-4** para escolher pagamento
6. Pressione **Enter** para confirmar e imprimir (ou **Esc** para pular)

### Operações Rápidas
- **Número + Enter**: Adiciona produto pelo código
- **F1**: Busca produto por nome
- **F3 + Número + Enter**: Define quantidade antes de adicionar
- **Ctrl+D**: Aplica desconto rápido
- **Delete**: Remove item selecionado

### Segurança
- **F7** e **F8** requerem senha de administrador
- **F9** (Fechar Caixa) requer autenticação admin
- Cancelamento de vendas é registrado no log

---

## 📱 Pagamento PIX (Mercado Pago)

Quando selecionar **F4** na tela de pagamento:
- QR Code é gerado automaticamente
- Código Copia e Cola disponível
- Timer de expiração visível (15 minutos)
- Monitoramento automático do pagamento
- **Esc** para cancelar PIX

---

## 🎯 Atalhos Globais

Estes atalhos funcionam em qualquer tela do sistema:

| Tecla | Função |
|-------|--------|
| **Alt+F4** | Fechar aplicação |
| **F11** | Tela cheia (se disponível) |

---

## 📝 Notas Importantes

1. **F1-F6**: Usados para operações principais de venda
2. **F7-F8**: Operações que requerem senha admin
3. **F9**: Fechar caixa (admin)
4. **F10**: Finalizar venda
5. **Ctrl+1-4**: Alternativos para pagamento (evitam conflito com F1-F4 da venda)
6. **Enter/Esc**: Confirmação e cancelamento padrão

---

*Última atualização: 28/10/2025*
*Versão do Sistema: 1.0*
