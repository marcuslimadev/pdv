"""
Janela de busca de produtos.
"""

import tkinter as tk
from tkinter import ttk

from src.dao.produto_dao import ProdutoDAO


class BuscaProdutoWindow:
    """Janela para buscar produtos."""
    
    def __init__(self, parent, termo_busca="", callback=None):
        self.callback = callback
        
        # Cria janela
        self.window = tk.Toplevel(parent)
        self.window.title("Buscar Produto")
        self.window.geometry("800x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.criar_widgets()
        
        # Se tem termo de busca, executa
        if termo_busca:
            self.entry_busca.insert(0, termo_busca)
            self.buscar()
        
        self.entry_busca.focus()
    
    def criar_widgets(self):
        """Cria os widgets."""
        # Container principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="🔍 Buscar Produto",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        ).pack(pady=(0, 15))
        
        # Busca
        busca_frame = ttk.Frame(main_frame)
        busca_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            busca_frame,
            text="Nome ou Código:",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_busca = ttk.Entry(busca_frame, font=("Arial", 12))
        self.entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_busca.bind('<Return>', lambda e: self.buscar())
        
        tk.Button(
            busca_frame,
            text="Buscar",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            command=self.buscar
        ).pack(side=tk.LEFT)
        
        # Tabela
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("codigo", "nome", "preco", "estoque"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("estoque", text="Estoque")
        
        self.tree.column("codigo", width=120)
        self.tree.column("nome", width=350)
        self.tree.column("preco", width=100)
        self.tree.column("estoque", width=80)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Navegação por teclado
        self.tree.bind('<Double-1>', lambda e: self.selecionar())
        self.tree.bind('<Return>', lambda e: self.selecionar())
        self.tree.bind('<Up>', self._navegar_cima)
        self.tree.bind('<Down>', self._navegar_baixo)
        self.tree.bind('<space>', lambda e: self.selecionar())  # Espaço também seleciona
        
        # Atalhos globais
        self.window.bind('<Escape>', lambda e: self.window.destroy())
        self.window.bind('<F1>', lambda e: self.selecionar())
        self.window.bind('<Return>', self._handle_enter)
        
        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Status de navegação
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(
            status_frame,
            text="⌨️ NAVEGAÇÃO: ↑↓ = Navegar | ENTER = Selecionar | F1 = Selecionar | ESC = Cancelar",
            font=("Arial", 9),
            fg="#7f8c8d"
        ).pack()
        
        tk.Button(
            btn_frame,
            text="ESC - Cancelar",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=8,
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            btn_frame,
            text="F1/ENTER - Selecionar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=8,
            command=self.selecionar
        ).pack(side=tk.RIGHT)
    
    def buscar(self):
        """Executa a busca."""
        termo = self.entry_busca.get().strip()
        
        # Limpa árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not termo:
            produtos = ProdutoDAO.buscar_todos()[:50]  # Limita a 50
        else:
            # Tenta buscar por código
            produto = ProdutoDAO.buscar_por_codigo_barras(termo)
            if produto:
                produtos = [produto]
            else:
                # Busca por nome
                produtos = ProdutoDAO.buscar_por_nome(termo)
        
        # Adiciona produtos
        for produto in produtos:
            self.tree.insert("", tk.END, values=(
                produto.codigo_barras or "",
                produto.nome,
                f"R$ {float(produto.preco_venda):.2f}",
                produto.estoque_atual
            ), tags=(produto.id,))
        
        # Auto-seleciona o primeiro item se houver resultados
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus_set()  # Foco na tree
            self.tree.focus(children[0])
            self.tree.see(children[0])
        
        # NÃO seleciona automaticamente - deixa usuário escolher
    
    def _navegar_cima(self, event):
        """Navega para cima na lista."""
        current = self.tree.selection()
        if current:
            prev_item = self.tree.prev(current[0])
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.see(prev_item)
        else:
            # Se nada selecionado, seleciona o último
            children = self.tree.get_children()
            if children:
                self.tree.selection_set(children[-1])
                self.tree.see(children[-1])
        return "break"
    
    def _navegar_baixo(self, event):
        """Navega para baixo na lista."""
        current = self.tree.selection()
        if current:
            next_item = self.tree.next(current[0])
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.see(next_item)
        else:
            # Se nada selecionado, seleciona o primeiro
            children = self.tree.get_children()
            if children:
                self.tree.selection_set(children[0])
                self.tree.see(children[0])
        return "break"
    
    def _handle_enter(self, event):
        """Trata Enter baseado no foco atual."""
        focused = self.window.focus_get()
        focused_class = focused.__class__.__name__ if focused else "None"
        
        print(f"Enter pressionado, foco em: {focused} (classe: {focused_class})")
        
        # Se está no campo de busca, executa busca
        if focused == self.entry_busca:
            print("Foco no campo de busca - executando busca")
            self.buscar()
            return "break"
        
        # Se está na árvore (lista), seleciona produto
        if focused_class == 'Treeview' or focused == self.tree:
            print("Foco na lista - selecionando produto")
            self.selecionar()
            return "break"
        
        # Se não conseguir identificar, verifica se há seleção na tree
        selecionado = self.tree.selection()
        if selecionado:
            print("Há item selecionado na lista - selecionando produto")
            self.selecionar()
        else:
            print("Nenhum contexto claro - tentando buscar")
            self.buscar()
        
        return "break"
    
    def selecionar(self):
        """Seleciona o produto."""
        children = self.tree.get_children()
        if not children:
            print("Nenhum produto na lista")
            return
        
        selecionado = self.tree.selection()
        
        if not selecionado:
            # Se nada selecionado, seleciona o primeiro item
            self.tree.selection_set(children[0])
            selecionado = self.tree.selection()
        
        if selecionado:
            try:
                # Pega o ID do produto
                produto_id = int(self.tree.item(selecionado[0])['tags'][0])
                produto = ProdutoDAO.buscar_por_id(produto_id)
                
                print(f"Produto selecionado: {produto.nome if produto else 'Não encontrado'}")
                
                if produto and self.callback:
                    self.callback(produto)
                
                self.window.destroy()
            except Exception as e:
                print(f"Erro ao selecionar produto: {e}")
        else:
            print("Não foi possível selecionar produto")
