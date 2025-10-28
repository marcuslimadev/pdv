# 📋 Guia de Atalhos do Sistema PDV

## 🛒 Tela de Vendas (Principal)

### Operações de Venda
| Tecla | Função | Descrição |
|-------|--------|-----------|
| **F1** | Buscar Produto | **Toggle** - Abre/fecha painel de busca inline |
| **F2** | Adicionar por Código | Foca no campo de código de barras |
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
| **Ctrl+F** | Buscar Produto (toggle) |
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
| **Esc** | Limpa campo de código / Fecha painel de busca |
| **Tab** | Próximo campo |
| **Shift+Tab** | Campo anterior |

---

## 🔍 Painel de Busca de Produtos (Inline)

**O painel de busca aparece na mesma tela, sem popup!**

| Tecla | Função |
|-------|--------|
| **Enter** | Buscar / Selecionar produto |
| **↑ / ↓** | Navegar na lista de resultados |
| **Esc** | Fechar painel de busca |
| **Duplo-clique** | Selecionar produto |

### Como usar:
1. Pressione **F1** para abrir o painel de busca
2. Digite o nome ou código do produto
3. Use **↑↓** para navegar nos resultados
4. Pressione **Enter** ou **Espaço** para selecionar
5. **Esc** fecha o painel e volta para a venda

---

## 💳 Tela de Pagamento

**Sistema inline - sem popups! Escolha a forma de pagamento diretamente.**

### Formas de Pagamento
| Tecla | Função |
|-------|--------|
| **F1** | 💵 Dinheiro (valor exato) |
| **F2** | 💳 Cartão Débito |
| **F3** | 💳 Cartão Crédito |
| **F4** | 📱 PIX Mercado Pago |

### Navegação
| Tecla | Função |
|-------|--------|
| **↑ / ↓** | Navega entre opções |
| **Enter** | Seleciona opção |
| **Esc** | Volta para tela de venda |
| **F9** | Cancelar venda |

### PIX Inline
Quando selecionar **F4 (PIX)**:
- QR Code aparece na própria tela (não abre janela)
- Código Copia e Cola disponível
- Timer de expiração visível (15 minutos)
- Monitoramento automático do pagamento
- **Esc** para cancelar PIX e voltar

---

## ✅ Tela de Venda Finalizada

| Tecla | Função |
|-------|--------|
| **Enter** | Imprimir cupom |
| **Esc** | Próxima venda (sem imprimir) |

---

## 💡 Dicas de Uso

### Fluxo Rápido de Venda (SEM POPUPS!)
1. Digite o código de barras e pressione **Enter**
2. Continue digitando códigos ou use **F1** para buscar (painel inline abre)
3. Digite quantidade antes do código (ex: 3 + código = adiciona 3 unidades)
4. Pressione **F10** para finalizar
5. Use **F1-F4** para escolher pagamento (direto na tela)
6. Pressione **Enter** para confirmar e imprimir (ou **Esc** para pular)

### Operações Rápidas
- **Número + Enter**: Adiciona produto pelo código
- **F1**: Toggle busca inline (abre/fecha na mesma tela)
- **Quantidade + Código**: Digite 3, depois leia código = adiciona 3 unidades
- **Delete**: Remove item selecionado
- **F10**: Vai direto para pagamento inline

### Busca Inteligente
- **F1** abre painel de busca **na mesma tela**
- Digite parte do nome ou código completo
- Navegue com **↑↓**
- **Enter** ou **Espaço** seleciona
- **Esc** fecha e volta para venda
- **Nenhuma janela popup!**

### Pagamento Inline
- **Sem popups!** Tudo aparece na mesma tela
- **F1-F4**: Escolha rápida de forma de pagamento
- PIX mostra QR Code inline (não abre janela)
- Cartões processam direto na tela
- **Esc** sempre volta para venda

### Segurança
- **F7** e **F8** requerem senha de administrador
- **F9** (Fechar Caixa) requer autenticação admin
- Cancelamento de vendas é registrado no log

---

## 📱 Pagamento PIX (Mercado Pago) - Inline

Quando selecionar **F4** na tela de pagamento:
- QR Code é gerado e **aparece na mesma tela** (não abre janela)
- Código Copia e Cola disponível ao lado do QR Code
- Timer de expiração visível (15 minutos)
- Monitoramento automático do pagamento em tempo real
- **Esc** para cancelar PIX e voltar para opções de pagamento
- Confirmação de pagamento aparece inline quando aprovado

**Nenhum popup! Tudo integrado na mesma interface.**

---

## 🎯 Atalhos Globais

Estes atalhos funcionam em qualquer tela do sistema:

| Tecla | Função |
|-------|--------|
| **Alt+F4** | Fechar aplicação |
| **F11** | Tela cheia (se disponível) |

---

## 📝 Notas Importantes

### Interface Sem Popups! 🎉
1. **F1**: Toggle de busca inline (abre/fecha na mesma tela)
2. **F2**: Adicionar por código
3. **F5-F6**: Remoção e cancelamento
4. **F7-F8**: Operações que requerem senha admin
5. **F9**: Fechar caixa (admin)
6. **F10**: Finalizar venda
7. **Pagamento**: Tudo inline, sem janelas popup
8. **PIX**: QR Code aparece na mesma tela
9. **Enter/Esc**: Confirmação e cancelamento padrão

### Melhorias de UX
- ✅ Nenhuma janela popup interrompe o fluxo
- ✅ Busca de produtos inline (F1 toggle)
- ✅ Pagamentos processados na mesma tela
- ✅ PIX com QR Code integrado
- ✅ Mensagens temporárias em vez de alertas
- ✅ Navegação fluida por teclado
- ✅ Foco automático após operações

### Performance
- Busca otimizada com cache
- Auto-seleção em buscas únicas
- Atalhos sem conflitos
- Navegação rápida (↑↓, Home, End, PgUp, PgDn)

---

*Última atualização: 28/10/2025*
*Versão do Sistema: 2.0 - Interface Inline (Sem Popups)*
