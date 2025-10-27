"""
Janela de Login do Sistema PDV.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.services.auth_service import auth_service
from src.models.usuario import Usuario


class LoginWindow:
    """Janela de login."""
    
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Sistema PDV - Login")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        
        # Centraliza a janela
        self.centralizar_janela()
        
        # Configura evento de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Criar interface
        self.criar_widgets()
        
        # Configurar navegação por teclado
        self.configurar_navegacao_teclado()
        
        # Foco inicial no campo de usuário
        self.entry_username.focus()
        
        # Bind Enter para fazer login
        self.window.bind('<Return>', lambda e: self.fazer_login())
    
    def centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_widgets(self):
        """Cria os widgets da interface."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🛒 Sistema PDV",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Ponto de Venda",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame do formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(
            form_frame,
            text="Usuário:",
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.entry_username = ttk.Entry(form_frame, font=("Arial", 11))
        self.entry_username.pack(fill=tk.X, pady=(0, 15))
        
        # Senha
        tk.Label(
            form_frame,
            text="Senha:",
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.entry_senha = ttk.Entry(form_frame, font=("Arial", 11), show="●")
        self.entry_senha.pack(fill=tk.X, pady=(0, 25))
        
        # Botão de login
        self.btn_login = tk.Button(
            form_frame,
            text="Entrar",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.fazer_login
        )
        self.btn_login.pack(fill=tk.X, pady=(0, 10))
        
        # Efeito hover no botão
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg="#229954"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg="#27ae60"))
        
        # Informações de acesso padrão
        info_frame = ttk.Frame(form_frame)
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_label = tk.Label(
            info_frame,
            text="Acesso padrão:\nAdmin: admin / admin123\nOperador: operador / operador123",
            font=("Arial", 8),
            fg="#95a5a6",
            justify=tk.LEFT
        )
        info_label.pack()
    
    def fazer_login(self):
        """Realiza o login."""
        username = self.entry_username.get().strip()
        senha = self.entry_senha.get()
        
        if not username or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        # Desabilita botão
        self.btn_login.config(state=tk.DISABLED, text="Autenticando...")
        self.window.update()
        
        # Tenta fazer login
        sucesso, mensagem, usuario = auth_service.login(username, senha)
        
        # Reabilita botão
        self.btn_login.config(state=tk.NORMAL, text="Entrar")
        
        if sucesso:
            self.window.destroy()
            self.abrir_janela_principal(usuario)
        else:
            messagebox.showerror("Erro de Login", mensagem)
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.focus()
    
    def abrir_janela_principal(self, usuario: Usuario):
        """Abre a janela principal apropriada baseada no tipo de usuário."""
        if usuario.is_admin():
            from src.ui.admin.main_admin import MainAdmin
            MainAdmin(self.master, usuario)
        else:
            from src.ui.caixa.main_caixa import MainCaixa
            MainCaixa(self.master, usuario)
    
    def configurar_navegacao_teclado(self):
        """Configura a navegação por teclado."""
        # Lista de widgets navegáveis
        self.widgets_navegaveis = []
        
        # Adicionar widgets após criação na função criar_widgets
        self.window.after(100, self._configurar_widgets_navegacao)
        
        # Binds globais
        self.window.bind('<Tab>', self._navegar_proximo)
        self.window.bind('<Shift-Tab>', self._navegar_anterior) 
        self.window.bind('<Up>', self._navegar_anterior)
        self.window.bind('<Down>', self._navegar_proximo)
        self.window.bind('<Escape>', lambda e: self.on_closing())
        
    def _configurar_widgets_navegacao(self):
        """Configura a lista de widgets navegáveis."""
        self.widgets_navegaveis = [
            self.entry_username,
            self.entry_senha,
            self.btn_login
        ]
        
        # Configura Tab stops
        for widget in self.widgets_navegaveis:
            widget.bind('<Tab>', self._navegar_proximo)
            widget.bind('<Shift-Tab>', self._navegar_anterior)
            if hasattr(widget, 'bind'):
                widget.bind('<Up>', self._navegar_anterior) 
                widget.bind('<Down>', self._navegar_proximo)
    
    def _navegar_proximo(self, event=None):
        """Navega para o próximo widget."""
        if event:
            event.widget.tk_focusNext().focus()
            return 'break'
    
    def _navegar_anterior(self, event=None):
        """Navega para o widget anterior.""" 
        if event:
            event.widget.tk_focusPrev().focus()
            return 'break'
    
    def on_closing(self):
        """Trata o fechamento da janela."""
        if messagebox.askokcancel("Sair", "Deseja sair do sistema?"):
            self.master.quit()
