# ==================== ÁREA DE PAGAMENTO INTEGRADA ====================

def mostrar_area_pagamento(self):
    """Mostra área de pagamento integrada."""
    if self.modo_pagamento:
        return  # Já está no modo pagamento
        
    self.modo_pagamento = True
    
    # Atualiza atalhos para modo pagamento
    self.configurar_atalhos_pagamento()
    
    # Limpa container do painel direito
    for widget in self.painel_direito_container.winfo_children():
        widget.destroy()
        
    # Cria área de pagamento
    frame = tk.Frame(self.painel_direito_container, bg="#ffffff", relief=tk.RAISED, bd=3)
    frame.pack(fill=tk.BOTH, expand=True)
    frame.configure(width=400)
    frame.pack_propagate(False)
    
    # Título
    titulo = tk.Frame(frame, bg="#e74c3c", height=40)
    titulo.pack(fill=tk.X)
    tk.Label(titulo, text="💳 PAGAMENTO", font=("Arial", 14, "bold"),
             fg="white", bg="#e74c3c").pack(pady=10)
    
    # Total da venda
    venda = self.venda_service.get_venda_atual()
    total_frame = tk.Frame(frame, bg="#27ae60", relief=tk.RAISED, bd=3)
    total_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(total_frame, text="TOTAL A PAGAR", font=("Arial", 14, "bold"),
             bg="#27ae60", fg="white").pack(pady=(10, 5))
    
    tk.Label(total_frame, text=Formatters.formatar_moeda(float(venda.total)), 
             font=("Arial", 32, "bold"), bg="#27ae60", fg="white").pack(pady=(0, 10))
    
    # Formas de pagamento
    pagamentos_frame = tk.Frame(frame, bg="#ffffff")
    pagamentos_frame.pack(fill=tk.X, padx=15, pady=15)
    
    tk.Label(pagamentos_frame, text="ESCOLHA A FORMA DE PAGAMENTO:",
             font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 15))
    
    # Botões de pagamento grandes
    self.criar_botao_pagamento(pagamentos_frame, "💵 DINHEIRO", "dinheiro", "#27ae60", "F1")
    self.criar_botao_pagamento(pagamentos_frame, "💳 DÉBITO", "debito", "#3498db", "F2") 
    self.criar_botao_pagamento(pagamentos_frame, "💳 CRÉDITO", "credito", "#9b59b6", "F3")
    self.criar_botao_pagamento(pagamentos_frame, "📱 PIX", "pix", "#f39c12", "F4")
    
    # Área de status
    self.status_frame = tk.Frame(frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
    self.status_frame.pack(fill=tk.X, padx=10, pady=10)
    
    self.label_status = tk.Label(self.status_frame, text="Selecione a forma de pagamento",
                                 font=("Arial", 11), bg="#ecf0f1", fg="#7f8c8d")
    self.label_status.pack(pady=10)
    
    # Botões de ação
    acoes_frame = tk.Frame(frame, bg="#ffffff")
    acoes_frame.pack(fill=tk.X, padx=15, pady=15)
    
    tk.Button(acoes_frame, text="ESC - VOLTAR", font=("Arial", 11, "bold"),
              bg="#95a5a6", fg="white", relief=tk.FLAT, pady=8,
              command=self.voltar_venda).pack(fill=tk.X, pady=(0, 5))
    
    tk.Button(acoes_frame, text="F6 - CANCELAR VENDA", font=("Arial", 11, "bold"),
              bg="#e74c3c", fg="white", relief=tk.FLAT, pady=8,
              command=self.cancelar_venda).pack(fill=tk.X)
    
    # Foca no primeiro botão de pagamento
    self.entry_codigo.config(state=tk.DISABLED)

def criar_botao_pagamento(self, parent, texto, tipo, cor, atalho):
    """Cria botão de forma de pagamento."""
    frame = tk.Frame(parent, bg="#ffffff")
    frame.pack(fill=tk.X, pady=5)
    
    btn = tk.Button(frame, text=f"{atalho} - {texto}", font=("Arial", 14, "bold"),
                    bg=cor, fg="white", relief=tk.FLAT, pady=15,
                    command=lambda: self.processar_pagamento(tipo))
    btn.pack(fill=tk.X)
    
    # Efeito hover
    btn.bind("<Enter>", lambda e: btn.config(bg=self.escurecer_cor(cor)))
    btn.bind("<Leave>", lambda e: btn.config(bg=cor))

def escurecer_cor(self, cor):
    """Escurece uma cor hexadecimal."""
    cores = {
        "#27ae60": "#229954",
        "#3498db": "#2980b9", 
        "#9b59b6": "#8e44ad",
        "#f39c12": "#e67e22"
    }
    return cores.get(cor, cor)

def configurar_atalhos_pagamento(self):
    """Configura atalhos para modo pagamento."""
    # Remove atalhos antigos e adiciona novos
    self.bind_all('<F1>', lambda e: self.processar_pagamento('dinheiro'))
    self.bind_all('<F2>', lambda e: self.processar_pagamento('debito'))
    self.bind_all('<F3>', lambda e: self.processar_pagamento('credito'))
    self.bind_all('<F4>', lambda e: self.processar_pagamento('pix'))
    self.bind_all('<Escape>', lambda e: self.voltar_venda())
    
def processar_pagamento(self, forma_pagamento):
    """Processa o pagamento selecionado."""
    venda = self.venda_service.get_venda_atual()
    
    self.label_status.config(text=f"Processando pagamento via {forma_pagamento.upper()}...",
                             fg="#f39c12")
    self.label_status.update()
    
    # Simula processamento
    self.after(1000, lambda: self.finalizar_pagamento(forma_pagamento, venda))

def finalizar_pagamento(self, forma_pagamento, venda):
    """Finaliza o pagamento."""
    try:
        # Processa pagamento
        sucesso = self.venda_service.processar_pagamento(
            venda.id, forma_pagamento, float(venda.total)
        )
        
        if sucesso:
            self.label_status.config(text="✅ PAGAMENTO APROVADO!", fg="#27ae60")
            self.after(1500, self.mostrar_opcoes_finalizacao)
        else:
            self.label_status.config(text="❌ PAGAMENTO RECUSADO!", fg="#e74c3c")
            
    except Exception as e:
        self.label_status.config(text="❌ ERRO NO PAGAMENTO!", fg="#e74c3c")

def mostrar_opcoes_finalizacao(self):
    """Mostra opções após pagamento aprovado."""
    # Limpa status frame
    for widget in self.status_frame.winfo_children():
        widget.destroy()
    
    # Pergunta sobre cupom
    tk.Label(self.status_frame, text="VENDA FINALIZADA COM SUCESSO!", 
             font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#27ae60").pack(pady=(10, 5))
    
    tk.Label(self.status_frame, text="Deseja imprimir cupom não fiscal?",
             font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50").pack(pady=5)
    
    botoes_frame = tk.Frame(self.status_frame, bg="#ecf0f1")
    botoes_frame.pack(pady=10)
    
    tk.Button(botoes_frame, text="F1 - SIM", font=("Arial", 11, "bold"),
              bg="#27ae60", fg="white", relief=tk.FLAT, padx=20, pady=8,
              command=self.imprimir_cupom).pack(side=tk.LEFT, padx=5)
    
    tk.Button(botoes_frame, text="F2 - NÃO", font=("Arial", 11, "bold"),
              bg="#95a5a6", fg="white", relief=tk.FLAT, padx=20, pady=8,
              command=self.nova_venda).pack(side=tk.LEFT, padx=5)
    
    # Configura atalhos
    self.bind_all('<F1>', lambda e: self.imprimir_cupom())
    self.bind_all('<F2>', lambda e: self.nova_venda())
    self.bind_all('<Return>', lambda e: self.nova_venda())
    self.bind_all('<Escape>', lambda e: self.nova_venda())
    
    # Auto-continua após 5 segundos
    self.after(5000, self.nova_venda)

def imprimir_cupom(self):
    """Imprime cupom não fiscal."""
    self.label_status.config(text="🖨️ Imprimindo cupom...", fg="#3498db")
    self.label_status.update()
    
    # Simula impressão
    self.after(2000, lambda: [
        self.label_status.config(text="✅ Cupom impresso!", fg="#27ae60"),
        self.after(1000, self.nova_venda)
    ])

def nova_venda(self):
    """Inicia nova venda."""
    self.modo_pagamento = False
    self.callback_venda_finalizada()
    self.voltar_venda()

def voltar_venda(self):
    """Volta para a tela de vendas."""
    self.modo_pagamento = False
    self.entry_codigo.config(state=tk.NORMAL)
    self.criar_painel_direito()
    self.configurar_atalhos()  # Restaura atalhos originais
    self.entry_codigo.focus()

def mostrar_mensagem_temporaria(self, mensagem, cor="#e74c3c", tempo=3000):
    """Mostra mensagem temporária na tela."""
    # Cria overlay temporário
    overlay = tk.Frame(self, bg=cor, relief=tk.RAISED, bd=3)
    overlay.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    
    tk.Label(overlay, text=mensagem, font=("Arial", 16, "bold"),
             bg=cor, fg="white", padx=30, pady=20).pack()
    
    # Remove após tempo especificado
    self.after(tempo, overlay.destroy)