"""
Tela de gestão de produtos.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.dao.produto_dao import ProdutoDAO
from src.dao.categoria_dao import CategoriaDAO
from src.models.produto import Produto
from src.utils.formatters import Formatters
from src.utils.validators import Validators
from decimal import Decimal


class ProdutosFrame(ttk.Frame):
    """Frame para gestão de produtos."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.criar_widgets()
        self.carregar_produtos()
    
    def criar_widgets(self):
        """Cria os widgets."""
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header,
            text="📦 Gestão de Produtos",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header,
            text="+ Novo Produto",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.novo_produto
        ).pack(side=tk.RIGHT)
        
        # Busca
        busca_frame = ttk.Frame(self)
        busca_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(busca_frame, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_busca = ttk.Entry(busca_frame, font=("Arial", 11), width=40)
        self.entry_busca.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_busca.bind('<KeyRelease>', lambda e: self.buscar())
        
        tk.Button(
            busca_frame,
            text="Atualizar",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            command=self.carregar_produtos
        ).pack(side=tk.LEFT)
        
        # Tabela
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("codigo", "nome", "categoria", "preco_custo", "preco_venda", "estoque", "status"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("preco_custo", text="Preço Custo")
        self.tree.heading("preco_venda", text="Preço Venda")
        self.tree.heading("estoque", text="Estoque")
        self.tree.heading("status", text="Status")
        
        self.tree.column("codigo", width=120)
        self.tree.column("nome", width=300)
        self.tree.column("categoria", width=150)
        self.tree.column("preco_custo", width=100)
        self.tree.column("preco_venda", width=100)
        self.tree.column("estoque", width=80)
        self.tree.column("status", width=80)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Double click para editar
        self.tree.bind('<Double-1>', lambda e: self.editar_produto())
        
        # Botões de ação
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            btn_frame,
            text="✏️ Editar",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.editar_produto
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="🗑️ Excluir",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.excluir_produto
        ).pack(side=tk.LEFT)
    
    def carregar_produtos(self):
        """Carrega os produtos na tabela."""
        # Limpa árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca produtos
        produtos = ProdutoDAO.buscar_todos(apenas_ativos=False)
        
        for produto in produtos:
            self.tree.insert("", tk.END, values=(
                produto.codigo_barras or "",
                produto.nome,
                produto.categoria_nome or "Sem Categoria",
                Formatters.formatar_moeda(produto.preco_custo),
                Formatters.formatar_moeda(produto.preco_venda),
                produto.estoque_atual,
                "Ativo" if produto.ativo else "Inativo"
            ), tags=(produto.id,))
    
    def buscar(self):
        """Busca produtos."""
        termo = self.entry_busca.get().strip()
        
        # Limpa árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not termo:
            self.carregar_produtos()
            return
        
        # Busca
        produtos = ProdutoDAO.buscar_por_nome(termo)
        
        for produto in produtos:
            self.tree.insert("", tk.END, values=(
                produto.codigo_barras or "",
                produto.nome,
                produto.categoria_nome or "Sem Categoria",
                Formatters.formatar_moeda(produto.preco_custo),
                Formatters.formatar_moeda(produto.preco_venda),
                produto.estoque_atual,
                "Ativo" if produto.ativo else "Inativo"
            ), tags=(produto.id,))
    
    def novo_produto(self):
        """Abre janela para novo produto."""
        ProdutoDialog(self, None, self.carregar_produtos)
    
    def editar_produto(self):
        """Edita o produto selecionado."""
        selecionado = self.tree.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        produto_id = int(self.tree.item(selecionado[0])['tags'][0])
        produto = ProdutoDAO.buscar_por_id(produto_id)
        
        if produto:
            ProdutoDialog(self, produto, self.carregar_produtos)
    
    def excluir_produto(self):
        """Exclui o produto selecionado."""
        selecionado = self.tree.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        produto_id = int(self.tree.item(selecionado[0])['tags'][0])
        produto = ProdutoDAO.buscar_por_id(produto_id)
        
        if produto:
            if messagebox.askyesno("Confirmar", f"Deseja excluir o produto '{produto.nome}'?"):
                if ProdutoDAO.excluir(produto_id):
                    messagebox.showinfo("Sucesso", "Produto excluído!")
                    self.carregar_produtos()
                else:
                    messagebox.showerror("Erro", "Erro ao excluir produto!")


class ProdutoDialog:
    """Dialog para cadastro/edição de produtos."""
    
    def __init__(self, parent, produto=None, callback=None):
        self.produto = produto
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Novo Produto" if not produto else "Editar Produto")
        self.window.geometry("500x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.criar_widgets()
        
        if produto:
            self.preencher_dados()
    
    def criar_widgets(self):
        """Cria os widgets."""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="Novo Produto" if not self.produto else "Editar Produto",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        ).pack(pady=(0, 20))
        
        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Código de barras
        self.criar_campo(form_frame, "Código de Barras:", 0)
        self.entry_codigo = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_codigo.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Nome
        self.criar_campo(form_frame, "Nome:*", 1)
        self.entry_nome = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_nome.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Descrição
        self.criar_campo(form_frame, "Descrição:", 2)
        self.entry_descricao = tk.Text(form_frame, font=("Arial", 11), height=3)
        self.entry_descricao.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Categoria
        self.criar_campo(form_frame, "Categoria:", 3)
        self.combo_categoria = ttk.Combobox(form_frame, font=("Arial", 11), state="readonly")
        self.combo_categoria.grid(row=3, column=1, sticky="ew", pady=5)
        self.carregar_categorias()
        
        # Preço custo
        self.criar_campo(form_frame, "Preço Custo:", 4)
        self.entry_preco_custo = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_preco_custo.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Preço venda
        self.criar_campo(form_frame, "Preço Venda:*", 5)
        self.entry_preco_venda = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_preco_venda.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Estoque
        self.criar_campo(form_frame, "Estoque Atual:", 6)
        self.entry_estoque = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_estoque.grid(row=6, column=1, sticky="ew", pady=5)
        
        # Estoque mínimo
        self.criar_campo(form_frame, "Estoque Mínimo:", 7)
        self.entry_estoque_min = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_estoque_min.grid(row=7, column=1, sticky="ew", pady=5)
        
        # Unidade de medida
        self.criar_campo(form_frame, "Unidade:", 8)
        self.combo_unidade = ttk.Combobox(
            form_frame,
            font=("Arial", 11),
            values=["UN", "KG", "LT", "MT", "CX", "PC"],
            state="readonly"
        )
        self.combo_unidade.grid(row=8, column=1, sticky="ew", pady=5)
        self.combo_unidade.set("UN")
        
        # Ativo
        self.var_ativo = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            form_frame,
            text="Produto Ativo",
            variable=self.var_ativo
        ).grid(row=9, column=1, sticky="w", pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Salvar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.salvar
        ).pack(side=tk.RIGHT)
    
    def criar_campo(self, parent, texto, row):
        """Cria um label de campo."""
        tk.Label(
            parent,
            text=texto,
            font=("Arial", 10)
        ).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 10))
    
    def carregar_categorias(self):
        """Carrega as categorias."""
        categorias = CategoriaDAO.buscar_todas()
        valores = ["Sem Categoria"] + [cat.nome for cat in categorias]
        self.combo_categoria['values'] = valores
        self.combo_categoria.set("Sem Categoria")
        self.categorias = {cat.nome: cat.id for cat in categorias}
    
    def preencher_dados(self):
        """Preenche os dados do produto."""
        if not self.produto:
            return
        
        self.entry_codigo.insert(0, self.produto.codigo_barras or "")
        self.entry_nome.insert(0, self.produto.nome)
        self.entry_descricao.insert("1.0", self.produto.descricao or "")
        
        if self.produto.categoria_nome:
            self.combo_categoria.set(self.produto.categoria_nome)
        
        self.entry_preco_custo.insert(0, f"{float(self.produto.preco_custo):.2f}")
        self.entry_preco_venda.insert(0, f"{float(self.produto.preco_venda):.2f}")
        self.entry_estoque.insert(0, str(self.produto.estoque_atual))
        self.entry_estoque_min.insert(0, str(self.produto.estoque_minimo))
        self.combo_unidade.set(self.produto.unidade_medida)
        self.var_ativo.set(self.produto.ativo)
    
    def salvar(self):
        """Salva o produto."""
        # Valida campos
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return
        
        valido, preco_venda = Validators.validar_preco(self.entry_preco_venda.get())
        if not valido:
            messagebox.showerror("Erro", "Preço de venda inválido!")
            return
        
        # Cria/atualiza produto
        if self.produto:
            produto = self.produto
        else:
            produto = Produto()
        
        produto.codigo_barras = self.entry_codigo.get().strip() or None
        produto.nome = nome
        produto.descricao = self.entry_descricao.get("1.0", tk.END).strip()
        
        categoria_nome = self.combo_categoria.get()
        produto.categoria_id = self.categorias.get(categoria_nome)
        
        _, preco_custo = Validators.validar_preco(self.entry_preco_custo.get())
        produto.preco_custo = preco_custo
        produto.preco_venda = preco_venda
        
        try:
            produto.estoque_atual = int(self.entry_estoque.get() or 0)
            produto.estoque_minimo = int(self.entry_estoque_min.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Estoque inválido!")
            return
        
        produto.unidade_medida = self.combo_unidade.get()
        produto.ativo = self.var_ativo.get()
        
        # Salva
        if self.produto:
            sucesso = ProdutoDAO.atualizar(produto)
            mensagem = "Produto atualizado!"
        else:
            produto_id = ProdutoDAO.criar(produto)
            sucesso = produto_id is not None
            mensagem = "Produto cadastrado!"
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            if self.callback:
                self.callback()
            self.window.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao salvar produto!")
