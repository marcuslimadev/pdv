"""
Janela de configuração de aparência do sistema
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from src.services.aparencia_service import AparenciaService
from src.ui.styles import ModernStyles


class AparenciaWindow(tk.Toplevel):
    """Janela para configurar aparência do sistema"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Configurações de Aparência")
        self.geometry("900x700")
        self.configure(bg=ModernStyles.BG_MAIN)
        
        self.service = AparenciaService()
        self.config_atual = self.service.get_configuracoes()
        
        # Dicionários para armazenar widgets de cor
        self.cor_buttons = {}
        self.cor_valores = {}
        
        self.criar_interface()
        self.carregar_valores()
    
    def criar_interface(self):
        """Cria a interface"""
        # Título
        titulo_frame = tk.Frame(self, bg=ModernStyles.PRIMARY, height=60)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(
            titulo_frame,
            text="🎨 CONFIGURAÇÕES DE APARÊNCIA",
            font=(ModernStyles.FONT_FAMILY, 18, "bold"),
            bg=ModernStyles.PRIMARY,
            fg=ModernStyles.TEXT_WHITE
        ).pack(expand=True)
        
        # Área de scroll
        canvas = tk.Canvas(self, bg=ModernStyles.BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg=ModernStyles.BG_MAIN)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Abas
        notebook = ttk.Notebook(self.scrollable_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba Cores
        self.aba_cores = tk.Frame(notebook, bg=ModernStyles.WHITE)
        notebook.add(self.aba_cores, text="Cores")
        self.criar_aba_cores()
        
        # Aba Fontes
        self.aba_fontes = tk.Frame(notebook, bg=ModernStyles.WHITE)
        notebook.add(self.aba_fontes, text="Fontes e Tamanhos")
        self.criar_aba_fontes()
        
        # Aba Logotipo
        self.aba_logotipo = tk.Frame(notebook, bg=ModernStyles.WHITE)
        notebook.add(self.aba_logotipo, text="Logotipo")
        self.criar_aba_logotipo()
        
        # Botões de ação
        self.criar_botoes_acao()
    
    def criar_aba_cores(self):
        """Cria aba de configuração de cores"""
        container = tk.Frame(self.aba_cores, bg=ModernStyles.WHITE)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cores principais
        self.criar_secao_cor(container, "Cores Principais", [
            ("cor_primaria", "Cor Primária", "Cor principal do sistema (botões, destaques)"),
            ("cor_secundaria", "Cor Secundária", "Cor de sucesso (confirmações, positivo)"),
            ("cor_destaque", "Cor de Destaque", "Cor de avisos e destaques"),
        ])
        
        # Cores de ação
        self.criar_secao_cor(container, "Cores de Ação", [
            ("cor_perigo", "Cor de Perigo", "Cor para ações perigosas (cancelar, excluir)"),
            ("cor_info", "Cor de Informação", "Cor para informações neutras"),
            ("cor_aviso", "Cor de Aviso", "Cor para alertas e avisos"),
        ])
        
        # Cores de texto
        self.criar_secao_cor(container, "Cores de Texto", [
            ("cor_texto_primario", "Texto Principal", "Cor do texto principal"),
            ("cor_texto_secundario", "Texto Secundário", "Cor do texto secundário/legendas"),
        ])
        
        # Cor de fundo
        self.criar_secao_cor(container, "Cor de Fundo", [
            ("cor_fundo", "Fundo Principal", "Cor de fundo do sistema"),
        ])
    
    def criar_secao_cor(self, parent, titulo, cores):
        """Cria uma seção de configuração de cores"""
        frame = tk.LabelFrame(
            parent,
            text=titulo,
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, pady=10)
        
        for chave, label, descricao in cores:
            self.criar_campo_cor(frame, chave, label, descricao)
    
    def criar_campo_cor(self, parent, chave, label, descricao):
        """Cria um campo de seleção de cor"""
        frame = tk.Frame(parent, bg=ModernStyles.WHITE)
        frame.pack(fill=tk.X, pady=8)
        
        # Label
        label_widget = tk.Label(
            frame,
            text=label,
            font=(ModernStyles.FONT_FAMILY, 11, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            width=20,
            anchor="w"
        )
        label_widget.pack(side=tk.LEFT, padx=(0, 10))
        
        # Valor atual (cor)
        cor_atual = self.config_atual.get(chave, "#FFFFFF")
        self.cor_valores[chave] = cor_atual
        
        # Botão de cor
        btn_cor = tk.Button(
            frame,
            text="",
            bg=cor_atual,
            width=10,
            height=2,
            relief="raised",
            bd=2,
            command=lambda k=chave: self.escolher_cor(k)
        )
        btn_cor.pack(side=tk.LEFT, padx=(0, 10))
        self.cor_buttons[chave] = btn_cor
        
        # Label com código da cor
        label_codigo = tk.Label(
            frame,
            text=cor_atual,
            font=(ModernStyles.FONT_FAMILY, 10),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY,
            width=10
        )
        label_codigo.pack(side=tk.LEFT, padx=(0, 10))
        self.cor_buttons[f"{chave}_label"] = label_codigo
        
        # Descrição
        tk.Label(
            frame,
            text=descricao,
            font=(ModernStyles.FONT_FAMILY, 9, "italic"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(side=tk.LEFT)
    
    def escolher_cor(self, chave):
        """Abre seletor de cor"""
        cor_atual = self.cor_valores.get(chave, "#FFFFFF")
        cor = colorchooser.askcolor(color=cor_atual, title=f"Escolher cor")
        
        if cor[1]:  # cor[1] contém o valor hexadecimal
            self.cor_valores[chave] = cor[1]
            self.cor_buttons[chave].config(bg=cor[1])
            self.cor_buttons[f"{chave}_label"].config(text=cor[1])
    
    def criar_aba_fontes(self):
        """Cria aba de configuração de fontes"""
        container = tk.Frame(self.aba_fontes, bg=ModernStyles.WHITE)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Fonte principal
        frame_fonte = tk.LabelFrame(
            container,
            text="Fonte Principal",
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            padx=15,
            pady=15
        )
        frame_fonte.pack(fill=tk.X, pady=10)
        
        tk.Label(
            frame_fonte,
            text="Família da Fonte:",
            font=(ModernStyles.FONT_FAMILY, 11),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 5))
        
        self.entry_fonte = tk.Entry(
            frame_fonte,
            font=(ModernStyles.FONT_FAMILY, 11),
            width=30
        )
        self.entry_fonte.pack(anchor="w", pady=(0, 5))
        
        tk.Label(
            frame_fonte,
            text="Exemplos: Segoe UI, Arial, Calibri, Tahoma",
            font=(ModernStyles.FONT_FAMILY, 9, "italic"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(anchor="w")
        
        # Tamanhos de fonte
        frame_tamanhos = tk.LabelFrame(
            container,
            text="Tamanhos de Fonte (pixels)",
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            padx=15,
            pady=15
        )
        frame_tamanhos.pack(fill=tk.X, pady=10)
        
        self.entries_tamanhos = {}
        tamanhos = [
            ("tamanho_fonte_pequeno", "Pequeno", "Textos muito pequenos, notas"),
            ("tamanho_fonte_normal", "Normal", "Texto padrão do sistema"),
            ("tamanho_fonte_medio", "Médio", "Títulos de seção, botões"),
            ("tamanho_fonte_grande", "Grande", "Títulos importantes"),
            ("tamanho_fonte_xlarge", "Extra Grande", "Destaques"),
            ("tamanho_fonte_xxlarge", "XX Grande", "Campos de entrada grandes"),
            ("tamanho_fonte_huge", "Enorme", "Valores principais (totais)"),
        ]
        
        for chave, label, descricao in tamanhos:
            self.criar_campo_tamanho(frame_tamanhos, chave, label, descricao)
        
        # Borda arredondada
        frame_borda = tk.LabelFrame(
            container,
            text="Bordas",
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            padx=15,
            pady=15
        )
        frame_borda.pack(fill=tk.X, pady=10)
        
        self.criar_campo_tamanho(frame_borda, "borda_arredondada", "Raio da Borda", "Arredondamento dos cantos (0 = quadrado)")
    
    def criar_campo_tamanho(self, parent, chave, label, descricao):
        """Cria campo de entrada para tamanho"""
        frame = tk.Frame(parent, bg=ModernStyles.WHITE)
        frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            frame,
            text=label,
            font=(ModernStyles.FONT_FAMILY, 10, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY,
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        entry = tk.Entry(frame, font=(ModernStyles.FONT_FAMILY, 10), width=10)
        entry.pack(side=tk.LEFT, padx=10)
        self.entries_tamanhos[chave] = entry
        
        tk.Label(
            frame,
            text=descricao,
            font=(ModernStyles.FONT_FAMILY, 9, "italic"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(side=tk.LEFT)
    
    def criar_aba_logotipo(self):
        """Cria aba de configuração de logotipo"""
        container = tk.Frame(self.aba_logotipo, bg=ModernStyles.WHITE)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Checkbox para mostrar logotipo
        self.var_mostrar_logo = tk.BooleanVar()
        chk_logo = tk.Checkbutton(
            container,
            text="Mostrar logotipo no sistema",
            variable=self.var_mostrar_logo,
            font=(ModernStyles.FONT_FAMILY, 11, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        )
        chk_logo.pack(anchor="w", pady=10)
        
        # Arquivo do logotipo
        frame_arquivo = tk.Frame(container, bg=ModernStyles.WHITE)
        frame_arquivo.pack(fill=tk.X, pady=10)
        
        tk.Label(
            frame_arquivo,
            text="Arquivo do Logotipo:",
            font=(ModernStyles.FONT_FAMILY, 11),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 5))
        
        frame_path = tk.Frame(frame_arquivo, bg=ModernStyles.WHITE)
        frame_path.pack(fill=tk.X)
        
        self.entry_logo_path = tk.Entry(
            frame_path,
            font=(ModernStyles.FONT_FAMILY, 10),
            width=50
        )
        self.entry_logo_path.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            frame_path,
            text="Procurar...",
            command=self.procurar_logotipo,
            font=(ModernStyles.FONT_FAMILY, 10),
            bg=ModernStyles.INFO,
            fg=ModernStyles.TEXT_WHITE,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        tk.Label(
            frame_arquivo,
            text="Formatos aceitos: PNG, JPG, JPEG, GIF",
            font=(ModernStyles.FONT_FAMILY, 9, "italic"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(anchor="w", pady=(5, 0))
        
        # Dimensões
        frame_dimensoes = tk.Frame(container, bg=ModernStyles.WHITE)
        frame_dimensoes.pack(fill=tk.X, pady=20)
        
        tk.Label(
            frame_dimensoes,
            text="Largura (pixels):",
            font=(ModernStyles.FONT_FAMILY, 10),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_logo_largura = tk.Entry(
            frame_dimensoes,
            font=(ModernStyles.FONT_FAMILY, 10),
            width=10
        )
        self.entry_logo_largura.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(
            frame_dimensoes,
            text="Altura (pixels):",
            font=(ModernStyles.FONT_FAMILY, 10),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.entry_logo_altura = tk.Entry(
            frame_dimensoes,
            font=(ModernStyles.FONT_FAMILY, 10),
            width=10
        )
        self.entry_logo_altura.pack(side=tk.LEFT)
    
    def procurar_logotipo(self):
        """Abre diálogo para selecionar arquivo de logotipo"""
        filename = filedialog.askopenfilename(
            title="Selecionar Logotipo",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("GIF", "*.gif"),
                ("Todos", "*.*")
            ]
        )
        if filename:
            self.entry_logo_path.delete(0, tk.END)
            self.entry_logo_path.insert(0, filename)
    
    def criar_botoes_acao(self):
        """Cria botões de ação"""
        frame_botoes = tk.Frame(self, bg=ModernStyles.BG_MAIN)
        frame_botoes.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            frame_botoes,
            text="💾 Salvar Configurações",
            command=self.salvar,
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.SUCCESS,
            fg=ModernStyles.TEXT_WHITE,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botoes,
            text="🔄 Restaurar Padrão",
            command=self.restaurar_padrao,
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.WARNING,
            fg=ModernStyles.TEXT_PRIMARY,
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botoes,
            text="❌ Cancelar",
            command=self.destroy,
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),
            bg=ModernStyles.DANGER,
            fg=ModernStyles.TEXT_WHITE,
            padx=20,
            pady=10
        ).pack(side=tk.RIGHT, padx=5)
    
    def carregar_valores(self):
        """Carrega valores atuais nos campos"""
        # Fontes
        self.entry_fonte.insert(0, self.config_atual.get('fonte_principal', 'Segoe UI'))
        
        # Tamanhos
        for chave in self.entries_tamanhos:
            valor = self.config_atual.get(chave, 10)
            self.entries_tamanhos[chave].insert(0, str(valor))
        
        # Logotipo
        self.var_mostrar_logo.set(self.config_atual.get('mostrar_logotipo', False))
        logo_path = self.config_atual.get('logotipo_path', '')
        if logo_path:
            self.entry_logo_path.insert(0, logo_path)
        
        self.entry_logo_largura.insert(0, str(self.config_atual.get('logotipo_largura', 150)))
        self.entry_logo_altura.insert(0, str(self.config_atual.get('logotipo_altura', 50)))
    
    def salvar(self):
        """Salva as configurações"""
        try:
            config = {}
            
            # Cores
            for chave in self.cor_valores:
                config[chave] = self.cor_valores[chave]
            
            # Fonte
            config['fonte_principal'] = self.entry_fonte.get()
            
            # Tamanhos
            for chave in self.entries_tamanhos:
                valor = self.entries_tamanhos[chave].get()
                config[chave] = int(valor) if valor.isdigit() else 10
            
            # Logotipo
            config['mostrar_logotipo'] = self.var_mostrar_logo.get()
            config['logotipo_path'] = self.entry_logo_path.get() or None
            
            largura = self.entry_logo_largura.get()
            config['logotipo_largura'] = int(largura) if largura.isdigit() else 150
            
            altura = self.entry_logo_altura.get()
            config['logotipo_altura'] = int(altura) if altura.isdigit() else 50
            
            # Salva
            if self.service.salvar_configuracoes(config):
                messagebox.showinfo(
                    "Sucesso",
                    "Configurações salvas com sucesso!\n\nReinicie o sistema para aplicar as mudanças.",
                    parent=self
                )
                self.destroy()
            else:
                messagebox.showerror(
                    "Erro",
                    "Erro ao salvar configurações.",
                    parent=self
                )
                
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao salvar: {str(e)}",
                parent=self
            )
    
    def restaurar_padrao(self):
        """Restaura configurações padrão"""
        if messagebox.askyesno(
            "Confirmar",
            "Deseja realmente restaurar as configurações padrão?\n\nEsta ação não pode ser desfeita.",
            parent=self
        ):
            if self.service.restaurar_padrao():
                messagebox.showinfo(
                    "Sucesso",
                    "Configurações restauradas para o padrão!\n\nReinicie o sistema para aplicar as mudanças.",
                    parent=self
                )
                self.destroy()
            else:
                messagebox.showerror(
                    "Erro",
                    "Erro ao restaurar configurações.",
                    parent=self
                )
