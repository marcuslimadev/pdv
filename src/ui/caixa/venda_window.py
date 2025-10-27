"""
Tela de vendas com atalhos de teclado F2-F10 e interface otimizada.
Permite quantidade multiplicadora e navegação completa por teclado.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from src.models.usuario import Usuario
from src.models.caixa import Caixa
from src.services.venda_service import VendaService
from src.dao.produto_dao import ProdutoDAO
from src.utils.formatters import Formatters


class VendaFrame(ttk.Frame):
    """Frame otimizado para operação de caixa por teclado."""
    
    def __init__(self, parent, usuario: Usuario, caixa: Caixa, callback_fechar_caixa):
        super().__init__(parent)
        
        self.usuario = usuario
        self.caixa = caixa
        self.callback_fechar_caixa = callback_fechar_caixa
        self.venda_service = VendaService()
        
        # Quantidade multiplicadora (digitar 3 antes de ler código)
        self.quantidade_digitada = ""
        
        # Inicia nova venda
        self.venda_service.iniciar_nova_venda(usuario.id, caixa.id)
        
        self.criar_widgets()
        self.configurar_atalhos()
        self.entry_codigo.focus()
    
    def configurar_atalhos(self):
        """Configura atalhos F1-F10 e navegação completa por teclado."""
        # Atalhos de função
        self.bind_all('<F1>', lambda e: self.buscar_produto())
        self.bind_all('<F2>', lambda e: self.adicionar_produto_por_codigo())
        self.bind_all('<F3>', lambda e: self.solicitar_quantidade())
        self.bind_all('<F4>', lambda e: self.aplicar_desconto())
        self.bind_all('<F5>', lambda e: self.remover_item_selecionado())
        self.bind_all('<F6>', lambda e: self.cancelar_venda())
        self.bind_all('<F9>', lambda e: self.callback_fechar_caixa())
        self.bind_all('<F10>', lambda e: self.finalizar_venda())
        
        # Navegação e operações
        self.bind_all('<Delete>', lambda e: self.remover_item_selecionado())
        self.bind_all('<Escape>', lambda e: self.limpar_campo_codigo())
        self.bind_all('<Tab>', self._navegar_proximo)
        self.bind_all('<Shift-Tab>', self._navegar_anterior)
        
        # Navegação na lista de produtos com setas
        self.bind_all('<Up>', self._navegar_lista_cima)
        self.bind_all('<Down>', self._navegar_lista_baixo)
        self.bind_all('<Home>', self._ir_primeiro_item)
        self.bind_all('<End>', self._ir_ultimo_item)
        self.bind_all('<Page_Up>', self._pagina_cima)
        self.bind_all('<Page_Down>', self._pagina_baixo)
        
        # Atalhos avançados
        self.bind_all('<Control-n>', lambda e: self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id))
        self.bind_all('<Control-f>', lambda e: self.buscar_produto())
        self.bind_all('<Control-d>', lambda e: self.aplicar_desconto())
        
        # Enter alternativo para finalizar
        self.bind_all('<Control-Return>', lambda e: self.finalizar_venda())
        
        # Atalhos para operações especiais com admin
        self.bind_all('<F8>', lambda e: self.cancelar_item_com_admin())
        self.bind_all('<F7>', lambda e: self.editar_quantidade_com_admin())
    
    def criar_widgets(self):
        """Cria interface."""
        main = tk.Frame(self, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Barra de atalhos
        self.criar_barra_atalhos(main)
        
        # Info operador
        info = tk.Frame(main, bg="#34495e", height=40)
        info.pack(fill=tk.X)
        tk.Label(info, text=f"👤 {self.usuario.nome_completo}  |  💵 Caixa #{self.caixa.id}",
                 font=("Arial", 11, "bold"), fg="white", bg="#34495e").pack(pady=10)
        
        # Campo código GRANDE
        self.criar_campo_entrada(main)
        
        # Conteúdo
        content = ttk.Frame(main)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.criar_lista_produtos(content)
        
        # Container para painel direito (total/pagamento)
        self.painel_direito_container = tk.Frame(content)
        self.painel_direito_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.criar_painel_direito()
        
        # Estado da tela
        self.modo_pagamento = False
    
    def criar_barra_atalhos(self, parent):
        """Barra com teclas F2-F10."""
        barra = tk.Frame(parent, bg="#2c3e50", height=45)
        barra.pack(fill=tk.X)
        
        atalhos = [
            ("F1", "Buscar", "#3498db"), ("F2", "Por Código", "#16a085"),
            ("F3", "Quantidade", "#f39c12"), ("F4", "Desconto", "#9b59b6"), 
            ("F5", "Cancelar Item", "#e67e22"), ("F6", "Cancelar Venda", "#e74c3c"), 
            ("F7", "Edit. Qtd (ADM)", "#f39c12"), ("F8", "Cancel. Item (ADM)", "#e74c3c"), 
            ("F9", "Fechar Caixa", "#95a5a6"), ("F10", "FINALIZAR", "#27ae60"),
        ]
        
        for tecla, texto, cor in atalhos:
            f = tk.Frame(barra, bg="#2c3e50")
            f.pack(side=tk.LEFT, padx=5, pady=5)
            tk.Label(f, text=tecla, font=("Arial", 9, "bold"), bg=cor, fg="white",
                     padx=8, pady=4, relief=tk.RAISED, bd=2).pack()
            tk.Label(f, text=texto, font=("Arial", 8), bg="#2c3e50", fg="white").pack()
    
    def criar_campo_entrada(self, parent):
        """Campo GRANDE para código."""
        frame = tk.Frame(parent, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        inner = tk.Frame(frame, bg="#ffffff")
        inner.pack(fill=tk.X, padx=15, pady=15)
        
        top = tk.Frame(inner, bg="#ffffff")
        top.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(top, text="LEIA O CÓDIGO DE BARRAS OU DIGITE O CÓDIGO",
                 font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(side=tk.LEFT)
        
        self.label_quantidade = tk.Label(top, text="", font=("Arial", 14, "bold"),
                                          bg="#ffffff", fg="#27ae60")
        self.label_quantidade.pack(side=tk.RIGHT, padx=10)
        
        self.entry_codigo = tk.Entry(inner, font=("Arial", 24, "bold"), bg="#f8f9fa",
                                      fg="#2c3e50", relief=tk.FLAT, insertwidth=4)
        self.entry_codigo.pack(fill=tk.X, ipady=15)
        self.entry_codigo.bind('<Return>', lambda e: self.adicionar_produto_por_codigo())
        self.entry_codigo.bind('<KeyPress>', self.capturar_quantidade)
        
        tk.Label(inner, text="💡 Digite quantidade antes do código (ex: 3 depois leia) | Use vírgula para peso (1,5)",
                 font=("Arial", 9, "italic"), bg="#ffffff", fg="#7f8c8d").pack(pady=(10, 0))
        
        # Label de status para mensagens
        self.label_status = tk.Label(inner, text="Sistema pronto para uso",
                                     font=("Arial", 11), bg="#ffffff", fg="#2c3e50")
        self.label_status.pack(pady=(5, 0))
    
    def criar_lista_produtos(self, parent):
        """Lista de produtos."""
        frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        titulo = tk.Frame(frame, bg="#3498db", height=40)
        titulo.pack(fill=tk.X)
        tk.Label(titulo, text="ITENS DA VENDA", font=("Arial", 14, "bold"),
                 fg="white", bg="#3498db").pack(pady=10)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_produtos = ttk.Treeview(tree_frame, yscrollcommand=scroll.set, height=15,
            columns=("item", "codigo", "nome", "qtd", "preco", "subtotal"), show="headings")
        
        self.tree_produtos.heading("item", text="#")
        self.tree_produtos.heading("codigo", text="Código")
        self.tree_produtos.heading("nome", text="Produto")
        self.tree_produtos.heading("qtd", text="Qtd")
        self.tree_produtos.heading("preco", text="Preço Unit.")
        self.tree_produtos.heading("subtotal", text="Subtotal")
        
        self.tree_produtos.column("item", width=40, anchor=tk.CENTER)
        self.tree_produtos.column("codigo", width=100)
        self.tree_produtos.column("nome", width=250)
        self.tree_produtos.column("qtd", width=80, anchor=tk.CENTER)
        self.tree_produtos.column("preco", width=100, anchor=tk.E)
        self.tree_produtos.column("subtotal", width=120, anchor=tk.E)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=35)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.tree_produtos.tag_configure('oddrow', background='#f8f9fa')
        self.tree_produtos.tag_configure('evenrow', background='white')
        
        scroll.config(command=self.tree_produtos.yview)
        self.tree_produtos.pack(fill=tk.BOTH, expand=True)
    
    def criar_painel_direito(self):
        """Display para cliente."""
        # Limpa container
        for widget in self.painel_direito_container.winfo_children():
            widget.destroy()
            
        frame = tk.Frame(self.painel_direito_container, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.configure(width=400)
        frame.pack_propagate(False)
        
        titulo = tk.Frame(frame, bg="#27ae60", height=40)
        titulo.pack(fill=tk.X)
        tk.Label(titulo, text="DISPLAY DO CLIENTE", font=("Arial", 14, "bold"),
                 fg="white", bg="#27ae60").pack(pady=10)
        
        # Último item
        ultimo = tk.Frame(frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        ultimo.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(ultimo, text="ÚLTIMO ITEM:", font=("Arial", 10, "bold"),
                 bg="#ecf0f1", fg="#7f8c8d").pack(pady=(10, 5))
        
        self.label_ultimo_produto = tk.Label(ultimo, text="-", font=("Arial", 16, "bold"),
                                               bg="#ecf0f1", fg="#2c3e50", wraplength=350)
        self.label_ultimo_produto.pack(pady=(0, 5))
        
        self.label_ultimo_valor = tk.Label(ultimo, text="R$ 0,00", font=("Arial", 28, "bold"),
                                            bg="#ecf0f1", fg="#27ae60")
        self.label_ultimo_valor.pack(pady=(0, 10))
        
        tk.Frame(frame, bg="#bdc3c7", height=2).pack(fill=tk.X, padx=10, pady=10)
        
        # Totais
        totais = tk.Frame(frame, bg="#ffffff")
        totais.pack(fill=tk.X, padx=15, pady=10)
        
        self.criar_linha_total(totais, "ITENS:", "label_qtd_itens", "0", "#7f8c8d", 12)
        self.criar_linha_total(totais, "SUBTOTAL:", "label_subtotal", "R$ 0,00", "#7f8c8d", 14)
        self.criar_linha_total(totais, "DESCONTO:", "label_desconto", "R$ 0,00", "#e74c3c", 12)
        
        tk.Frame(totais, bg="#27ae60", height=3).pack(fill=tk.X, pady=15)
        
        total_frame = tk.Frame(totais, bg="#27ae60", relief=tk.RAISED, bd=3)
        total_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(total_frame, text="TOTAL A PAGAR", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white").pack(pady=(10, 5))
        
        self.label_total = tk.Label(total_frame, text="R$ 0,00", font=("Arial", 42, "bold"),
                                     bg="#27ae60", fg="white")
        self.label_total.pack(pady=(0, 10))
        
        tk.Frame(frame, bg="#ffffff").pack(fill=tk.BOTH, expand=True)
        
        instr = tk.Frame(frame, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        instr.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(instr, text="Pressione F10 para FINALIZAR", font=("Arial", 11, "bold"),
                 bg="#f8f9fa", fg="#27ae60").pack(pady=8)
    
    def criar_linha_total(self, parent, label, attr, valor, cor, tamanho):
        """Cria linha de total."""
        f = tk.Frame(parent, bg="#ffffff")
        f.pack(fill=tk.X, pady=5)
        tk.Label(f, text=label, font=("Arial", tamanho), bg="#ffffff", fg=cor).pack(side=tk.LEFT)
        lbl = tk.Label(f, text=valor, font=("Arial", tamanho, "bold"), bg="#ffffff", fg="#2c3e50" if "desconto" not in attr else cor)
        lbl.pack(side=tk.RIGHT)
        setattr(self, attr, lbl)
    
    def capturar_quantidade(self, event):
        """Captura dígitos para multiplicador."""
        if event.char.isdigit() or event.char in '.,':
            if self.entry_codigo.get() == "" and event.char.isdigit():
                self.quantidade_digitada += event.char
                self.label_quantidade.config(text=f"Qtd: {self.quantidade_digitada} X")
                return "break"
            elif self.quantidade_digitada and (event.char.isdigit() or event.char in '.,'):
                self.quantidade_digitada += event.char
                self.label_quantidade.config(text=f"Qtd: {self.quantidade_digitada} X")
                return "break"
    
    def adicionar_produto_por_codigo(self):
        """Adiciona produto."""
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            return
        
        try:
            quantidade = Decimal(self.quantidade_digitada.replace(',', '.') if self.quantidade_digitada else '1')
        except:
            messagebox.showerror("Erro", "Quantidade inválida!")
            self.quantidade_digitada = ""
            self.label_quantidade.config(text="")
            return
            
        produto = ProdutoDAO.buscar_por_codigo_barras(codigo)
        
        if not produto:
            produtos = ProdutoDAO.buscar_por_nome(codigo)
            if len(produtos) == 1:
                produto = produtos[0]
            elif len(produtos) > 1:
                self.buscar_produto(codigo)
                self.quantidade_digitada = ""
                self.label_quantidade.config(text="")
                return
        
        if produto:
            sucesso, msg = self.venda_service.adicionar_produto(produto, quantidade)
            if sucesso:
                self.atualizar_lista_produtos()
                self.label_ultimo_produto.config(text=f"{produto.nome}\n{quantidade} x {Formatters.formatar_moeda(produto.preco_venda)}")
                self.label_ultimo_valor.config(text=Formatters.formatar_moeda(quantidade * produto.preco_venda))
                self.entry_codigo.delete(0, tk.END)
                self.quantidade_digitada = ""
                self.label_quantidade.config(text="")
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", f"Produto não encontrado: {codigo}")
    
    def atualizar_lista_produtos(self):
        """Atualiza lista."""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        venda = self.venda_service.get_venda_atual()
        if venda:
            for idx, item in enumerate(venda.itens, 1):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree_produtos.insert("", tk.END, values=(
                    idx, item.produto_codigo_barras or "", item.produto_nome or "",
                    Formatters.formatar_quantidade(item.quantidade),
                    Formatters.formatar_moeda(item.preco_unitario),
                    Formatters.formatar_moeda(item.subtotal)
                ), tags=(tag,))
        self.atualizar_totais()
    
    def atualizar_totais(self):
        """Atualiza totais."""
        venda = self.venda_service.get_venda_atual()
        if venda:
            self.label_qtd_itens.config(text=str(len(venda.itens)))
            self.label_subtotal.config(text=Formatters.formatar_moeda(venda.subtotal))
            self.label_desconto.config(text=Formatters.formatar_moeda(venda.desconto))
            self.label_total.config(text=Formatters.formatar_moeda(venda.total))
    
    def buscar_produto(self, termo=""):
        """Abre busca."""
        from src.ui.caixa.busca_produto_window import BuscaProdutoWindow
        BuscaProdutoWindow(self, termo or self.entry_codigo.get(), self.adicionar_produto_busca)
    
    def adicionar_produto_busca(self, produto):
        """Adiciona produto da busca."""
        # Adiciona com quantidade 1 por padrão
        from decimal import Decimal
        qtd = Decimal("1")
        sucesso, msg = self.venda_service.adicionar_produto(produto, qtd)
        if sucesso:
            self.atualizar_lista_produtos()
            self.label_ultimo_produto.config(text=f"{produto.nome}\n{qtd} x {Formatters.formatar_moeda(produto.preco_venda)}")
            self.label_ultimo_valor.config(text=Formatters.formatar_moeda(qtd * produto.preco_venda))
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.focus()
            self.mostrar_mensagem_temporaria(f"✅ {produto.nome} adicionado", "#27ae60")
        else:
            self.mostrar_mensagem_temporaria(f"❌ {msg}", "#e74c3c")
    
    def solicitar_quantidade(self):
        """F3 - Solicita quantidade."""
        d = tk.Toplevel(self)
        d.title("Quantidade")
        d.geometry("300x150")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text="Digite a Quantidade:", font=("Arial", 12)).pack(pady=(0, 10))
        
        e = ttk.Entry(f, font=("Arial", 14), width=15)
        e.pack(pady=(0, 20))
        e.focus()
        
        def ok():
            if e.get().strip():
                self.quantidade_digitada = e.get().strip()
                self.label_quantidade.config(text=f"Qtd: {self.quantidade_digitada} X")
            d.destroy()
            self.entry_codigo.focus()
        
        tk.Button(f, text="Confirmar", font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
                  cursor="hand2", relief=tk.FLAT, padx=30, pady=10, command=ok).pack()
        e.bind('<Return>', lambda ev: ok())
    
    def solicitar_quantidade_para_produto(self, produto):
        """Solicita quantidade para produto específico."""
        d = tk.Toplevel(self)
        d.title("Quantidade")
        d.geometry("350x200")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text=produto.nome, font=("Arial", 12, "bold")).pack(pady=(0, 10))
        tk.Label(f, text="Digite a Quantidade:", font=("Arial", 11)).pack(pady=(0, 10))
        
        e = ttk.Entry(f, font=("Arial", 14), width=15)
        e.pack(pady=(0, 20))
        e.insert(0, "1")
        e.select_range(0, tk.END)
        e.focus()
        
        def ok():
            try:
                qtd = Decimal(e.get().replace(',', '.'))
                sucesso, msg = self.venda_service.adicionar_produto(produto, qtd)
                if sucesso:
                    self.atualizar_lista_produtos()
                    self.label_ultimo_produto.config(text=f"{produto.nome}\n{qtd} x {Formatters.formatar_moeda(produto.preco_venda)}")
                    self.label_ultimo_valor.config(text=Formatters.formatar_moeda(qtd * produto.preco_venda))
                    d.destroy()
                    self.entry_codigo.delete(0, tk.END)
                    self.entry_codigo.focus()
                else:
                    messagebox.showerror("Erro", msg)
            except:
                messagebox.showerror("Erro", "Quantidade inválida!")
        
        tk.Button(f, text="Confirmar", font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
                  cursor="hand2", relief=tk.FLAT, padx=30, pady=10, command=ok).pack()
        e.bind('<Return>', lambda ev: ok())
    
    def remover_item_selecionado(self):
        """F5 - Remove item."""
        sel = self.tree_produtos.selection()
        if not sel:
            itens = self.tree_produtos.get_children()
            if itens:
                self.tree_produtos.selection_set(itens[-1])
                sel = self.tree_produtos.selection()
            else:
                return
        
        idx = self.tree_produtos.index(sel[0])
        sucesso, _ = self.venda_service.remover_item(idx)
        if sucesso:
            self.atualizar_lista_produtos()
        self.entry_codigo.focus()
    
    def aplicar_desconto(self):
        """F4 - Aplica desconto."""
        d = tk.Toplevel(self)
        d.title("Desconto")
        d.geometry("350x180")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text="💰 Desconto", font=("Arial", 16, "bold"), fg="#e74c3c").pack(pady=(0, 15))
        tk.Label(f, text="Valor do Desconto:", font=("Arial", 11)).pack(pady=(0, 10))
        
        e = ttk.Entry(f, font=("Arial", 14), width=15)
        e.pack(pady=(0, 20))
        e.insert(0, "0.00")
        e.select_range(0, tk.END)
        e.focus()
        
        def ok():
            try:
                desc = Decimal(e.get().replace(',', '.'))
                sucesso, msg = self.venda_service.aplicar_desconto(desc)
                if sucesso:
                    self.atualizar_totais()
                    d.destroy()
                    self.entry_codigo.focus()
                else:
                    messagebox.showerror("Erro", msg)
            except:
                messagebox.showerror("Erro", "Valor inválido!")
        
        tk.Button(f, text="Confirmar", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white",
                  cursor="hand2", relief=tk.FLAT, padx=30, pady=10, command=ok).pack()
        e.bind('<Return>', lambda ev: ok())
    
    def cancelar_venda(self):
        """F6 - Cancela venda."""
        venda = self.venda_service.get_venda_atual()
        if venda and len(venda.itens) > 0:
            if messagebox.askyesno("Confirmar", "Deseja cancelar a venda atual?"):
                self.venda_service.cancelar_venda()
                self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id)
                self.atualizar_lista_produtos()
                self.label_ultimo_produto.config(text="-")
                self.label_ultimo_valor.config(text="R$ 0,00")
        self.entry_codigo.focus()
    
    def finalizar_venda(self):
        """F10 - Finaliza venda."""
        # Fechar janela de busca se estiver aberta
        for child in self.winfo_children():
            if isinstance(child, tk.Toplevel) and "Buscar" in child.title():
                child.destroy()
        
        venda = self.venda_service.get_venda_atual()
        if not venda or len(venda.itens) == 0:
            # Mostrar mensagem na própria tela em vez de popup
            self.mostrar_mensagem_temporaria("⚠️ ADICIONE PRODUTOS À VENDA", "#e74c3c")
            return
        
        # Mostrar área de pagamento integrada em vez de popup
        self.mostrar_area_pagamento()
    
    def callback_venda_finalizada(self):
        """Callback após venda finalizada."""
        self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id)
        self.atualizar_lista_produtos()
        self.label_ultimo_produto.config(text="-")
        self.label_ultimo_valor.config(text="R$ 0,00")
        self.entry_codigo.focus()
    
    def mostrar_area_pagamento(self):
        """Mostra área de pagamento integrada na própria tela."""
        # Esconde o painel de entrada
        for widget in self.painel_esquerdo.winfo_children():
            if hasattr(widget, 'pack_info'):
                widget.pack_forget()
        
        # Criar área de pagamento no painel esquerdo
        self.criar_area_pagamento_integrada()
        
        # Foco na primeira opção de pagamento
        self.opcoes_pagamento[0].focus_set()
    
    def criar_area_pagamento_integrada(self):
        """Cria área de pagamento integrada."""
        # Frame principal do pagamento
        frame_pagamento = tk.Frame(self.painel_esquerdo, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame_pagamento.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_frame = tk.Frame(frame_pagamento, bg="#27ae60", height=50)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="💳 FINALIZAR VENDA", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white").pack(expand=True)
        
        # Valor total
        total_frame = tk.Frame(frame_pagamento, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(total_frame, text="TOTAL A PAGAR", font=("Arial", 12, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(pady=(10, 5))
        
        venda = self.venda_service.get_venda_atual()
        tk.Label(total_frame, text=f"R$ {float(venda.total):.2f}", font=("Arial", 24, "bold"),
                 bg="#ecf0f1", fg="#27ae60").pack(pady=(0, 10))
        
        # Opções de pagamento
        opcoes_frame = tk.Frame(frame_pagamento, bg="#ffffff")
        opcoes_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(opcoes_frame, text="ESCOLHA A FORMA DE PAGAMENTO:", font=("Arial", 12, "bold"),
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 15))
        
        # Botões de pagamento
        self.opcoes_pagamento = []
        
        # F1 - Dinheiro
        btn_dinheiro = tk.Button(opcoes_frame, text="F1 - 💵 DINHEIRO", font=("Arial", 14, "bold"),
                                bg="#27ae60", fg="white", relief=tk.FLAT, pady=15,
                                command=lambda: self.processar_pagamento("dinheiro"))
        btn_dinheiro.pack(fill=tk.X, pady=5)
        self.opcoes_pagamento.append(btn_dinheiro)
        
        # F2 - Débito
        btn_debito = tk.Button(opcoes_frame, text="F2 - 💳 CARTÃO DÉBITO", font=("Arial", 14, "bold"),
                              bg="#3498db", fg="white", relief=tk.FLAT, pady=15,
                              command=lambda: self.processar_pagamento("debito"))
        btn_debito.pack(fill=tk.X, pady=5)
        self.opcoes_pagamento.append(btn_debito)
        
        # F3 - Crédito
        btn_credito = tk.Button(opcoes_frame, text="F3 - 💳 CARTÃO CRÉDITO", font=("Arial", 14, "bold"),
                               bg="#9b59b6", fg="white", relief=tk.FLAT, pady=15,
                               command=lambda: self.processar_pagamento("credito"))
        btn_credito.pack(fill=tk.X, pady=5)
        self.opcoes_pagamento.append(btn_credito)
        
        # F4 - PIX
        btn_pix = tk.Button(opcoes_frame, text="F4 - 📱 PIX MERCADO PAGO", font=("Arial", 14, "bold"),
                           bg="#16a085", fg="white", relief=tk.FLAT, pady=15,
                           command=lambda: self.processar_pagamento("pix"))
        btn_pix.pack(fill=tk.X, pady=5)
        self.opcoes_pagamento.append(btn_pix)
        
        # Status do pagamento
        self.status_pagamento = tk.Label(frame_pagamento, text="⌨️ Use F1-F4 para escolher | ↑↓ para navegar | ESC para voltar",
                                        font=("Arial", 10), bg="#ffffff", fg="#7f8c8d")
        self.status_pagamento.pack(pady=10)
        
        # Botões de ação
        acoes_frame = tk.Frame(frame_pagamento, bg="#ffffff")
        acoes_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Button(acoes_frame, text="ESC - VOLTAR", font=("Arial", 12, "bold"),
                  bg="#95a5a6", fg="white", relief=tk.FLAT, pady=10,
                  command=self.voltar_para_venda).pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(acoes_frame, text="F9 - CANCELAR VENDA", font=("Arial", 12, "bold"),
                  bg="#e74c3c", fg="white", relief=tk.FLAT, pady=10,
                  command=self.cancelar_venda).pack(fill=tk.X)
        
        # Configurar navegação por teclado
        self.configurar_navegacao_pagamento()
    
    def configurar_navegacao_pagamento(self):
        """Configura navegação por teclado na área de pagamento."""
        # Remover bindings anteriores
        self.unbind_all('<F1>')
        self.unbind_all('<F2>')
        self.unbind_all('<F3>')
        self.unbind_all('<F4>')
        
        # Novos bindings para pagamento
        self.bind_all('<F1>', lambda e: self.processar_pagamento("dinheiro"))
        self.bind_all('<F2>', lambda e: self.processar_pagamento("debito"))
        self.bind_all('<F3>', lambda e: self.processar_pagamento("credito"))
        self.bind_all('<F4>', lambda e: self.processar_pagamento("pix"))
        self.bind_all('<Escape>', lambda e: self.voltar_para_venda())
        self.bind_all('<F9>', lambda e: self.cancelar_venda())
        
        # Navegação com setas
        self.bind_all('<Up>', self._navegar_pagamento_cima)
        self.bind_all('<Down>', self._navegar_pagamento_baixo)
        self.bind_all('<Return>', self._executar_pagamento_selecionado)
    
    def _navegar_pagamento_cima(self, event):
        """Navega para cima nas opções de pagamento."""
        focused = self.focus_get()
        try:
            index = self.opcoes_pagamento.index(focused)
            if index > 0:
                self.opcoes_pagamento[index - 1].focus_set()
        except (ValueError, AttributeError):
            self.opcoes_pagamento[-1].focus_set()
        return "break"
    
    def _navegar_pagamento_baixo(self, event):
        """Navega para baixo nas opções de pagamento."""
        focused = self.focus_get()
        try:
            index = self.opcoes_pagamento.index(focused)
            if index < len(self.opcoes_pagamento) - 1:
                self.opcoes_pagamento[index + 1].focus_set()
        except (ValueError, AttributeError):
            self.opcoes_pagamento[0].focus_set()
        return "break"
    
    def _executar_pagamento_selecionado(self, event):
        """Executa o pagamento do botão selecionado."""
        focused = self.focus_get()
        if focused in self.opcoes_pagamento:
            focused.invoke()
        return "break"
    
    def mostrar_mensagem_temporaria(self, mensagem, cor="#e74c3c"):
        """Mostra mensagem temporária na tela."""
        # Usar o status label existente para mostrar mensagem
        original_text = self.label_status.cget("text")
        original_bg = self.label_status.cget("bg")
        
        self.label_status.config(text=mensagem, bg=cor, fg="white")
        self.after(3000, lambda: self.label_status.config(text=original_text, bg=original_bg, fg="black"))
    
    def processar_pagamento(self, tipo):
        """Processa pagamento do tipo especificado."""
        venda = self.venda_service.get_venda_atual()
        
        if tipo == "dinheiro":
            self.processar_dinheiro(venda)
        elif tipo == "debito":
            self.processar_debito(venda)
        elif tipo == "credito":
            self.processar_credito(venda)
        elif tipo == "pix":
            self.processar_pix_mercado_pago(venda)
    
    def processar_dinheiro(self, venda):
        """Processa pagamento em dinheiro."""
        # Por simplicidade, considera valor exato
        from src.models.pagamento import Pagamento
        pagamento = Pagamento(
            forma_pagamento=Pagamento.FORMA_DINHEIRO,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            self.finalizar_venda_com_sucesso()
        else:
            self.status_pagamento.config(text=f"❌ Erro: {mensagem}", fg="#e74c3c")
    
    def processar_debito(self, venda):
        """Processa pagamento no débito."""
        self.status_pagamento.config(text="💳 Processando cartão de débito...", fg="#3498db")
        
        # Simula processamento
        self.after(2000, lambda: self._finalizar_cartao(venda, "debito"))
    
    def processar_credito(self, venda):
        """Processa pagamento no crédito."""
        self.status_pagamento.config(text="💳 Processando cartão de crédito...", fg="#9b59b6")
        
        # Simula processamento
        self.after(2000, lambda: self._finalizar_cartao(venda, "credito"))
    
    def _finalizar_cartao(self, venda, tipo):
        """Finaliza processamento do cartão."""
        from src.models.pagamento import Pagamento
        
        forma = Pagamento.FORMA_DEBITO if tipo == "debito" else Pagamento.FORMA_CREDITO
        
        pagamento = Pagamento(
            forma_pagamento=forma,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO,
            nsu="123456",
            codigo_autorizacao="789012"
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            self.finalizar_venda_com_sucesso()
        else:
            self.status_pagamento.config(text=f"❌ Erro: {mensagem}", fg="#e74c3c")
    
    def processar_pix_mercado_pago(self, venda):
        """Processa PIX via Mercado Pago."""
        try:
            from src.services.mercado_pago_service import MercadoPagoService
            from src.ui.caixa.pix_frame import PIXFrame
            
            self.status_pagamento.config(text="📱 Gerando PIX...", fg="#16a085")
            
            # Instanciar o serviço Mercado Pago
            mp_service = MercadoPagoService()
            
            # Criar pagamento PIX
            payment_data = mp_service.criar_pagamento_pix(
                valor=float(venda.total),
                descricao=f"Venda PDV #{venda.numero}"
            )
            
            if payment_data:
                # Mostrar interface PIX
                self.mostrar_pix_interface(payment_data, venda)
            else:
                self.status_pagamento.config(text="❌ Erro ao gerar PIX", fg="#e74c3c")
                
        except Exception as e:
            self.status_pagamento.config(text=f"❌ Erro PIX: {str(e)}", fg="#e74c3c")
    
    def mostrar_pix_interface(self, payment_data, venda):
        """Mostra interface PIX integrada."""
        # Limpar área de pagamento
        for widget in self.painel_esquerdo.winfo_children():
            widget.destroy()
        
        # Criar frame PIX
        try:
            from src.ui.caixa.pix_frame import PIXFrame
            
            self.pix_frame = PIXFrame(
                parent=self.painel_esquerdo,
                payment_data=payment_data,
                callback_aprovado=lambda: self.pix_aprovado(venda),
                callback_cancelado=self.voltar_para_venda
            )
            self.pix_frame.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"Erro ao criar PIX frame: {e}")
            self.voltar_para_venda()
    
    def pix_aprovado(self, venda):
        """Callback quando PIX é aprovado."""
        from src.models.pagamento import Pagamento
        
        pagamento = Pagamento(
            forma_pagamento=Pagamento.FORMA_PIX,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            self.finalizar_venda_com_sucesso()
        else:
            self.mostrar_mensagem_temporaria(f"Erro: {mensagem}", "#e74c3c")
    
    def finalizar_venda_com_sucesso(self):
        """Finaliza venda com sucesso e pergunta sobre cupom."""
        # Limpar área de pagamento
        for widget in self.painel_esquerdo.winfo_children():
            widget.destroy()
        
        # Mostrar pergunta sobre cupom
        self.mostrar_pergunta_cupom()
    
    def mostrar_pergunta_cupom(self):
        """Mostra pergunta sobre imprimir cupom não fiscal."""
        frame_cupom = tk.Frame(self.painel_esquerdo, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame_cupom.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_frame = tk.Frame(frame_cupom, bg="#27ae60", height=50)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="✅ VENDA FINALIZADA!", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white").pack(expand=True)
        
        # Conteúdo
        content_frame = tk.Frame(frame_cupom, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(content_frame, text="🎉 Venda realizada com sucesso!", font=("Arial", 16, "bold"),
                 bg="#ffffff", fg="#27ae60").pack(pady=(0, 20))
        
        tk.Label(content_frame, text="Deseja imprimir cupom não fiscal?", font=("Arial", 14),
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 30))
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg="#ffffff")
        botoes_frame.pack(fill=tk.X)
        
        btn_sim = tk.Button(botoes_frame, text="F1 - SIM", font=("Arial", 14, "bold"),
                           bg="#27ae60", fg="white", relief=tk.FLAT, pady=15,
                           command=self.imprimir_cupom)
        btn_sim.pack(fill=tk.X, pady=(0, 10))
        
        btn_nao = tk.Button(botoes_frame, text="F2 - NÃO", font=("Arial", 14, "bold"),
                           bg="#95a5a6", fg="white", relief=tk.FLAT, pady=15,
                           command=self.nova_venda)
        btn_nao.pack(fill=tk.X)
        
        # Status
        tk.Label(content_frame, text="⌨️ F1 = Imprimir | F2 = Próxima venda", font=("Arial", 10),
                 bg="#ffffff", fg="#7f8c8d").pack(pady=(20, 0))
        
        # Configurar navegação
        self.bind_all('<F1>', lambda e: self.imprimir_cupom())
        self.bind_all('<F2>', lambda e: self.nova_venda())
        
        # Auto-foco no primeiro botão
        btn_sim.focus_set()
    
    def imprimir_cupom(self):
        """Simula impressão do cupom não fiscal."""
        self.mostrar_mensagem_temporaria("🖨️ Cupom impresso!", "#27ae60")
        self.after(2000, self.nova_venda)
    
    def nova_venda(self):
        """Inicia nova venda."""
        self.voltar_para_venda()
        self.callback_venda_finalizada()
    
    def voltar_para_venda(self):
        """Volta para a tela de venda."""
        # Limpar área de pagamento/pix/cupom
        for widget in self.painel_esquerdo.winfo_children():
            widget.destroy()
        
        # Recriar widgets originais
        self.criar_barra_atalhos(self.painel_esquerdo)
        self.criar_campo_entrada(self.painel_esquerdo)
        self.criar_lista_produtos(self.painel_esquerdo)
        
        # Restaurar bindings originais
        self.configurar_atalhos()
        
        # Voltar foco para entrada
        self.entry_codigo.focus()
    
    # ==================== MÉTODOS DE NAVEGAÇÃO ====================
    
    def limpar_campo_codigo(self):
        """Limpa o campo de código e volta foco para ele."""
        self.entry_codigo.delete(0, tk.END)
        self.quantity_multiplier = ""
        self.label_quantidade.config(text="")
        self.entry_codigo.focus()
        return 'break'
    
    def _navegar_proximo(self, event=None):
        """Navega para o próximo widget focalizável."""
        if event:
            # Se estiver no campo de código, vai para a lista
            if event.widget == self.entry_codigo:
                self._focar_lista_produtos()
            else:
                event.widget.tk_focusNext().focus()
            return 'break'
    
    def _navegar_anterior(self, event=None):
        """Navega para o widget anterior."""
        if event:
            # Se estiver na lista, volta para o campo de código
            if event.widget == self.tree_produtos:
                self.entry_codigo.focus()
            else:
                event.widget.tk_focusPrev().focus()
            return 'break'
    
    def _focar_lista_produtos(self):
        """Foca na lista de produtos."""
        self.tree_produtos.focus()
        # Se não há seleção, seleciona o primeiro item
        if not self.tree_produtos.selection():
            items = self.tree_produtos.get_children()
            if items:
                self.tree_produtos.selection_set(items[0])
                self.tree_produtos.focus(items[0])
    
    def _navegar_lista_cima(self, event=None):
        """Navega para cima na lista de produtos."""
        # Só funciona se o foco estiver na lista ou campo de código
        if hasattr(event, 'widget') and event.widget not in [self.tree_produtos, self.entry_codigo]:
            return
        
        if not self.tree_produtos.focus():
            self._focar_lista_produtos()
            return 'break'
        
        # Se há seleção, move para cima
        current = self.tree_produtos.focus()
        if current:
            prev_item = self.tree_produtos.prev(current)
            if prev_item:
                self.tree_produtos.selection_set(prev_item)
                self.tree_produtos.focus(prev_item)
                self.tree_produtos.see(prev_item)
        return 'break'
    
    def _navegar_lista_baixo(self, event=None):
        """Navega para baixo na lista de produtos."""
        # Só funciona se o foco estiver na lista ou campo de código
        if hasattr(event, 'widget') and event.widget not in [self.tree_produtos, self.entry_codigo]:
            return
        
        if not self.tree_produtos.focus():
            self._focar_lista_produtos()
            return 'break'
        
        # Se há seleção, move para baixo
        current = self.tree_produtos.focus()
        if current:
            next_item = self.tree_produtos.next(current)
            if next_item:
                self.tree_produtos.selection_set(next_item)
                self.tree_produtos.focus(next_item)
                self.tree_produtos.see(next_item)
        return 'break'
    
    def _ir_primeiro_item(self, event=None):
        """Vai para o primeiro item da lista."""
        items = self.tree_produtos.get_children()
        if items:
            self.tree_produtos.selection_set(items[0])
            self.tree_produtos.focus(items[0])
            self.tree_produtos.see(items[0])
        return 'break'
    
    def _ir_ultimo_item(self, event=None):
        """Vai para o último item da lista."""
        items = self.tree_produtos.get_children()
        if items:
            last_item = items[-1]
            self.tree_produtos.selection_set(last_item)
            self.tree_produtos.focus(last_item)
            self.tree_produtos.see(last_item)
        return 'break'
    
    def _pagina_cima(self, event=None):
        """Navega uma página para cima."""
        items = self.tree_produtos.get_children()
        if not items:
            return 'break'
        
        current = self.tree_produtos.focus()
        if current:
            current_index = items.index(current)
            # Move 10 itens para cima (ou vai para o primeiro)
            new_index = max(0, current_index - 10)
            new_item = items[new_index]
            self.tree_produtos.selection_set(new_item)
            self.tree_produtos.focus(new_item)
            self.tree_produtos.see(new_item)
        return 'break'
    
    def _pagina_baixo(self, event=None):
        """Navega uma página para baixo."""
        items = self.tree_produtos.get_children()
        if not items:
            return 'break'
        
        current = self.tree_produtos.focus()
        if current:
            current_index = items.index(current)
            # Move 10 itens para baixo (ou vai para o último)
            new_index = min(len(items) - 1, current_index + 10)
            new_item = items[new_index]
            self.tree_produtos.selection_set(new_item)
            self.tree_produtos.focus(new_item)
            self.tree_produtos.see(new_item)
        return 'break'
