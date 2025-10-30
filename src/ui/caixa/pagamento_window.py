"""
Janela de pagamento da venda.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from src.models.venda import Venda
from src.models.pagamento import Pagamento
from src.services.venda_service import VendaService
from src.services.pinpad_service import PinpadService
from src.utils.formatters import Formatters


class PagamentoWindow:
    """Janela para processar pagamentos."""
    
    def __init__(self, parent, venda: Venda, callback_finalizado):
        self.venda = venda
        self.callback_finalizado = callback_finalizado
        self.venda_service = VendaService()
        self.pinpad = PinpadService()
        self.pagamentos = []
        
        # Cria janela
        self.window = tk.Toplevel(parent)
        self.window.title("Pagamento da Venda")
        self.window.geometry("700x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Conecta pinpad
        self.pinpad.conectar()
        
        self.criar_widgets()
        
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
            text="💳 Pagamento",
            font=("Arial", 24, "bold"),
            fg="#27ae60"
        ).pack(pady=(0, 20))
        
        # Total da venda
        total_frame = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            total_frame,
            text="Valor Total:",
            font=("Arial", 14),
            bg="#ecf0f1"
        ).pack(pady=(10, 5))
        
        self.label_total = tk.Label(
            total_frame,
            text=Formatters.formatar_moeda(self.venda.total),
            font=("Arial", 28, "bold"),
            fg="#27ae60",
            bg="#ecf0f1"
        )
        self.label_total.pack(pady=(0, 10))
        
        # Valor restante
        tk.Label(
            total_frame,
            text="Valor Restante:",
            font=("Arial", 12),
            bg="#ecf0f1"
        ).pack()
        
        self.label_restante = tk.Label(
            total_frame,
            text=Formatters.formatar_moeda(self.venda.total),
            font=("Arial", 20, "bold"),
            fg="#e74c3c",
            bg="#ecf0f1"
        )
        self.label_restante.pack(pady=(0, 10))
        
        # Formas de pagamento
        formas_frame = ttk.LabelFrame(main_frame, text="Formas de Pagamento", padding="10")
        formas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Grid de botões
        btn_frame = ttk.Frame(formas_frame)
        btn_frame.pack(fill=tk.BOTH, expand=True)
        
        # Primeira linha
        self.criar_botao_pagamento(
            btn_frame, "💵 Dinheiro", "#27ae60", 
            lambda: self.processar_dinheiro(), 0, 0
        )
        
        self.criar_botao_pagamento(
            btn_frame, "💳 Débito", "#3498db",
            lambda: self.processar_debito(), 0, 1
        )
        
        # Segunda linha
        self.criar_botao_pagamento(
            btn_frame, "💳 Crédito", "#9b59b6",
            lambda: self.processar_credito(), 1, 0
        )
        
        self.criar_botao_pagamento(
            btn_frame, "📱 PIX", "#16a085",
            lambda: self.processar_pix(), 1, 1
        )
        
        # Botões de ação
        btn_action_frame = ttk.Frame(main_frame)
        btn_action_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_action_frame,
            text="Cancelar",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.cancelar
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_finalizar = tk.Button(
            btn_action_frame,
            text="✓ Finalizar Venda",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            state=tk.DISABLED,
            command=self.finalizar
        )
        self.btn_finalizar.pack(side=tk.RIGHT)
    
    def criar_botao_pagamento(self, parent, texto, cor, comando, row, col):
        """Cria um botão de forma de pagamento."""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Arial", 14, "bold"),
            bg=cor,
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=30,
            command=comando
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        parent.rowconfigure(row, weight=1)
        parent.columnconfigure(col, weight=1)
        
        return btn
    
    def get_valor_restante(self) -> Decimal:
        """Retorna o valor restante a pagar."""
        total_pago = sum(p.valor for p in self.pagamentos)
        return self.venda.total - total_pago
    
    def atualizar_valores(self):
        """Atualiza os valores exibidos."""
        restante = self.get_valor_restante()
        self.label_restante.config(text=Formatters.formatar_moeda(restante))
        
        if restante <= 0:
            self.label_restante.config(fg="#27ae60")
            self.btn_finalizar.config(state=tk.NORMAL)
        else:
            self.label_restante.config(fg="#e74c3c")
            self.btn_finalizar.config(state=tk.DISABLED)
    
    def processar_dinheiro(self):
        """Processa pagamento em dinheiro."""
        restante = self.get_valor_restante()
        
        # Janela para entrada do valor
        dialog = tk.Toplevel(self.window)
        dialog.title("Pagamento em Dinheiro")
        dialog.geometry("350x250")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="💵 Dinheiro",
            font=("Arial", 18, "bold"),
            fg="#27ae60"
        ).pack(pady=(0, 20))
        
        tk.Label(
            frame,
            text=f"Valor Restante: {Formatters.formatar_moeda(restante)}",
            font=("Arial", 12)
        ).pack(pady=(0, 15))
        
        tk.Label(frame, text="Valor Recebido:", font=("Arial", 11)).pack()
        
        entry_valor = ttk.Entry(frame, font=("Arial", 14), width=15)
        entry_valor.pack(pady=(5, 15))
        entry_valor.insert(0, f"{float(restante):.2f}".replace('.', ','))
        entry_valor.select_range(0, tk.END)
        entry_valor.focus()
        
        label_troco = tk.Label(frame, text="", font=("Arial", 12, "bold"), fg="#27ae60")
        label_troco.pack(pady=(10, 15))
        
        def calcular_troco(*args):
            try:
                valor_str = entry_valor.get().replace(',', '.')
                valor_recebido = Decimal(valor_str)
                troco = valor_recebido - restante
                if troco >= 0:
                    label_troco.config(text=f"Troco: {Formatters.formatar_moeda(troco)}")
                else:
                    label_troco.config(text="Valor insuficiente!", fg="#e74c3c")
            except:
                label_troco.config(text="")
        
        entry_valor.bind('<KeyRelease>', calcular_troco)
        calcular_troco()
        
        def confirmar():
            try:
                valor_str = entry_valor.get().replace(',', '.')
                valor = Decimal(valor_str)
                
                if valor < restante:
                    messagebox.showerror("Erro", "Valor insuficiente!")
                    return
                
                pagamento = Pagamento(
                    forma_pagamento=Pagamento.FORMA_DINHEIRO,
                    valor=restante,
                    status=Pagamento.STATUS_APROVADO
                )
                
                self.pagamentos.append(pagamento)
                self.atualizar_valores()
                
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        tk.Button(
            frame,
            text="Confirmar",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=confirmar
        ).pack()
        
        entry_valor.bind('<Return>', lambda e: confirmar())
    
    def processar_debito(self):
        """Processa pagamento no débito."""
        restante = self.get_valor_restante()
        
        # Simula processamento com pinpad
        messagebox.showinfo("Pinpad", "Insira o cartão no pinpad e digite a senha...")
        
        self.window.update()
        response = self.pinpad.venda_debito(restante)
        
        if response.sucesso:
            pagamento = Pagamento(
                forma_pagamento=Pagamento.FORMA_DEBITO,
                valor=restante,
                status=Pagamento.STATUS_APROVADO,
                nsu=response.nsu,
                codigo_autorizacao=response.codigo_autorizacao
            )
            
            self.pagamentos.append(pagamento)
            self.atualizar_valores()
            
            messagebox.showinfo("Sucesso", "Pagamento aprovado!")
        else:
            messagebox.showerror("Erro", f"Pagamento recusado!\n{response.mensagem}")
    
    def processar_credito(self):
        """Processa pagamento no crédito."""
        restante = self.get_valor_restante()
        
        # Janela para escolher parcelas
        dialog = tk.Toplevel(self.window)
        dialog.title("Pagamento no Crédito")
        dialog.geometry("300x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="💳 Crédito",
            font=("Arial", 18, "bold"),
            fg="#9b59b6"
        ).pack(pady=(0, 20))
        
        tk.Label(
            frame,
            text=f"Valor: {Formatters.formatar_moeda(restante)}",
            font=("Arial", 12)
        ).pack(pady=(0, 15))
        
        tk.Label(frame, text="Número de Parcelas:", font=("Arial", 11)).pack()
        
        parcelas_var = tk.StringVar(value="1")
        combo_parcelas = ttk.Combobox(
            frame,
            textvariable=parcelas_var,
            values=[str(i) for i in range(1, 13)],
            state="readonly",
            font=("Arial", 12),
            width=10
        )
        combo_parcelas.pack(pady=(5, 20))
        
        def confirmar():
            parcelas = int(parcelas_var.get())
            
            messagebox.showinfo("Pinpad", "Insira o cartão no pinpad e digite a senha...")
            dialog.update()
            
            response = self.pinpad.venda_credito(restante, parcelas)
            
            if response.sucesso:
                pagamento = Pagamento(
                    forma_pagamento=Pagamento.FORMA_CREDITO,
                    valor=restante,
                    numero_parcelas=parcelas,
                    status=Pagamento.STATUS_APROVADO,
                    nsu=response.nsu,
                    codigo_autorizacao=response.codigo_autorizacao
                )
                
                self.pagamentos.append(pagamento)
                self.atualizar_valores()
                
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Pagamento aprovado em {parcelas}x!")
            else:
                messagebox.showerror("Erro", f"Pagamento recusado!\n{response.mensagem}")
        
        tk.Button(
            frame,
            text="Confirmar",
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=confirmar
        ).pack()
    
    def processar_pix(self):
        """Processa pagamento via PIX."""
        restante = self.get_valor_restante()
        
        # Abre janela de PIX
        from src.ui.caixa.pix_window import PixWindow
        PixWindow(self.window, restante, self.callback_pix_aprovado)
    
    def callback_pix_aprovado(self, dados_pix):
        """Callback quando PIX é aprovado."""
        restante = self.get_valor_restante()
        
        pagamento = Pagamento(
            forma_pagamento=Pagamento.FORMA_PIX,
            valor=restante,
            status=Pagamento.STATUS_APROVADO,
            dados_pix=dados_pix
        )
        
        self.pagamentos.append(pagamento)
        self.atualizar_valores()
    
    def finalizar(self):
        """Finaliza a venda."""
        if self.get_valor_restante() > 0:
            messagebox.showerror("Erro", "Valor restante não pago!")
            return
        
        # Finaliza venda
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda(self.pagamentos)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.window.destroy()
            if self.callback_finalizado:
                self.callback_finalizado()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def cancelar(self):
        """Cancela o pagamento."""
        if messagebox.askyesno("Cancelar", "Deseja cancelar o pagamento?"):
            self.window.destroy()
