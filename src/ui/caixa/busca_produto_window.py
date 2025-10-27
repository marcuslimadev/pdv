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
        
        # Double click para selecionar
        self.tree.bind('<Double-1>', lambda e: self.selecionar())
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=8,
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Selecionar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
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
    
    def selecionar(self):
        """Seleciona o produto."""
        selecionado = self.tree.selection()
        
        if not selecionado:
            return
        
        # Pega o ID do produto
        produto_id = int(self.tree.item(selecionado[0])['tags'][0])
        produto = ProdutoDAO.buscar_por_id(produto_id)
        
        if produto and self.callback:
            self.callback(produto)
        
        self.window.destroy()
