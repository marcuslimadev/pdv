"""
Painel inline de busca de produtos (substitui janela popup).
"""

import tkinter as tk
from tkinter import ttk

from src.dao.produto_dao import ProdutoDAO


class BuscaProdutoPanel(tk.Frame):
    """Painel inline para buscar produtos."""
    
    def __init__(self, parent, callback=None):
        super().__init__(parent, bg="#ffffff", relief=tk.RAISED, bd=3)
        self.callback = callback
        self.produtos_cache = []
        
        self.criar_widgets()
        
    def criar_widgets(self):
        """Cria os widgets."""
        # Cabeçalho
        header = tk.Frame(self, bg="#3498db", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔍 BUSCAR PRODUTO",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(side=tk.LEFT, padx=20, expand=True)
        
        tk.Button(
            header,
            text="✕",
            font=("Arial", 16, "bold"),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            width=3,
            command=self.ocultar
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Corpo
        body = tk.Frame(self, bg="#ffffff")
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Campo de busca
        busca_frame = tk.Frame(body, bg="#ffffff")
        busca_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            busca_frame,
            text="Nome ou Código:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_busca = tk.Entry(
            busca_frame,
            font=("Arial", 14),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief=tk.FLAT,
            insertwidth=3
        )
        self.entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.entry_busca.bind('<Return>', lambda e: self.buscar())
        self.entry_busca.bind('<Escape>', lambda e: self.ocultar())
        self.entry_busca.bind('<KeyRelease>', self.filtrar_ao_digitar)
        self.entry_busca.bind('<Down>', lambda e: self._focar_tree())
        self.entry_busca.bind('<Up>', lambda e: self._focar_tree())
        
        tk.Button(
            busca_frame,
            text="🔍 BUSCAR",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.buscar
        ).pack(side=tk.LEFT)
        
        # Tabela
        tree_frame = tk.Frame(body, bg="#ffffff")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("codigo", "nome", "preco", "estoque"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("estoque", text="Estoque")
        
        self.tree.column("codigo", width=120)
        self.tree.column("nome", width=400)
        self.tree.column("preco", width=120, anchor=tk.E)
        self.tree.column("estoque", width=100, anchor=tk.CENTER)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Eventos de navegação
        self.tree.bind('<Double-1>', lambda e: self.selecionar())
        self.tree.bind('<Return>', lambda e: self.selecionar())
        self.tree.bind('<space>', lambda e: self.selecionar())
        self.tree.bind('<Up>', self._navegar_tree_cima)
        self.tree.bind('<Down>', self._navegar_tree_baixo)
        self.tree.bind('<Escape>', lambda e: self.ocultar())
        
        # Rodapé com instruções
        footer = tk.Frame(body, bg="#ecf0f1", relief=tk.RAISED, bd=1)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            footer,
            text="⌨️ ENTER = Selecionar | ESC = Fechar | ↑↓ = Navegar",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(pady=8)
        
    def mostrar(self, termo_busca=""):
        """Mostra o painel e executa busca."""
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.entry_busca.delete(0, tk.END)
        
        if termo_busca:
            self.entry_busca.insert(0, termo_busca)
            self.buscar()
        else:
            # Mostra produtos populares/recentes
            self.buscar()
        
        self.entry_busca.focus_set()
        self.lift()
    
    def ocultar(self):
        """Oculta o painel."""
        self.pack_forget()
        # Notifica o callback com None para indicar cancelamento
        if self.callback:
            self.callback(None)
    
    def buscar(self):
        """Executa a busca."""
        termo = self.entry_busca.get().strip()
        
        # Limpa árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not termo:
            # Sem termo: mostra todos (limitado)
            produtos = ProdutoDAO.buscar_todos()[:50]
        else:
            # Tenta buscar por código exato
            produto = ProdutoDAO.buscar_por_codigo_barras(termo)
            if produto:
                produtos = [produto]
            else:
                # Busca por nome
                produtos = ProdutoDAO.buscar_por_nome(termo)
        
        self.produtos_cache = produtos
        
        # Popula árvore
        from src.utils.formatters import Formatters
        for produto in produtos:
            self.tree.insert("", tk.END, values=(
                produto.codigo_barras or "",
                produto.nome,
                Formatters.formatar_moeda(produto.preco_venda),
                produto.estoque_atual
            ), tags=(produto.id,))
        
        # Auto-seleciona o primeiro
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus_set()
            self.tree.focus(children[0])
            self.tree.see(children[0])
            
            # Se for busca por código exato com 1 resultado, seleciona automaticamente
            if termo and len(produtos) == 1:
                self.after(100, self.selecionar)
    
    def _focar_tree(self):
        """Foca na tree quando setas são pressionadas no campo de busca."""
        children = self.tree.get_children()
        if children:
            self.tree.focus_set()
            if not self.tree.selection():
                self.tree.selection_set(children[0])
                self.tree.focus(children[0])
            self.tree.see(self.tree.selection()[0] if self.tree.selection() else children[0])
        return "break"
    
    def _navegar_tree_cima(self, event):
        """Navega para cima na tree."""
        current = self.tree.selection()
        if current:
            prev_item = self.tree.prev(current[0])
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.focus(prev_item)
                self.tree.see(prev_item)
            else:
                # Está no topo, volta para o campo de busca
                self.entry_busca.focus_set()
        return "break"
    
    def _navegar_tree_baixo(self, event):
        """Navega para baixo na tree."""
        current = self.tree.selection()
        if current:
            next_item = self.tree.next(current[0])
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.focus(next_item)
                self.tree.see(next_item)
        return "break"
    
    def filtrar_ao_digitar(self, event=None):
        """Filtra produtos em tempo real ao digitar."""
        # Ignora teclas especiais
        if event and event.keysym in ('Up', 'Down', 'Left', 'Right', 'Escape', 'Return', 
                                       'Tab', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R',
                                       'Alt_L', 'Alt_R', 'Caps_Lock'):
            return
        
        # Executa busca automaticamente após pequeno delay
        if hasattr(self, '_filtro_timer'):
            self.after_cancel(self._filtro_timer)
        
        self._filtro_timer = self.after(300, self.buscar)  # 300ms delay
    
    def selecionar(self):
        """Seleciona o produto."""
        selecionado = self.tree.selection()
        
        if not selecionado:
            # Sem seleção, pega o primeiro
            children = self.tree.get_children()
            if children:
                selecionado = [children[0]]
            else:
                return
        
        try:
            # Pega o ID do produto
            produto_id = int(self.tree.item(selecionado[0])['tags'][0])
            produto = ProdutoDAO.buscar_por_id(produto_id)
            
            if produto:
                self.ocultar()
                if self.callback:
                    self.callback(produto)
        except Exception as e:
            print(f"Erro ao selecionar produto: {e}")
