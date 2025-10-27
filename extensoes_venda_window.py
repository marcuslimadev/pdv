# ==================== OPERAÇÕES ESPECIAIS COM ADMIN ====================

def cancelar_item_com_admin(self):
    """F8 - Cancela item selecionado com autenticação de admin."""
    # Verifica se há item selecionado
    selection = self.tree_produtos.selection()
    if not selection:
        self.mostrar_mensagem_temporaria("⚠️ SELECIONE UM ITEM PARA CANCELAR", "#e67e22")
        return
    
    # Obtém dados do item
    item_values = self.tree_produtos.item(selection[0])['values']
    item_data = {
        'codigo': item_values[1],
        'nome': item_values[2],
        'qtd': item_values[3],
        'preco': item_values[4]
    }
    
    # Solicita autenticação de admin
    from src.services.admin_auth_service import AdminAuthService
    AdminAuthService.solicitar_autenticacao_admin(
        self,
        lambda admin_user: self.executar_cancelamento_item(selection[0], admin_user),
        lambda: self.entry_codigo.focus()
    )

def editar_quantidade_com_admin(self):
    """F7 - Edita quantidade do item com autenticação de admin."""
    # Verifica se há item selecionado
    selection = self.tree_produtos.selection()
    if not selection:
        self.mostrar_mensagem_temporaria("⚠️ SELECIONE UM ITEM PARA EDITAR", "#f39c12")
        return
    
    # Obtém dados do item
    item_values = self.tree_produtos.item(selection[0])['values']
    item_data = {
        'codigo': item_values[1],
        'nome': item_values[2],
        'qtd': item_values[3],
        'preco': item_values[4]
    }
    
    # Solicita autenticação de admin
    from src.services.admin_auth_service import AdminAuthService
    AdminAuthService.solicitar_autenticacao_admin(
        self,
        lambda admin_user: self.executar_edicao_quantidade(selection[0], item_data, admin_user),
        lambda: self.entry_codigo.focus()
    )

def executar_cancelamento_item(self, tree_item_id, admin_user):
    """Executa o cancelamento do item após autenticação."""
    from src.services.admin_auth_service import ItemActionDialog
    
    # Obtém dados do item novamente
    item_values = self.tree_produtos.item(tree_item_id)['values']
    item_data = {
        'codigo': item_values[1],
        'nome': item_values[2],
        'qtd': item_values[3],
        'preco': item_values[4]
    }
    
    # Mostra dialog de confirmação
    dialog = ItemActionDialog(self, item_data, "cancelar")
    self.wait_window(dialog.dialog)
    
    if dialog.resultado and dialog.resultado['acao'] == 'cancelar_item':
        # Cancela o item
        item_index = int(item_values[0]) - 1  # Índice baseado em 0
        if self.venda_service.remover_item(item_index):
            self.atualizar_lista_produtos()
            self.mostrar_mensagem_temporaria(f"✅ ITEM CANCELADO POR {admin_user.nome_completo}", "#27ae60")
            # Log da operação
            from src.utils.logger import Logger
            Logger.log_operacao(admin_user.username, "CANCELAMENTO_ITEM", 
                              f"Item: {item_data['nome']} - Qtd: {item_data['qtd']}")
        else:
            self.mostrar_mensagem_temporaria("❌ ERRO AO CANCELAR ITEM", "#e74c3c")
    
    self.entry_codigo.focus()

def executar_edicao_quantidade(self, tree_item_id, item_data, admin_user):
    """Executa a edição de quantidade após autenticação."""
    from src.services.admin_auth_service import ItemActionDialog
    
    # Mostra dialog de edição
    dialog = ItemActionDialog(self, item_data, "editar_quantidade")
    self.wait_window(dialog.dialog)
    
    if dialog.resultado and dialog.resultado['acao'] == 'editar_quantidade':
        nova_quantidade = dialog.resultado['nova_quantidade']
        
        # Edita a quantidade
        item_values = self.tree_produtos.item(tree_item_id)['values']
        item_index = int(item_values[0]) - 1  # Índice baseado em 0
        
        if self.venda_service.alterar_quantidade_item(item_index, nova_quantidade):
            self.atualizar_lista_produtos()
            self.mostrar_mensagem_temporaria(
                f"✅ QUANTIDADE ALTERADA POR {admin_user.nome_completo}", "#27ae60")
            # Log da operação
            from src.utils.logger import Logger
            Logger.log_operacao(admin_user.username, "EDICAO_QUANTIDADE", 
                              f"Item: {item_data['nome']} - Qtd: {item_data['qtd']} → {nova_quantidade}")
        else:
            self.mostrar_mensagem_temporaria("❌ ERRO AO ALTERAR QUANTIDADE", "#e74c3c")
    
    self.entry_codigo.focus()

# ==================== PIX MERCADO PAGO INTEGRADO ====================

def mostrar_pagamento_pix(self, venda):
    """Mostra interface de pagamento PIX integrada."""
    # Limpa container do painel direito
    for widget in self.painel_direito_container.winfo_children():
        widget.destroy()
    
    # Cria frame do PIX
    from src.ui.caixa.pix_frame import PIXFrame
    
    self.pix_frame = PIXFrame(
        self.painel_direito_container,
        venda.total,
        self.pix_aprovado,
        self.pix_cancelado
    )
    self.pix_frame.pack(fill=tk.BOTH, expand=True)
    
    # Desabilita campo de código durante PIX
    self.entry_codigo.config(state=tk.DISABLED)

def pix_aprovado(self):
    """Callback quando PIX é aprovado."""
    # Finaliza pagamento
    venda = self.venda_service.get_venda_atual()
    sucesso = self.venda_service.processar_pagamento(
        venda.id, "pix", float(venda.total)
    )
    
    if sucesso:
        self.mostrar_opcoes_finalizacao()
    else:
        self.mostrar_mensagem_temporaria("❌ ERRO AO PROCESSAR PAGAMENTO", "#e74c3c")
        self.voltar_venda()

def pix_cancelado(self, motivo):
    """Callback quando PIX é cancelado ou erro."""
    self.mostrar_mensagem_temporaria(f"⚠️ PIX: {motivo.upper()}", "#f39c12")
    self.voltar_venda()

def mostrar_mensagem_temporaria(self, mensagem, cor="#e74c3c", tempo=3000):
    """Mostra mensagem temporária na tela."""
    # Cria overlay temporário
    overlay = tk.Frame(self, bg=cor, relief=tk.RAISED, bd=3)
    overlay.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    
    tk.Label(overlay, text=mensagem, font=("Arial", 16, "bold"),
             bg=cor, fg="white", padx=30, pady=20).pack()
    
    # Remove após tempo especificado
    self.after(tempo, overlay.destroy)