"""
Tela de gestão de categorias.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.dao.categoria_dao import CategoriaDAO
from src.models.categoria import Categoria


class CategoriasFrame(ttk.Frame):
    """Frame para gestão de categorias."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.criar_widgets()
        self.carregar_categorias()
    
    def criar_widgets(self):
        """Cria os widgets."""
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="🏷️ Gestão de Categorias", font=("Arial", 20, "bold"),
                 fg="#2c3e50").pack(side=tk.LEFT)
        
        tk.Button(header, text="+ Nova Categoria", font=("Arial", 11, "bold"),
                  bg="#27ae60", fg="white", cursor="hand2", relief=tk.FLAT,
                  padx=20, pady=8, command=self.nova_categoria).pack(side=tk.RIGHT)
        
        # Tabela
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
            columns=("nome", "descricao", "status"), show="headings")
        
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("status", text="Status")
        
        self.tree.column("nome", width=200)
        self.tree.column("descricao", width=400)
        self.tree.column("status", width=100)
        
        scroll.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<Double-1>', lambda e: self.editar_categoria())
        
        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(btn_frame, text="✏️ Editar", font=("Arial", 10), bg="#3498db",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=20, pady=8,
                  command=self.editar_categoria).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="🗑️ Excluir", font=("Arial", 10), bg="#e74c3c",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=20, pady=8,
                  command=self.excluir_categoria).pack(side=tk.LEFT)
    
    def carregar_categorias(self):
        """Carrega categorias."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        categorias = CategoriaDAO.buscar_todas(apenas_ativas=False)
        for cat in categorias:
            self.tree.insert("", tk.END, values=(
                cat.nome, cat.descricao or "", "Ativa" if cat.ativo else "Inativa"
            ), tags=(cat.id,))
    
    def nova_categoria(self):
        """Nova categoria."""
        CategoriaDialog(self, None, self.carregar_categorias)
    
    def editar_categoria(self):
        """Edita categoria."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        
        cat_id = int(self.tree.item(sel[0])['tags'][0])
        cat = CategoriaDAO.buscar_por_id(cat_id)
        if cat:
            CategoriaDialog(self, cat, self.carregar_categorias)
    
    def excluir_categoria(self):
        """Exclui categoria."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        
        cat_id = int(self.tree.item(sel[0])['tags'][0])
        cat = CategoriaDAO.buscar_por_id(cat_id)
        
        if cat:
            if messagebox.askyesno("Confirmar", f"Deseja excluir '{cat.nome}'?"):
                if CategoriaDAO.excluir(cat_id):
                    messagebox.showinfo("Sucesso", "Categoria excluída!")
                    self.carregar_categorias()


class CategoriaDialog:
    """Dialog para categoria."""
    
    def __init__(self, parent, categoria=None, callback=None):
        self.categoria = categoria
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nova Categoria" if not categoria else "Editar Categoria")
        self.window.geometry("450x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.criar_widgets()
        if categoria:
            self.preencher_dados()
    
    def criar_widgets(self):
        """Cria widgets."""
        main = ttk.Frame(self.window, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="Nova Categoria" if not self.categoria else "Editar Categoria",
                 font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=(0, 20))
        
        form = ttk.Frame(main)
        form.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form, text="Nome:*", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = ttk.Entry(form, font=("Arial", 11))
        self.entry_nome.grid(row=0, column=1, sticky="ew", pady=5)
        
        tk.Label(form, text="Descrição:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_desc = tk.Text(form, font=("Arial", 11), height=5)
        self.entry_desc.grid(row=1, column=1, sticky="ew", pady=5)
        
        self.var_ativo = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Ativa", variable=self.var_ativo).grid(row=2, column=1, sticky="w", pady=10)
        
        form.columnconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(btn_frame, text="Cancelar", font=("Arial", 11), bg="#95a5a6",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(btn_frame, text="Salvar", font=("Arial", 11, "bold"), bg="#27ae60",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=self.salvar).pack(side=tk.RIGHT)
    
    def preencher_dados(self):
        """Preenche dados."""
        if self.categoria:
            self.entry_nome.insert(0, self.categoria.nome)
            self.entry_desc.insert("1.0", self.categoria.descricao or "")
            self.var_ativo.set(self.categoria.ativo)
    
    def salvar(self):
        """Salva categoria."""
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return
        
        if self.categoria:
            cat = self.categoria
        else:
            cat = Categoria()
        
        cat.nome = nome
        cat.descricao = self.entry_desc.get("1.0", tk.END).strip()
        cat.ativo = self.var_ativo.get()
        
        if self.categoria:
            sucesso = CategoriaDAO.atualizar(cat)
            msg = "Categoria atualizada!"
        else:
            cat_id = CategoriaDAO.criar(cat)
            sucesso = cat_id is not None
            msg = "Categoria cadastrada!"
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            if self.callback:
                self.callback()
            self.window.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao salvar!")
