"""
Tela de gestão de usuários.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.dao.usuario_dao import UsuarioDAO
from src.models.usuario import Usuario
from src.utils.validators import Validators


class UsuariosFrame(ttk.Frame):
    """Frame para gestão de usuários."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.criar_widgets()
        self.carregar_usuarios()
    
    def criar_widgets(self):
        """Cria widgets."""
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="👥 Gestão de Usuários", font=("Arial", 20, "bold"),
                 fg="#2c3e50").pack(side=tk.LEFT)
        
        tk.Button(header, text="+ Novo Usuário", font=("Arial", 11, "bold"),
                  bg="#27ae60", fg="white", cursor="hand2", relief=tk.FLAT,
                  padx=20, pady=8, command=self.novo_usuario).pack(side=tk.RIGHT)
        
        # Tabela
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
            columns=("username", "nome", "tipo", "status"), show="headings")
        
        self.tree.heading("username", text="Usuário")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("status", text="Status")
        
        self.tree.column("username", width=150)
        self.tree.column("nome", width=300)
        self.tree.column("tipo", width=120)
        self.tree.column("status", width=100)
        
        scroll.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<Double-1>', lambda e: self.editar_usuario())
        
        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(btn_frame, text="✏️ Editar", font=("Arial", 10), bg="#3498db",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=20, pady=8,
                  command=self.editar_usuario).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="🔑 Alterar Senha", font=("Arial", 10), bg="#f39c12",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=20, pady=8,
                  command=self.alterar_senha).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="🗑️ Excluir", font=("Arial", 10), bg="#e74c3c",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=20, pady=8,
                  command=self.excluir_usuario).pack(side=tk.LEFT)
    
    def carregar_usuarios(self):
        """Carrega usuários."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = UsuarioDAO.buscar_todos(apenas_ativos=False)
        for u in usuarios:
            tipo = "Administrador" if u.tipo == Usuario.TIPO_ADMIN else "Operador"
            self.tree.insert("", tk.END, values=(
                u.username, u.nome_completo, tipo, "Ativo" if u.ativo else "Inativo"
            ), tags=(u.id,))
    
    def novo_usuario(self):
        """Novo usuário."""
        UsuarioDialog(self, None, self.carregar_usuarios)
    
    def editar_usuario(self):
        """Edita usuário."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        
        user_id = int(self.tree.item(sel[0])['tags'][0])
        user = UsuarioDAO.buscar_por_id(user_id)
        if user:
            UsuarioDialog(self, user, self.carregar_usuarios)
    
    def alterar_senha(self):
        """Altera senha do usuário."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        
        user_id = int(self.tree.item(sel[0])['tags'][0])
        user = UsuarioDAO.buscar_por_id(user_id)
        
        if not user:
            return
        
        d = tk.Toplevel(self)
        d.title("Alterar Senha")
        d.geometry("350x200")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text=f"Alterar senha de: {user.username}",
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        tk.Label(f, text="Nova Senha:", font=("Arial", 10)).pack(pady=(0, 5))
        e_senha = ttk.Entry(f, font=("Arial", 12), show="●")
        e_senha.pack(pady=(0, 15))
        e_senha.focus()
        
        def salvar():
            senha = e_senha.get()
            valido, msg = Validators.validar_senha(senha)
            if not valido:
                messagebox.showerror("Erro", msg)
                return
            
            user.set_senha(senha)
            if UsuarioDAO.atualizar(user):
                messagebox.showinfo("Sucesso", "Senha alterada!")
                d.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao alterar senha!")
        
        tk.Button(f, text="Salvar", font=("Arial", 11, "bold"), bg="#27ae60",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=salvar).pack()
        
        e_senha.bind('<Return>', lambda ev: salvar())
    
    def excluir_usuario(self):
        """Exclui usuário."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        
        user_id = int(self.tree.item(sel[0])['tags'][0])
        user = UsuarioDAO.buscar_por_id(user_id)
        
        if user:
            if messagebox.askyesno("Confirmar", f"Deseja excluir '{user.username}'?"):
                if UsuarioDAO.excluir(user_id):
                    messagebox.showinfo("Sucesso", "Usuário excluído!")
                    self.carregar_usuarios()


class UsuarioDialog:
    """Dialog para usuário."""
    
    def __init__(self, parent, usuario=None, callback=None):
        self.usuario = usuario
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Novo Usuário" if not usuario else "Editar Usuário")
        self.window.geometry("450x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.criar_widgets()
        if usuario:
            self.preencher_dados()
    
    def criar_widgets(self):
        """Cria widgets."""
        main = ttk.Frame(self.window, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="Novo Usuário" if not self.usuario else "Editar Usuário",
                 font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=(0, 20))
        
        form = ttk.Frame(main)
        form.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form, text="Username:*", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_username = ttk.Entry(form, font=("Arial", 11))
        self.entry_username.grid(row=0, column=1, sticky="ew", pady=5)
        
        tk.Label(form, text="Nome Completo:*", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = ttk.Entry(form, font=("Arial", 11))
        self.entry_nome.grid(row=1, column=1, sticky="ew", pady=5)
        
        if not self.usuario:
            tk.Label(form, text="Senha:*", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
            self.entry_senha = ttk.Entry(form, font=("Arial", 11), show="●")
            self.entry_senha.grid(row=2, column=1, sticky="ew", pady=5)
        
        tk.Label(form, text="Tipo:*", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(form, font=("Arial", 11),
                                        values=["Administrador", "Operador"],
                                        state="readonly")
        self.combo_tipo.grid(row=3, column=1, sticky="ew", pady=5)
        self.combo_tipo.set("Operador")
        
        self.var_ativo = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Ativo", variable=self.var_ativo).grid(row=4, column=1, sticky="w", pady=10)
        
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
        if self.usuario:
            self.entry_username.insert(0, self.usuario.username)
            self.entry_nome.insert(0, self.usuario.nome_completo)
            self.combo_tipo.set("Administrador" if self.usuario.tipo == Usuario.TIPO_ADMIN else "Operador")
            self.var_ativo.set(self.usuario.ativo)
    
    def salvar(self):
        """Salva usuário."""
        username = self.entry_username.get().strip()
        nome = self.entry_nome.get().strip()
        
        valido, msg = Validators.validar_username(username)
        if not valido:
            messagebox.showerror("Erro", msg)
            return
        
        if not nome:
            messagebox.showerror("Erro", "Nome completo é obrigatório!")
            return
        
        if not self.usuario:
            senha = self.entry_senha.get()
            valido, msg = Validators.validar_senha(senha)
            if not valido:
                messagebox.showerror("Erro", msg)
                return
        
        if self.usuario:
            user = self.usuario
        else:
            user = Usuario()
        
        user.username = username
        user.nome_completo = nome
        user.tipo = Usuario.TIPO_ADMIN if self.combo_tipo.get() == "Administrador" else Usuario.TIPO_OPERADOR
        user.ativo = self.var_ativo.get()
        
        if not self.usuario:
            user.set_senha(self.entry_senha.get())
        
        if self.usuario:
            sucesso = UsuarioDAO.atualizar(user)
            msg = "Usuário atualizado!"
        else:
            user_id = UsuarioDAO.criar(user)
            sucesso = user_id is not None
            msg = "Usuário cadastrado!"
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            if self.callback:
                self.callback()
            self.window.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao salvar!")
