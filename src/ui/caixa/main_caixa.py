"""
Janela principal do operador de caixa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from src.models.usuario import Usuario
from src.services.auth_service import auth_service
from src.dao.caixa_dao import CaixaDAO
from src.models.caixa import Caixa


class MainCaixa:
    """Interface principal do operador de caixa."""
    
    def __init__(self, master, usuario: Usuario):
        self.master = master
        self.usuario = usuario
        
        # Cria janela principal
        self.window = tk.Toplevel(master)
        self.window.title(f"Sistema PDV - Caixa - {usuario.nome_completo}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        # Configuração de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Verifica se tem caixa aberto
        self.caixa_atual = CaixaDAO.buscar_caixa_aberto(usuario.id)
        
        if self.caixa_atual:
            self.iniciar_frente_caixa()
        else:
            self.mostrar_abertura_caixa()
    
    def mostrar_abertura_caixa(self):
        """Mostra a tela de abertura de caixa."""
        # Limpa janela
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Container centralizado
        container = ttk.Frame(self.window)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        tk.Label(
            container,
            text="💵 Abertura de Caixa",
            font=("Arial", 28, "bold"),
            fg="#27ae60"
        ).pack(pady=(0, 30))
        
        # Informações
        info_frame = ttk.Frame(container)
        info_frame.pack(pady=(0, 30))
        
        tk.Label(
            info_frame,
            text=f"Operador: {self.usuario.nome_completo}",
            font=("Arial", 14)
        ).pack()
        
        # Valor de abertura
        tk.Label(
            container,
            text="Valor Inicial em Caixa:",
            font=("Arial", 12)
        ).pack(pady=(0, 10))
        
        self.entry_valor_abertura = ttk.Entry(container, font=("Arial", 16), width=20)
        self.entry_valor_abertura.pack(pady=(0, 30))
        self.entry_valor_abertura.insert(0, "0.00")
        self.entry_valor_abertura.focus()
        self.entry_valor_abertura.select_range(0, tk.END)
        
        # Botão abrir
        btn_abrir = tk.Button(
            container,
            text="Abrir Caixa",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=40,
            pady=15,
            command=self.abrir_caixa
        )
        btn_abrir.pack()
        
        # Bind Enter
        self.window.bind('<Return>', lambda e: self.abrir_caixa())
    
    def abrir_caixa(self):
        """Abre o caixa."""
        try:
            valor_str = self.entry_valor_abertura.get().replace(',', '.')
            valor_abertura = Decimal(valor_str)
            
            if valor_abertura < 0:
                messagebox.showerror("Erro", "Valor inicial não pode ser negativo!")
                return
            
            # Cria caixa
            caixa = Caixa(
                usuario_id=self.usuario.id,
                valor_abertura=valor_abertura,
                status=Caixa.STATUS_ABERTO
            )
            
            caixa_id = CaixaDAO.criar(caixa)
            
            if caixa_id:
                caixa.id = caixa_id
                self.caixa_atual = caixa
                
                messagebox.showinfo(
                    "Sucesso",
                    f"Caixa aberto com sucesso!\n\nValor inicial: R$ {float(valor_abertura):.2f}"
                )
                
                self.iniciar_frente_caixa()
            else:
                messagebox.showerror("Erro", "Erro ao abrir caixa!")
        
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
    
    def iniciar_frente_caixa(self):
        """Inicia a frente de caixa."""
        # Limpa janela
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Importa e cria a tela de venda
        from src.ui.caixa.venda_window import VendaFrame
        VendaFrame(self.window, self.usuario, self.caixa_atual, self.fechar_caixa_callback).pack(fill=tk.BOTH, expand=True)
    
    def fechar_caixa_callback(self):
        """Callback para mostrar a tela de fechamento de caixa."""
        self.mostrar_fechamento_caixa()
    
    def mostrar_fechamento_caixa(self):
        """Mostra a tela de fechamento de caixa."""
        # Limpa janela
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Container centralizado
        container = ttk.Frame(self.window)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        tk.Label(
            container,
            text="💰 Fechamento de Caixa",
            font=("Arial", 28, "bold"),
            fg="#e74c3c"
        ).pack(pady=(0, 30))
        
        # Informações do caixa
        info_frame = tk.Frame(container, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        info_frame.pack(pady=(0, 30), padx=40, fill=tk.X)
        
        tk.Label(
            info_frame,
            text=f"Valor de Abertura: R$ {float(self.caixa_atual.valor_abertura):.2f}",
            font=("Arial", 12),
            bg="#ecf0f1"
        ).pack(pady=10)
        
        # Valor de fechamento
        tk.Label(
            container,
            text="Valor Final em Caixa:",
            font=("Arial", 12)
        ).pack(pady=(0, 10))
        
        self.entry_valor_fechamento = ttk.Entry(container, font=("Arial", 16), width=20)
        self.entry_valor_fechamento.pack(pady=(0, 30))
        self.entry_valor_fechamento.focus()
        
        # Botões
        btn_frame = ttk.Frame(container)
        btn_frame.pack()
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.iniciar_frente_caixa
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Fechar Caixa",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.fechar_caixa
        ).pack(side=tk.LEFT, padx=5)
    
    def fechar_caixa(self):
        """Fecha o caixa."""
        try:
            valor_str = self.entry_valor_fechamento.get().replace(',', '.')
            valor_fechamento = Decimal(valor_str)
            
            if valor_fechamento < 0:
                messagebox.showerror("Erro", "Valor final não pode ser negativo!")
                return
            
            # Confirma fechamento
            if not messagebox.askyesno(
                "Confirmar Fechamento",
                f"Confirmar fechamento do caixa?\n\n"
                f"Valor de Abertura: R$ {float(self.caixa_atual.valor_abertura):.2f}\n"
                f"Valor de Fechamento: R$ {float(valor_fechamento):.2f}\n"
                f"Diferença: R$ {float(valor_fechamento - self.caixa_atual.valor_abertura):.2f}"
            ):
                return
            
            # Fecha caixa
            if CaixaDAO.fechar_caixa(self.caixa_atual.id, float(valor_fechamento)):
                messagebox.showinfo(
                    "Sucesso",
                    "Caixa fechado com sucesso!"
                )
                
                self.sair()
            else:
                messagebox.showerror("Erro", "Erro ao fechar caixa!")
        
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
    
    def sair(self):
        """Sai do sistema."""
        auth_service.logout()
        self.window.destroy()
        from src.ui.login_window import LoginWindow
        LoginWindow(self.master)
    
    def on_closing(self):
        """Trata o fechamento da janela."""
        if messagebox.askokcancel("Sair", "Deseja sair? O caixa permanecerá aberto."):
            self.sair()
