"""
Janela de pagamento PIX com QR Code.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from PIL import Image, ImageTk

from src.services.pix_service import PixService
from src.utils.formatters import Formatters


class PixWindow:
    """Janela para pagamento PIX."""
    
    def __init__(self, parent, valor: Decimal, callback_aprovado):
        self.valor = valor
        self.callback_aprovado = callback_aprovado
        self.pix_service = PixService()
        
        # Cria janela
        self.window = tk.Toplevel(parent)
        self.window.title("Pagamento PIX")
        self.window.geometry("500x650")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.criar_widgets()
        self.gerar_qrcode()
        
        # Centraliza
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """Centraliza a janela."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_widgets(self):
        """Cria os widgets."""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="📱 Pagamento PIX",
            font=("Arial", 24, "bold"),
            fg="#16a085"
        ).pack(pady=(0, 10))
        
        # Valor
        tk.Label(
            main_frame,
            text=Formatters.formatar_moeda(self.valor),
            font=("Arial", 28, "bold"),
            fg="#16a085"
        ).pack(pady=(0, 20))
        
        # Instruções
        tk.Label(
            main_frame,
            text="Escaneie o QR Code com o aplicativo do seu banco:",
            font=("Arial", 12),
            fg="#2c3e50"
        ).pack(pady=(0, 15))
        
        # QR Code
        self.qrcode_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        self.qrcode_frame.pack(pady=(0, 20))
        
        self.label_qrcode = tk.Label(self.qrcode_frame, bg="white")
        self.label_qrcode.pack(padx=20, pady=20)
        
        # Chave PIX
        info_frame = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_frame,
            text=f"Chave PIX: {self.pix_service.CHAVE_PIX}",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(pady=10)
        
        tk.Label(
            info_frame,
            text=f"Beneficiário: {self.pix_service.NOME_BENEFICIARIO}",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(pady=(0, 10))
        
        # Status
        self.label_status = tk.Label(
            main_frame,
            text="⏳ Aguardando pagamento...",
            font=("Arial", 12),
            fg="#f39c12"
        )
        self.label_status.pack(pady=(0, 20))
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
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
            command=self.cancelar
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✓ Confirmar Pagamento",
            font=("Arial", 12, "bold"),
            bg="#16a085",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.confirmar_pagamento
        ).pack(side=tk.LEFT, padx=5)
        
        # Nota
        tk.Label(
            main_frame,
            text="* Clique em 'Confirmar Pagamento' após realizar a transferência",
            font=("Arial", 9, "italic"),
            fg="#95a5a6"
        ).pack(pady=(15, 0))
    
    def gerar_qrcode(self):
        """Gera e exibe o QR Code."""
        try:
            # Gera identificador único
            import datetime
            identificador = f"VND{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Gera QR Code
            img = self.pix_service.gerar_qrcode_pix(self.valor, identificador, tamanho=300)
            
            # Converte para PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Exibe
            self.label_qrcode.config(image=photo)
            self.label_qrcode.image = photo  # Mantém referência
            
            # Guarda dados do PIX
            self.dados_pix = self.pix_service.gerar_payload_pix(self.valor, identificador)
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar QR Code: {str(e)}")
            self.cancelar()
    
    def confirmar_pagamento(self):
        """Confirma que o pagamento foi realizado."""
        if messagebox.askyesno(
            "Confirmar Pagamento",
            "Você confirma que recebeu o pagamento via PIX?"
        ):
            self.label_status.config(text="✓ Pagamento confirmado!", fg="#27ae60")
            
            if self.callback_aprovado:
                self.callback_aprovado(self.dados_pix)
            
            self.window.destroy()
    
    def cancelar(self):
        """Cancela o pagamento PIX."""
        self.window.destroy()
