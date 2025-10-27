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
        """Configura atalhos F2-F10."""
        self.bind_all('<F2>', lambda e: self.buscar_produto())
        self.bind_all('<F3>', lambda e: self.solicitar_quantidade())
        self.bind_all('<F4>', lambda e: self.aplicar_desconto())
        self.bind_all('<F5>', lambda e: self.remover_item_selecionado())
        self.bind_all('<F6>', lambda e: self.cancelar_venda())
        self.bind_all('<F9>', lambda e: self.callback_fechar_caixa())
        self.bind_all('<F10>', lambda e: self.finalizar_venda())
        self.bind_all('<Delete>', lambda e: self.remover_item_selecionado())
        self.bind_all('<Escape>', lambda e: self.entry_codigo.delete(0, tk.END))
    
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
        self.criar_painel_direito(content)
    
    def criar_barra_atalhos(self, parent):
        """Barra com teclas F2-F10."""
        barra = tk.Frame(parent, bg="#2c3e50", height=45)
        barra.pack(fill=tk.X)
        
        atalhos = [
            ("F2", "Buscar", "#3498db"), ("F3", "Quantidade", "#f39c12"),
            ("F4", "Desconto", "#9b59b6"), ("F5", "Cancelar Item", "#e67e22"),
            ("F6", "Cancelar Venda", "#e74c3c"), ("F9", "Fechar Caixa", "#95a5a6"),
            ("F10", "FINALIZAR", "#27ae60"),
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
    
    def criar_painel_direito(self, parent):
        """Display para cliente."""
        frame = tk.Frame(parent, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame.pack(side=tk.RIGHT, fill=tk.Y)
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
        self.solicitar_quantidade_para_produto(produto)
    
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
        venda = self.venda_service.get_venda_atual()
        if not venda or len(venda.itens) == 0:
            messagebox.showwarning("Aviso", "Adicione produtos à venda!")
            return
        
        from src.ui.caixa.pagamento_window import PagamentoWindow
        PagamentoWindow(self, venda, self.callback_venda_finalizada)
    
    def callback_venda_finalizada(self):
        """Callback após venda finalizada."""
        self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id)
        self.atualizar_lista_produtos()
        self.label_ultimo_produto.config(text="-")
        self.label_ultimo_valor.config(text="R$ 0,00")
        self.entry_codigo.focus()
