"""
Serviço para autenticação de administrador para operações especiais.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable

from src.dao.usuario_dao import UsuarioDAO
from src.models.usuario import Usuario


class AdminAuthService:
    """Serviço para autenticação de administrador."""
    
    @staticmethod
    def solicitar_autenticacao_admin(parent, callback_sucesso: Callable, callback_cancelado: Callable = None):
        """
        Solicita autenticação de administrador.
        
        Args:
            parent: Widget pai
            callback_sucesso: Função chamada quando autenticado com sucesso (recebe o usuario admin)
            callback_cancelado: Função chamada quando cancelado
        """
        AdminAuthDialog(parent, callback_sucesso, callback_cancelado)


class AdminAuthDialog:
    """Dialog para autenticação de administrador."""
    
    def __init__(self, parent, callback_sucesso: Callable, callback_cancelado: Callable = None):
        self.callback_sucesso = callback_sucesso
        self.callback_cancelado = callback_cancelado
        
        # Cria overlay modal
        self.overlay = tk.Frame(parent, bg="black")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.configure(bg="black")  # Semi-transparente seria ideal
        self.overlay.lift()
        
        # Dialog centralizado
        self.dialog = tk.Frame(self.overlay, bg="#ffffff", relief=tk.RAISED, bd=3)
        self.dialog.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=250)
        
        self.criar_widgets()
        
        # Foco no campo
        self.entry_username.focus()
        
        # Binds
        self.dialog.bind_all('<Return>', lambda e: self.autenticar())
        self.dialog.bind_all('<Escape>', lambda e: self.cancelar())
    
    def criar_widgets(self):
        """Cria os widgets do dialog."""
        # Título
        titulo_frame = tk.Frame(self.dialog, bg="#e74c3c", height=50)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="🔐 AUTENTICAÇÃO ADMINISTRADOR",
                 font=("Arial", 14, "bold"), bg="#e74c3c", fg="white").pack(expand=True)
        
        # Conteúdo
        content_frame = tk.Frame(self.dialog, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text="Esta operação requer autenticação de administrador:",
                 font=("Arial", 10), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 15))
        
        # Username
        tk.Label(content_frame, text="Usuário Administrador:",
                 font=("Arial", 10, "bold"), bg="#ffffff", fg="#2c3e50").pack(anchor=tk.W)
        
        self.entry_username = ttk.Entry(content_frame, font=("Arial", 12))
        self.entry_username.pack(fill=tk.X, pady=(5, 10))
        
        # Senha
        tk.Label(content_frame, text="Senha:",
                 font=("Arial", 10, "bold"), bg="#ffffff", fg="#2c3e50").pack(anchor=tk.W)
        
        self.entry_senha = ttk.Entry(content_frame, font=("Arial", 12), show="●")
        self.entry_senha.pack(fill=tk.X, pady=(5, 15))
        
        # Status
        self.label_status = tk.Label(content_frame, text="",
                                     font=("Arial", 9), bg="#ffffff", fg="#e74c3c")
        self.label_status.pack(pady=(0, 10))
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg="#ffffff")
        botoes_frame.pack(fill=tk.X)
        
        tk.Button(botoes_frame, text="CANCELAR", font=("Arial", 10, "bold"),
                  bg="#95a5a6", fg="white", relief=tk.FLAT, padx=20, pady=8,
                  command=self.cancelar).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(botoes_frame, text="AUTENTICAR", font=("Arial", 10, "bold"),
                  bg="#27ae60", fg="white", relief=tk.FLAT, padx=20, pady=8,
                  command=self.autenticar).pack(side=tk.RIGHT)
    
    def autenticar(self):
        """Tenta autenticar o administrador."""
        username = self.entry_username.get().strip()
        senha = self.entry_senha.get()
        
        if not username or not senha:
            self.label_status.config(text="⚠️ Preencha todos os campos")
            return
        
        # Tenta autenticar
        usuario = UsuarioDAO.autenticar(username, senha)
        
        if usuario and usuario.is_admin():
            # Sucesso - é admin
            self.destruir()
            if self.callback_sucesso:
                self.callback_sucesso(usuario)
        elif usuario and not usuario.is_admin():
            # Usuário válido mas não é admin
            self.label_status.config(text="❌ Usuário não é administrador")
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.focus()
        else:
            # Credenciais inválidas
            self.label_status.config(text="❌ Credenciais inválidas")
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.focus()
    
    def cancelar(self):
        """Cancela a autenticação."""
        self.destruir()
        if self.callback_cancelado:
            self.callback_cancelado()
    
    def destruir(self):
        """Destrói o dialog."""
        self.dialog.unbind_all('<Return>')
        self.dialog.unbind_all('<Escape>')
        self.overlay.destroy()


class ItemActionDialog:
    """Dialog para ações em itens (cancelar/editar quantidade)."""
    
    def __init__(self, parent, item_data, acao="cancelar"):
        self.item_data = item_data
        self.acao = acao
        self.resultado = None
        
        # Cria overlay modal
        self.overlay = tk.Frame(parent, bg="black")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()
        
        # Dialog centralizado
        altura = 300 if acao == "editar_quantidade" else 250
        self.dialog = tk.Frame(self.overlay, bg="#ffffff", relief=tk.RAISED, bd=3)
        self.dialog.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=altura)
        
        self.criar_widgets()
        
        # Foco apropriado
        if acao == "editar_quantidade":
            self.entry_quantidade.focus()
            self.entry_quantidade.select_range(0, tk.END)
        
        # Binds
        self.dialog.bind_all('<Return>', lambda e: self.confirmar())
        self.dialog.bind_all('<Escape>', lambda e: self.cancelar())
    
    def criar_widgets(self):
        """Cria os widgets do dialog."""
        # Cor do título baseada na ação
        cor_titulo = "#f39c12" if self.acao == "editar_quantidade" else "#e74c3c"
        texto_titulo = "📝 EDITAR QUANTIDADE" if self.acao == "editar_quantidade" else "🗑️ CANCELAR ITEM"
        
        # Título
        titulo_frame = tk.Frame(self.dialog, bg=cor_titulo, height=50)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text=texto_titulo,
                 font=("Arial", 14, "bold"), bg=cor_titulo, fg="white").pack(expand=True)
        
        # Conteúdo
        content_frame = tk.Frame(self.dialog, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Informações do item
        item_frame = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        item_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(item_frame, text="ITEM SELECIONADO:",
                 font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#7f8c8d").pack(pady=(10, 5))
        
        # Exibe dados do item
        tk.Label(item_frame, text=f"Código: {self.item_data.get('codigo', 'N/A')}",
                 font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50").pack()
        
        tk.Label(item_frame, text=f"Produto: {self.item_data.get('nome', 'N/A')}",
                 font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#2c3e50").pack()
        
        tk.Label(item_frame, text=f"Quantidade Atual: {self.item_data.get('qtd', 'N/A')}",
                 font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50").pack()
        
        tk.Label(item_frame, text=f"Preço Unit.: {self.item_data.get('preco', 'N/A')}",
                 font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50").pack(pady=(0, 10))
        
        if self.acao == "editar_quantidade":
            # Campo para nova quantidade
            tk.Label(content_frame, text="Nova Quantidade:",
                     font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(anchor=tk.W)
            
            self.entry_quantidade = ttk.Entry(content_frame, font=("Arial", 14))
            self.entry_quantidade.pack(fill=tk.X, pady=(5, 15))
            self.entry_quantidade.insert(0, str(self.item_data.get('qtd', '1')))
            
            tk.Label(content_frame, text="💡 Use vírgula para decimais (ex: 1,5)",
                     font=("Arial", 9, "italic"), bg="#ffffff", fg="#7f8c8d").pack(anchor=tk.W)
        else:
            # Confirmação de cancelamento
            tk.Label(content_frame, text="⚠️ Confirma o cancelamento deste item?",
                     font=("Arial", 12, "bold"), bg="#ffffff", fg="#e74c3c").pack(pady=15)
        
        # Status
        self.label_status = tk.Label(content_frame, text="",
                                     font=("Arial", 9), bg="#ffffff", fg="#e74c3c")
        self.label_status.pack(pady=(10, 0))
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg="#ffffff")
        botoes_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Button(botoes_frame, text="CANCELAR", font=("Arial", 11, "bold"),
                  bg="#95a5a6", fg="white", relief=tk.FLAT, padx=20, pady=10,
                  command=self.cancelar).pack(side=tk.LEFT, padx=(0, 10))
        
        texto_confirmar = "ALTERAR" if self.acao == "editar_quantidade" else "CANCELAR ITEM"
        cor_confirmar = "#f39c12" if self.acao == "editar_quantidade" else "#e74c3c"
        
        tk.Button(botoes_frame, text=texto_confirmar, font=("Arial", 11, "bold"),
                  bg=cor_confirmar, fg="white", relief=tk.FLAT, padx=20, pady=10,
                  command=self.confirmar).pack(side=tk.RIGHT)
    
    def confirmar(self):
        """Confirma a ação."""
        if self.acao == "editar_quantidade":
            try:
                nova_qtd_str = self.entry_quantidade.get().replace(',', '.')
                nova_qtd = float(nova_qtd_str)
                
                if nova_qtd <= 0:
                    self.label_status.config(text="⚠️ Quantidade deve ser maior que zero")
                    return
                
                self.resultado = {"acao": "editar_quantidade", "nova_quantidade": nova_qtd}
                
            except ValueError:
                self.label_status.config(text="⚠️ Quantidade inválida")
                return
        else:
            self.resultado = {"acao": "cancelar_item"}
        
        self.destruir()
    
    def cancelar(self):
        """Cancela a ação."""
        self.resultado = None
        self.destruir()
    
    def destruir(self):
        """Destrói o dialog."""
        self.dialog.unbind_all('<Return>')
        self.dialog.unbind_all('<Escape>')
        self.overlay.destroy()