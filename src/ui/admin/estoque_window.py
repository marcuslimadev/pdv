"""
Tela de gestão de estoque.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.dao.produto_dao import ProdutoDAO
from src.utils.formatters import Formatters


class EstoqueFrame(ttk.Frame):
    """Frame para gestão de estoque."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.criar_widgets()
        self.carregar_produtos()
    
    def criar_widgets(self):
        """Cria widgets."""
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="📦 Gestão de Estoque", font=("Arial", 20, "bold"),
                 fg="#2c3e50").pack(side=tk.LEFT)
        
        tk.Button(header, text="⚠️ Estoque Baixo", font=("Arial", 11),
                  bg="#e74c3c", fg="white", cursor="hand2", relief=tk.FLAT,
                  padx=20, pady=8, command=self.mostrar_estoque_baixo).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(header, text="🔄 Atualizar", font=("Arial", 11),
                  bg="#3498db", fg="white", cursor="hand2", relief=tk.FLAT,
                  padx=20, pady=8, command=self.carregar_produtos).pack(side=tk.RIGHT)
        
        # Tabela
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
            columns=("codigo", "nome", "estoque", "minimo", "status"), show="headings")
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nome", text="Produto")
        self.tree.heading("estoque", text="Estoque")
        self.tree.heading("minimo", text="Mínimo")
        self.tree.heading("status", text="Status")
        
        self.tree.column("codigo", width=120)
        self.tree.column("nome", width=350)
        self.tree.column("estoque", width=100)
        self.tree.column("minimo", width=100)
        self.tree.column("status", width=120)
        
        scroll.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<Double-1>', lambda e: self.ajustar_estoque())
        
        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(btn_frame, text="✏️ Ajustar Estoque", font=("Arial", 10),
                  bg="#27ae60", fg="white", cursor="hand2", relief=tk.FLAT,
                  padx=20, pady=8, command=self.ajustar_estoque).pack(side=tk.LEFT)
    
    def carregar_produtos(self):
        """Carrega produtos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        produtos = ProdutoDAO.buscar_todos()
        for p in produtos:
            status = "OK"
            if p.estoque_atual <= 0:
                status = "SEM ESTOQUE"
            elif p.estoque_atual <= p.estoque_minimo:
                status = "ESTOQUE BAIXO"
            
            self.tree.insert("", tk.END, values=(
                p.codigo_barras or "", p.nome, p.estoque_atual, p.estoque_minimo, status
            ), tags=(p.id,))
    
    def mostrar_estoque_baixo(self):
        """Mostra apenas produtos com estoque baixo."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        produtos = ProdutoDAO.buscar_estoque_baixo()
        for p in produtos:
            status = "SEM ESTOQUE" if p.estoque_atual <= 0 else "ESTOQUE BAIXO"
            self.tree.insert("", tk.END, values=(
                p.codigo_barras or "", p.nome, p.estoque_atual, p.estoque_minimo, status
            ), tags=(p.id,))
    
    def ajustar_estoque(self):
        """Ajusta estoque do produto."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        prod_id = int(self.tree.item(sel[0])['tags'][0])
        produto = ProdutoDAO.buscar_por_id(prod_id)
        
        if not produto:
            return
        
        d = tk.Toplevel(self)
        d.title("Ajustar Estoque")
        d.geometry("400x250")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text=produto.nome, font=("Arial", 14, "bold"),
                 fg="#2c3e50", wraplength=360).pack(pady=(0, 15))
        
        tk.Label(f, text=f"Estoque Atual: {produto.estoque_atual}",
                 font=("Arial", 12)).pack(pady=(0, 15))
        
        tk.Label(f, text="Novo Estoque:", font=("Arial", 11)).pack(pady=(0, 10))
        
        e = ttk.Entry(f, font=("Arial", 14), width=15)
        e.pack(pady=(0, 20))
        e.insert(0, str(produto.estoque_atual))
        e.select_range(0, tk.END)
        e.focus()
        
        def salvar():
            try:
                novo_estoque = int(e.get())
                if novo_estoque < 0:
                    messagebox.showerror("Erro", "Estoque não pode ser negativo!")
                    return
                
                if ProdutoDAO.atualizar_estoque(produto.id, novo_estoque):
                    messagebox.showinfo("Sucesso", "Estoque atualizado!")
                    d.destroy()
                    self.carregar_produtos()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar!")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        tk.Button(f, text="Salvar", font=("Arial", 11, "bold"), bg="#27ae60",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=salvar).pack()
        
        e.bind('<Return>', lambda ev: salvar())
