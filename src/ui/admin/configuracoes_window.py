"""
Janela de configurações do sistema (admin).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.services.config_service import config_service, PERCENTUAL_CLIENTE, PERCENTUAL_PLATAFORMA, PIX_PLATAFORMA


class ConfiguracoesFrame(ttk.Frame):
    """Frame para configuração do sistema."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._criar_interface()
        self._carregar_configuracoes()
    
    def _criar_interface(self):
        """Cria a interface de configurações."""
        # Título
        titulo = ttk.Label(
            self,
            text="Configurações do Sistema",
            font=("Segoe UI", 16, "bold")
        )
        titulo.pack(pady=20)
        
        # Notebook (abas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Aba PIX
        frame_pix = ttk.Frame(notebook, padding=20)
        notebook.add(frame_pix, text="PIX")
        
        # Aba Mercado Pago
        frame_mp = ttk.Frame(notebook, padding=20)
        notebook.add(frame_mp, text="Mercado Pago")
        
        self._criar_aba_pix(frame_pix)
        self._criar_aba_mercadopago(frame_mp)
    
    def _criar_aba_pix(self, parent):
        """Cria a aba de configurações PIX."""
        # Info sobre split fixo
        info_frame = ttk.LabelFrame(parent, text="Divisão de Pagamentos (Fixo)", padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            info_frame,
            text=f"• Cliente recebe: {PERCENTUAL_CLIENTE}% de cada pagamento PIX",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Label(
            info_frame,
            text=f"• Plataforma recebe: {PERCENTUAL_PLATAFORMA}% de cada pagamento PIX",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Label(
            info_frame,
            text=f"• PIX da Plataforma: {PIX_PLATAFORMA}",
            font=("Segoe UI", 10, "bold"),
            foreground="#007ACC"
        ).pack(anchor=tk.W, pady=2)
        
        # Configurações do cliente
        config_frame = ttk.LabelFrame(parent, text="Dados do Estabelecimento", padding=15)
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chave PIX
        ttk.Label(config_frame, text="Chave PIX:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_chave_pix = ttk.Entry(config_frame, width=40)
        self.entry_chave_pix.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(
            config_frame,
            text="(CPF, CNPJ, e-mail, telefone ou chave aleatória)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Nome do beneficiário
        ttk.Label(config_frame, text="Nome do Estabelecimento:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_nome = ttk.Entry(config_frame, width=40)
        self.entry_nome.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Cidade
        ttk.Label(config_frame, text="Cidade:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_cidade = ttk.Entry(config_frame, width=40)
        self.entry_cidade.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        config_frame.columnconfigure(1, weight=1)
        
        # Botão salvar
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            btn_frame,
            text="Salvar Configurações PIX",
            command=self._salvar_pix,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)
    
    def _criar_aba_mercadopago(self, parent):
        """Cria a aba de configurações do Mercado Pago."""
        # Info
        info_label = ttk.Label(
            parent,
            text="Configure sua integração com Mercado Pago para aceitar pagamentos PIX online.",
            font=("Segoe UI", 10),
            foreground="gray"
        )
        info_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Access Token
        token_frame = ttk.LabelFrame(parent, text="Credenciais de Acesso", padding=15)
        token_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(token_frame, text="Access Token:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_mp_token = ttk.Entry(token_frame, width=60, show="*")
        self.entry_mp_token.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(
            token_frame,
            text="Obtido no painel do Mercado Pago > Suas integrações > Credenciais",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Botão mostrar/ocultar
        self.btn_mostrar_token = ttk.Button(
            token_frame,
            text="👁 Mostrar",
            command=self._toggle_token_visibility,
            width=10
        )
        self.btn_mostrar_token.grid(row=0, column=2, padx=(10, 0))
        
        token_frame.columnconfigure(1, weight=1)
        
        # Link útil
        link_frame = ttk.Frame(parent)
        link_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            link_frame,
            text="📖 Como obter access token:",
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)
        
        link_label = ttk.Label(
            link_frame,
            text="https://www.mercadopago.com.br/developers/pt/docs/credentials",
            font=("Segoe UI", 9),
            foreground="#007ACC",
            cursor="hand2"
        )
        link_label.pack(anchor=tk.W, padx=(20, 0))
        
        # Botão salvar
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            btn_frame,
            text="Salvar Configurações Mercado Pago",
            command=self._salvar_mercadopago,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)
    
    def _carregar_configuracoes(self):
        """Carrega as configurações atuais."""
        # PIX
        self.entry_chave_pix.insert(0, config_service.get_pix_chave_cliente())
        self.entry_nome.insert(0, config_service.get_pix_nome_beneficiario())
        self.entry_cidade.insert(0, config_service.get_pix_cidade())
        
        # Mercado Pago
        token = config_service.get_mercadopago_access_token()
        if token:
            self.entry_mp_token.insert(0, token)
    
    def _toggle_token_visibility(self):
        """Alterna visibilidade do token."""
        if self.entry_mp_token.cget("show") == "*":
            self.entry_mp_token.configure(show="")
            self.btn_mostrar_token.configure(text="🔒 Ocultar")
        else:
            self.entry_mp_token.configure(show="*")
            self.btn_mostrar_token.configure(text="👁 Mostrar")
    
    def _salvar_pix(self):
        """Salva configurações PIX."""
        try:
            chave = self.entry_chave_pix.get().strip()
            nome = self.entry_nome.get().strip()
            cidade = self.entry_cidade.get().strip()
            
            if not chave:
                messagebox.showwarning(
                    "Atenção",
                    "Informe a chave PIX do estabelecimento."
                )
                self.entry_chave_pix.focus()
                return
            
            if not nome:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do estabelecimento."
                )
                self.entry_nome.focus()
                return
            
            if not cidade:
                messagebox.showwarning(
                    "Atenção",
                    "Informe a cidade."
                )
                self.entry_cidade.focus()
                return
            
            # Salvar
            config_service.set_pix_chave_cliente(chave)
            config_service.set_pix_nome_beneficiario(nome)
            config_service.set_pix_cidade(cidade)
            
            messagebox.showinfo(
                "Sucesso",
                "Configurações PIX salvas com sucesso!"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao salvar configurações PIX:\n{str(e)}"
            )
    
    def _salvar_mercadopago(self):
        """Salva configurações do Mercado Pago."""
        try:
            token = self.entry_mp_token.get().strip()
            
            if not token:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o Access Token do Mercado Pago."
                )
                self.entry_mp_token.focus()
                return
            
            # Salvar
            config_service.set_mercadopago_access_token(token)
            
            messagebox.showinfo(
                "Sucesso",
                "Configurações do Mercado Pago salvas com sucesso!"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao salvar configurações do Mercado Pago:\n{str(e)}"
            )
