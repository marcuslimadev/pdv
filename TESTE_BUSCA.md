# 🔍 TESTE DA BUSCA DE PRODUTO - PASSO A PASSO

## 🎯 **COMO TESTAR A BUSCA:**

### **1. Executar Sistema:**
```powershell
cd c:\PDV
C:/PDV/venv/Scripts/python.exe main.py
```

### **2. Login:**
- **Usuário:** `operador`
- **Tab** para campo senha
- **Senha:** `operador123`
- **Enter** para login

### **3. Buscar Produto:**
- **F1** para abrir busca
- **Digite:** `sabonete` (ou outro nome/código)
- **Enter** para buscar

### **4. Navegar e Selecionar:**
- **↑↓** para navegar na lista
- **Enter** ou **F1** ou **Espaço** para selecionar
- **ESC** para cancelar

### **5. Verificar Resultado:**
- Produto deve ser adicionado automaticamente (quantidade 1)
- Deve aparecer na lista da venda
- Mensagem de confirmação verde deve aparecer

---

## 🔧 **SE NÃO FUNCIONAR:**

### **Verificações:**
1. **Lista vazia?** - Verificar se há produtos no banco
2. **Não seleciona?** - Usar **Espaço** em vez de Enter
3. **Erro?** - Verificar mensagem no label de status

### **Debug Ativado:**
- Mensagens de debug no console (prints)
- Verificar terminal onde rodou o sistema

### **Atalhos Alternativos:**
- **F1** - Selecionar produto
- **Espaço** - Selecionar produto  
- **Enter** - Selecionar produto (na lista)
- **ESC** - Cancelar busca

---

## 📝 **MELHORIAS IMPLEMENTADAS:**

### **✅ Busca Automática:**
- Se só 1 resultado, seleciona automaticamente após 100ms
- Primeiro item sempre selecionado por padrão
- Foco automático na lista após busca

### **✅ Múltiplas Formas de Seleção:**
- **Enter** na lista
- **F1** em qualquer lugar
- **Espaço** na lista
- **Double-click** com mouse (se necessário)

### **✅ Adição Simplificada:**
- Sem popup de quantidade
- Adiciona quantidade 1 automaticamente
- Use F7 depois para alterar quantidade (admin)
- Mensagem de confirmação integrada

### **✅ Navegação Intuitiva:**
- ↑↓ para navegar
- Enter no campo = buscar
- Enter na lista = selecionar
- ESC = cancelar sempre

---

## 🚀 **FLUXO COMPLETO TESTE:**

```
1. F1 (busca)
2. Digite "sabonete"
3. Enter (buscar)
4. ↓ (navegar se necessário)
5. Enter (selecionar)
6. ✅ Produto adicionado!
```

**Se der erro ou não funcionar, me avise com detalhes do que aconteceu!**