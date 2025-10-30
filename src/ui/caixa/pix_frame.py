"""
Janela integrada para pagamento PIX com Mercado Pago.
"""

import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import io
import base64
from decimal import Decimal

from src.services.mercado_pago_service import mercado_pago_service, pix_monitor
from src.utils.formatters import Formatters


class PIXFrame(tk.Frame):
    """Frame integrado para pagamento PIX."""
    
    def __init__(self, parent, payment_data, callback_aprovado, callback_cancelado):
        super().__init__(parent, bg="#ffffff")
        
        self.payment_data = payment_data
        self.valor = Decimal(str(payment_data.get('transaction_amount', 0)))
        self.callback_aprovado = callback_aprovado
        self.callback_cancelado = callback_cancelado
        
        self.payment_id = None
        self.qr_code_data = None
        self.timer_ativo = True
        
        self.criar_widgets()
        self.processar_payment_data()
    
    def criar_widgets(self):
        """Cria os widgets da interface PIX."""
        # Container principal
        main_container = tk.Frame(self, bg="#ffffff", relief=tk.RAISED, bd=3)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Frame(main_container, bg="#f39c12", height=50)
        titulo.pack(fill=tk.X)
        titulo.pack_propagate(False)
        
        tk.Label(titulo, text="📱 PAGAMENTO PIX", font=("Arial", 16, "bold"),
                 bg="#f39c12", fg="white").pack(expand=True)
        
        # Valor
        valor_frame = tk.Frame(main_container, bg="#27ae60", relief=tk.RAISED, bd=2)
        valor_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(valor_frame, text="VALOR A PAGAR", font=("Arial", 12, "bold"),
                 bg="#27ae60", fg="white").pack(pady=(10, 5))
        
        tk.Label(valor_frame, text=Formatters.formatar_moeda(float(self.valor)),
                 font=("Arial", 24, "bold"), bg="#27ae60", fg="white").pack(pady=(0, 10))
        
        # Container do conteúdo principal
        content_frame = tk.Frame(main_container, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status
        self.status_frame = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.label_status = tk.Label(self.status_frame, text="🔄 Gerando PIX...",
                                     font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#f39c12")
        self.label_status.pack(pady=10)
        
        # Container para QR Code e Copia e Cola
        self.qr_container = tk.Frame(content_frame, bg="#ffffff")
        self.qr_container.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        acoes_frame = tk.Frame(main_container, bg="#ffffff")
        acoes_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(acoes_frame, text="ESC - CANCELAR PIX", font=("Arial", 12, "bold"),
                  bg="#e74c3c", fg="white", relief=tk.FLAT, pady=10,
                  command=self.cancelar_pix).pack(fill=tk.X)
        
        # Bind do Escape
        self.bind_all('<Escape>', lambda e: self.cancelar_pix())
    
    def processar_payment_data(self):
        """Processa os dados do pagamento já criado."""
        if self.payment_data:
            self.payment_id = str(self.payment_data.get("id", ""))
            
            # Obter QR Code do payment_data
            point_of_interaction = self.payment_data.get("point_of_interaction", {})
            transaction_data = point_of_interaction.get("transaction_data", {})
            
            # Estrutura dos dados do QR Code
            self.qr_code_data = {
                "qr_code": transaction_data.get("qr_code", ""),
                "qr_code_base64": transaction_data.get("qr_code_base64", "")
            }
            
            if self.qr_code_data.get("qr_code"):
                self.mostrar_qr_code()
                self.iniciar_monitoramento()
            else:
                self.mostrar_erro("Erro ao obter dados do QR Code PIX")
        else:
            self.mostrar_erro("Erro ao processar pagamento PIX")
    
    def mostrar_qr_code(self):
        """Mostra o QR Code e código Copia e Cola."""
        # Atualiza status
        self.label_status.config(text="📱 PIX Gerado - Aguardando Pagamento", fg="#3498db")
        
        # Limpa container
        for widget in self.qr_container.winfo_children():
            widget.destroy()
        
        # Divide em duas colunas
        left_frame = tk.Frame(self.qr_container, bg="#ffffff")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(self.qr_container, bg="#ffffff")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # QR Code (lado esquerdo)
        tk.Label(left_frame, text="🎯 ESCANEIE O QR CODE", font=("Arial", 14, "bold"),
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 10))
        
        # Gera QR Code
        if self.qr_code_data and self.qr_code_data["qr_code"]:
            qr_img = self.gerar_qr_code_image(self.qr_code_data["qr_code"])
            if qr_img:
                qr_label = tk.Label(left_frame, image=qr_img, bg="#ffffff")
                qr_label.image = qr_img  # Mantém referência
                qr_label.pack(pady=10)
        
        # Código Copia e Cola (lado direito)
        tk.Label(right_frame, text="📋 COPIA E COLA", font=("Arial", 12, "bold"),
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 10))
        
        # Campo de texto com o código
        codigo_frame = tk.Frame(right_frame, bg="#f8f9fa", relief=tk.SUNKEN, bd=2)
        codigo_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        texto_codigo = tk.Text(codigo_frame, height=8, width=40, font=("Courier", 9),
                               bg="#f8f9fa", fg="#2c3e50", wrap=tk.WORD,
                               relief=tk.FLAT, state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(codigo_frame, orient=tk.VERTICAL, command=texto_codigo.yview)
        texto_codigo.configure(yscrollcommand=scrollbar.set)
        
        # Insere o código
        texto_codigo.config(state=tk.NORMAL)
        if self.qr_code_data and self.qr_code_data["qr_code"]:
            texto_codigo.insert(tk.END, self.qr_code_data["qr_code"])
        texto_codigo.config(state=tk.DISABLED)
        
        texto_codigo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão copiar
        tk.Button(right_frame, text="📋 COPIAR CÓDIGO", font=("Arial", 10, "bold"),
                  bg="#3498db", fg="white", relief=tk.FLAT, pady=8,
                  command=self.copiar_codigo).pack(fill=tk.X, pady=(10, 0))
        
        # Timer visual
        self.timer_frame = tk.Frame(self.qr_container, bg="#ffffff")
        self.timer_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.label_timer = tk.Label(self.timer_frame, text="⏱️ PIX expira em 15:00 minutos",
                                    font=("Arial", 10), bg="#ffffff", fg="#7f8c8d")
        self.label_timer.pack()
        
        # Inicia countdown
        self.iniciar_countdown(15 * 60)  # 15 minutos
    
    def gerar_qr_code_image(self, codigo: str) -> ImageTk.PhotoImage:
        """Gera imagem do QR Code."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=4,
            )
            qr.add_data(codigo)
            qr.make(fit=True)
            
            # Cria imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Redimensiona para caber na tela
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            
            # Converte para PhotoImage
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"Erro ao gerar QR Code: {e}")
            return None
    
    def copiar_codigo(self):
        """Copia o código PIX para a área de transferência."""
        if self.qr_code_data and self.qr_code_data["qr_code"]:
            self.clipboard_clear()
            self.clipboard_append(self.qr_code_data["qr_code"])
            self.label_status.config(text="📋 Código copiado para área de transferência!", fg="#27ae60")
            self.after(3000, lambda: self.label_status.config(
                text="📱 PIX Gerado - Aguardando Pagamento", fg="#3498db"))
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento do pagamento."""
        if self.payment_id:
            pix_monitor.adicionar_monitoramento(
                self.payment_id,
                self.pagamento_aprovado,
                self.pagamento_erro
            )
    
    def iniciar_countdown(self, segundos_restantes):
        """Inicia o countdown do PIX."""
        def atualizar_timer():
            if not self.timer_ativo:
                return segundos_restantes
            
            if segundos_restantes > 0:
                minutos = segundos_restantes // 60
                segundos = segundos_restantes % 60
                if hasattr(self, 'label_timer') and self.label_timer.winfo_exists():
                    self.label_timer.config(text=f"⏱️ PIX expira em {minutos:02d}:{segundos:02d} minutos")
                self.after(1000, atualizar_timer)
                return segundos_restantes - 1
            else:
                self.pix_expirado()
                return 0
        
        atualizar_timer()
    
    def pagamento_aprovado(self):
        """Callback quando pagamento é aprovado."""
        # Para o timer
        self.timer_ativo = False
        
        self.label_status.config(text="✅ PAGAMENTO PIX APROVADO!", fg="#27ae60")
        
        # Mostra confirmação visual
        self.mostrar_confirmacao_aprovado()
        
        # Chama callback após 2 segundos
        self.after(2000, self.callback_aprovado)
    
    def pagamento_erro(self, motivo: str):
        """Callback quando há erro no pagamento."""
        # Para o timer
        self.timer_ativo = False
        
        self.label_status.config(text=f"❌ {motivo.upper()}", fg="#e74c3c")
        
        # Remove do monitoramento
        if self.payment_id:
            pix_monitor.remover_monitoramento(self.payment_id)
        
        # Chama callback após 3 segundos
        self.after(3000, lambda: self.callback_cancelado(motivo))
    
    def pix_expirado(self):
        """Callback quando PIX expira."""
        # Para o timer
        self.timer_ativo = False
        
        self.label_status.config(text="⏰ PIX EXPIRADO", fg="#e74c3c")
        
        # Cancela pagamento no Mercado Pago
        if self.payment_id:
            mercado_pago_service.cancelar_pagamento(self.payment_id)
            pix_monitor.remover_monitoramento(self.payment_id)
        
        # Chama callback após 2 segundos
        self.after(2000, lambda: self.callback_cancelado("PIX expirado"))
    
    def mostrar_confirmacao_aprovado(self):
        """Mostra animação de confirmação."""
        # Limpa container
        for widget in self.qr_container.winfo_children():
            widget.destroy()
        
        # Mostra confirmação grande
        confirmacao_frame = tk.Frame(self.qr_container, bg="#27ae60", relief=tk.RAISED, bd=5)
        confirmacao_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(confirmacao_frame, text="✅", font=("Arial", 72, "bold"),
                 bg="#27ae60", fg="white").pack(expand=True)
        
        tk.Label(confirmacao_frame, text="PAGAMENTO APROVADO!", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white").pack(expand=True)
    
    def cancelar_pix(self):
        """Cancela o PIX."""
        # Para o timer
        self.timer_ativo = False
        
        self.label_status.config(text="🔄 Cancelando PIX...", fg="#f39c12")
        
        # Cancela no Mercado Pago
        if self.payment_id:
            sucesso = mercado_pago_service.cancelar_pagamento(self.payment_id)
            pix_monitor.remover_monitoramento(self.payment_id)
            
            if sucesso:
                self.label_status.config(text="❌ PIX CANCELADO", fg="#e74c3c")
            else:
                self.label_status.config(text="⚠️ Erro ao cancelar - contate suporte", fg="#e67e22")
        
        # Chama callback após 1 segundo
        self.after(1000, lambda: self.callback_cancelado("Cancelado pelo usuário"))
    
    def mostrar_erro(self, mensagem: str):
        """Mostra mensagem de erro."""
        self.label_status.config(text=f"❌ {mensagem.upper()}", fg="#e74c3c")
        
        # Chama callback após 3 segundos
        self.after(3000, lambda: self.callback_cancelado(mensagem))