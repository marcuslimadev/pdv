# Correção do ESC na Tela de Vendas

## Problema Identificado
A tecla ESC não estava funcionando corretamente para sair da tela de pagamento e voltar para a venda.

## Causas Identificadas

1. **Conflito de Bindings**: Os bindings globais (`bind_all`) não estavam sendo limpos corretamente ao alternar entre modos (venda → pagamento → venda).

2. **Falta de Reconfiguração**: Quando voltava da tela de pagamento, os atalhos não eram reconfigurados completamente.

3. **Estado Inconsistente**: O flag `modo_pagamento` não era gerenciado de forma consistente em todos os fluxos.

## Correções Implementadas

### 1. Handler do ESC Melhorado
```python
def _handle_escape(self, event):
    # Prioridade 1: Se a busca está aberta, fecha a busca
    if hasattr(self, 'painel_busca') and self.painel_busca.winfo_ismapped():
        self.painel_busca.ocultar()
        self.frame_venda.pack(fill=tk.BOTH, expand=True)
        self.entry_codigo.focus_set()
        return "break"
    
    # Prioridade 2: Se está em modo pagamento, volta para venda
    if self.modo_pagamento:
        self.voltar_para_venda()
    else:
        # Modo venda normal - limpa campo de código
        self.limpar_campo_codigo()
    return "break"
```

### 2. Função `voltar_para_venda` Robusta
- Destrói corretamente todos os frames de pagamento/PIX
- Limpa widgets extras no painel esquerdo
- **Reconfigura TODOS os atalhos** chamando `configurar_atalhos()`
- Restaura o modo venda (`modo_pagamento = False`)
- Retorna foco para o campo de código

### 3. Navegação no Pagamento Isolada
```python
def configurar_navegacao_pagamento(self):
    # Remove bindings conflitantes
    self.unbind_all('<Up>')
    self.unbind_all('<Down>')
    self.unbind_all('<Return>')
    
    # Adiciona navegação específica
    self.bind_all('<Up>', self._navegar_pagamento_cima)
    self.bind_all('<Down>', self._navegar_pagamento_baixo)
    self.bind_all('<Return>', self._executar_pagamento_selecionado)
```

### 4. ESC na Tela de Troco (Dinheiro)
- Unbind do ESC global antes de criar handlers locais
- Handlers locais específicos para o frame de troco
- Garantia de que ESC sempre volta para venda

### 5. ESC na Tela de Cupom
- Handlers específicos que retornam "break"
- Chamam `nova_venda()` que já reconfigura tudo

## Fluxo Correto Agora

### Fluxo Normal de Venda
1. **ESC**: Limpa campo de código
2. **F10**: Vai para pagamento
3. **ESC no pagamento**: Volta para venda (reconfigura atalhos)

### Fluxo com Busca
1. **F1**: Abre busca
2. **ESC**: Fecha busca, volta para venda

### Fluxo de Pagamento em Dinheiro
1. **F10 → F1**: Vai para tela de troco
2. **ESC**: Volta para seleção de pagamento
3. **ESC novamente**: Volta para venda

### Fluxo de Finalização
1. Pagamento aprovado
2. Tela de cupom aparece
3. **ESC**: Inicia nova venda (reconfigura tudo)

## Benefícios das Correções

✅ **ESC sempre funciona** em qualquer tela  
✅ **Não há mais bindings duplicados** ou conflitantes  
✅ **Navegação consistente** em todos os modos  
✅ **Estado do sistema sempre correto** após voltar  
✅ **Foco automático** no campo correto após cada ação  

## Teste Manual Recomendado

1. Adicionar produtos à venda
2. Pressionar F10 (ir para pagamento)
3. Pressionar ESC (deve voltar para venda)
4. Verificar se F10 ainda funciona
5. Ir para pagamento novamente
6. Escolher dinheiro (F1)
7. Pressionar ESC na tela de troco
8. Verificar se voltou corretamente
9. Finalizar uma venda
10. Pressionar ESC na tela de cupom
11. Verificar se iniciou nova venda corretamente

## Data da Correção
29 de outubro de 2025

## Arquivos Modificados
- `c:\PDV\src\ui\caixa\venda_window.py`
