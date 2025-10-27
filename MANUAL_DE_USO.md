# 🎮 MANUAL DE USO - SISTEMA PDV

## 🔑 **CREDENCIAIS PADRÃO**

### **Administrador:**
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Acesso:** Todas as funcionalidades

### **Operador:**
- **Usuário:** `operador`
- **Senha:** `operador123`
- **Acesso:** Vendas e pagamentos

---

## 🖥️ **COMO INICIAR O SISTEMA**

### **1. Preparação:**
```powershell
cd c:\PDV
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **2. Iniciar XAMPP:**
- ✅ Ligar Apache
- ✅ Ligar MySQL

### **3. Configurar Banco (primeira vez):**
```powershell
python setup_database.py
```

### **4. Executar Sistema:**
```powershell
python main.py
```

---

## 🏪 **OPERAÇÃO COMPLETA DO PDV**

### **🔐 LOGIN (Teclado)**
1. **Enter** no campo usuário digitado
2. **Tab** para campo senha
3. **Enter** para login
4. **Escape** para sair

### **👨‍💼 ADMINISTRADOR - Tela Principal**

#### **Menu Principal (F1-F6):**
- **F1** - Produtos (Cadastro/Edição)
- **F2** - Categorias (Cadastro/Edição)
- **F3** - Usuários (Cadastro/Edição)
- **F4** - Relatórios (Vendas/Estoque)
- **F5** - Caixa (Ir para vendas)
- **F6** - Logout

#### **🏷️ Gestão de Produtos (F1):**
| Tecla | Ação |
|-------|------|
| **Insert** | Novo produto |
| **Delete** | Excluir selecionado |
| **Enter** | Editar selecionado |
| **↑↓** | Navegar lista |
| **F5** | Atualizar lista |
| **Escape** | Voltar |

#### **📁 Gestão de Categorias (F2):**
| Tecla | Ação |
|-------|------|
| **Insert** | Nova categoria |
| **Delete** | Excluir selecionada |
| **Enter** | Editar selecionada |
| **↑↓** | Navegar lista |
| **Escape** | Voltar |

#### **👥 Gestão de Usuários (F3):**
| Tecla | Ação |
|-------|------|
| **Insert** | Novo usuário |
| **Delete** | Excluir selecionado |
| **Enter** | Editar selecionado |
| **↑↓** | Navegar lista |
| **Escape** | Voltar |

### **💰 OPERADOR - Tela de Vendas**

#### **🛍️ Venda - Atalhos Principais:**
| Tecla | Função |
|-------|---------|
| **F1** | Buscar produto |
| **F2** | Adicionar por código |
| **F3** | Limpar venda atual |
| **F4** | Escolher pagamento |
| **F5** | Desconto no item |
| **F6** | Desconto na venda |
| **F7** | ⭐ Editar qtd (Admin) |
| **F8** | ⭐ Cancelar item (Admin) |
| **F9** | Cancelar venda |
| **F10** | Finalizar venda |

#### **🔍 Busca de Produto (F1):**
1. **F1** - Abre janela de busca
2. **Digite** o nome do produto
3. **↑↓** - Navegar resultados
4. **Enter** - Selecionar produto
5. **Digite quantidade** (ou Enter para 1)
6. **Enter** - Adicionar à venda

#### **📟 Adicionar por Código (F2):**
1. **F2** - Campo código
2. **Digite código** do produto
3. **Enter** - Confirmar
4. **Digite quantidade** (ou Enter para 1)
5. **Enter** - Adicionar à venda

#### **🗑️ Limpar Venda (F3):**
- **F3** - Remove todos os itens
- **Confirmação** - Enter para sim, Escape para cancelar

#### **⭐ NOVA! Editar Quantidade (F7 - Admin):**
1. **Selecione item** na lista (↑↓)
2. **F7** - Editar quantidade
3. **Digite usuário admin** (ex: admin)
4. **Tab** - Campo senha
5. **Digite senha admin** (ex: admin123)
6. **Enter** - Autenticar
7. **Digite nova quantidade** (ex: 2.5)
8. **Enter** - Confirmar alteração

#### **⭐ NOVA! Cancelar Item (F8 - Admin):**
1. **Selecione item** na lista (↑↓)
2. **F8** - Cancelar item
3. **Digite usuário admin** (ex: admin)
4. **Tab** - Campo senha
5. **Digite senha admin** (ex: admin123)
6. **Enter** - Autenticar
7. **"Sim"** - Confirmar cancelamento
8. **Enter** - Item removido

#### **💳 Finalizar Venda (F10):**

##### **Métodos de Pagamento:**
- **F1** - Dinheiro
- **F2** - Cartão Débito
- **F3** - Cartão Crédito
- **F4** - ⭐ PIX (Mercado Pago)
- **F5** - Misto (múltiplos pagamentos)

##### **⭐ NOVO! PIX Mercado Pago (F4):**

**Fluxo Automático PIX:**
1. **F10** (Finalizar) → **F4** (PIX)
2. **🎯 QR Code aparece automaticamente**
3. **📱 Cliente escaneia QR Code** OU
4. **📋 Cliente usa Copia e Cola** (código já copiado)
5. **⏱️ Timer de 15 minutos** aparece
6. **🔄 Sistema verifica a cada 5 segundos**
7. **✅ PAGAMENTO APROVADO!** (automático)
8. **📄 Quer cupom não fiscal?** (s/n)
9. **🆕 Nova venda automaticamente**

**Durante PIX:**
- **Escape** - Cancela PIX e volta ao menu
- **QR Code** - Sempre visível para cliente
- **Código Copia e Cola** - Automaticamente copiado
- **Status** - "Aguardando pagamento..." → "✅ APROVADO!"

---

## 🎯 **DICAS DE USO AVANÇADO**

### **⚡ Operação Rápida:**
1. **Login rápido:** `operador` + Tab + `operador123` + Enter
2. **Produto rápido:** F2 + código + Enter + Enter
3. **PIX rápido:** F10 + F4 (QR automático)
4. **Próxima venda:** Automática após pagamento

### **🔧 Operações Admin (durante venda):**
- **Editou quantidade errada?** F7 (admin auth)
- **Item errado na lista?** F8 (admin auth)
- **Ambos geram log de auditoria**

### **📱 PIX - Cliente:**
1. **QR Code:** Abrir app banco → PIX → Ler QR Code
2. **Copia e Cola:** App banco → PIX → Colar código
3. **Aguardar:** Sistema confirma automaticamente
4. **Tempo:** 15 minutos para pagar

### **🔍 Busca de Produto:**
- **Nome completo:** "Coca Cola 2L"
- **Nome parcial:** "coca" ou "cola"
- **Por categoria:** "bebida" ou "refrigerante"
- **Busca inteligente:** Ignora acentos e maiúsculas

---

## 🚨 **SITUAÇÕES ESPECIAIS**

### **❌ PIX Cancelado:**
- **Cliente desistiu:** Escape durante PIX
- **Tempo esgotado:** Sistema cancela automaticamente
- **Volta ao menu** de pagamentos

### **🔄 PIX Expirado:**
- **Timer zerou:** PIX cancelado automaticamente
- **Gerar novo:** F4 novamente (novo QR Code)

### **🔐 Admin Auth Falhada:**
- **Usuário inexistente:** "Usuário não encontrado"
- **Senha incorreta:** "Senha incorreta"
- **Não é admin:** "Usuário não é administrador"
- **Tentar novamente:** Repetir F7 ou F8

### **📱 Problemas PIX:**
- **QR não carrega:** Verificar internet
- **Pagamento não confirma:** Aguardar (até 5 min)
- **Erro Mercado Pago:** Usar outro método
- **Log completo** salvo para análise

---

## 📊 **LOGS E AUDITORIA**

### **📁 Arquivos de Log:**
- **Local:** `logs/`
- **Arquivo:** `pdv_YYYYMMDD.log`
- **Rotação:** Diária

### **📝 Eventos Importantes:**
- **LOGIN/LOGOUT:** Quem entrou/saiu e quando
- **VENDAS:** Todas as transações
- **PIX:** Criado, aprovado, cancelado
- **ADMIN:** Cancelamentos e edições de quantidade
- **ERROS:** Falhas de sistema ou integração

### **🔍 Consultar Logs:**
```powershell
cd c:\PDV\logs
Get-Content pdv_20241201.log | Select-String "ADMIN_AUTH"
```

---

## 🎉 **RESUMO DE TECLAS IMPORTANTES**

### **🌟 Principais:**
- **F1-F10:** Funções principais
- **↑↓←→:** Navegação
- **Enter:** Confirmar
- **Escape:** Cancelar/Voltar
- **Tab:** Próximo campo

### **⭐ Novidades:**
- **F7:** Editar quantidade (requer admin)
- **F8:** Cancelar item (requer admin)
- **F4 (pagto):** PIX automático Mercado Pago

### **🚀 Produtividade:**
- **PIX:** 100% automático (QR + monitoramento)
- **Admin Auth:** Controle total sobre alterações
- **Logs:** Auditoria completa de operações
- **Teclado:** 100% navegável, sem mouse

---

**💡 DICA FINAL:** O sistema foi desenhado para operação 100% por teclado. Pratique os atalhos F1-F10 e as setas de navegação para máxima produtividade!

**🎯 SISTEMA PRONTO PARA USO PROFISSIONAL!**