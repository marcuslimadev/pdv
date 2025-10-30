"""
Estilos modernos e bonitos para o sistema PDV.
Inclui cores, fontes e configurações visuais DINÂMICAS e configuráveis.
"""

import tkinter as tk
from tkinter import ttk


class ModernStyles:
    """Estilos modernos para o sistema - CONFIGURÁVEIS DINAMICAMENTE."""
    
    # Configurações carregadas do banco (serão atualizadas pelo carregador)
    _config = None
    
    # ===== PALETA DE CORES PADRÃO (fallback) =====
    PRIMARY = "#6C5CE7"
    PRIMARY_DARK = "#5F3DC4"
    PRIMARY_LIGHT = "#A29BFE"
    
    SUCCESS = "#00B894"
    SUCCESS_DARK = "#00916E"
    SUCCESS_LIGHT = "#55EFC4"
    
    DANGER = "#FF7675"
    DANGER_DARK = "#D63031"
    
    WARNING = "#FDCB6E"
    WARNING_DARK = "#F39C12"
    
    INFO = "#74B9FF"
    INFO_DARK = "#0984E3"
    
    DARK = "#2D3436"
    GRAY_DARK = "#636E72"
    GRAY = "#B2BEC3"
    GRAY_LIGHT = "#DFE6E9"
    LIGHT = "#F8F9FA"
    WHITE = "#FFFFFF"
    
    BG_MAIN = "#F8F9FA"
    BG_SECONDARY = "#FFFFFF"
    BG_DARK = "#2D3436"
    
    TEXT_PRIMARY = "#2D3436"
    TEXT_SECONDARY = "#636E72"
    TEXT_LIGHT = "#B2BEC3"
    TEXT_WHITE = "#FFFFFF"
    
    FOCUS_BORDER = "#6C5CE7"
    FOCUS_BG = "#F5F3FF"
    FOCUS_SHADOW = "#6C5CE740"
    
    # ===== FONTES PADRÃO =====
    FONT_FAMILY = "Segoe UI"
    FONT_FAMILY_ALT = "Calibri"
    FONT_MONO = "Consolas"
    
    FONT_SMALL = 9
    FONT_NORMAL = 11
    FONT_MEDIUM = 13
    FONT_LARGE = 16
    FONT_XLARGE = 20
    FONT_XXLARGE = 28
    FONT_HUGE = 42
    
    # ===== DIMENSÕES PADRÃO =====
    BORDER_RADIUS = 12
    BORDER_WIDTH = 2
    PADDING_SMALL = 8
    PADDING_MEDIUM = 15
    PADDING_LARGE = 25
    
    @classmethod
    def carregar_configuracoes(cls):
        """Carrega configurações de aparência do banco de dados"""
        try:
            from src.services.aparencia_service import AparenciaService
            service = AparenciaService()
            config = service.get_configuracoes()
            
            # Atualiza cores
            cls.PRIMARY = config.get('cor_primaria', cls.PRIMARY)
            cls.SUCCESS = config.get('cor_secundaria', cls.SUCCESS)
            cls.WARNING = config.get('cor_destaque', cls.WARNING)
            cls.DANGER = config.get('cor_perigo', cls.DANGER)
            cls.INFO = config.get('cor_info', cls.INFO)
            cls.TEXT_PRIMARY = config.get('cor_texto_primario', cls.TEXT_PRIMARY)
            cls.TEXT_SECONDARY = config.get('cor_texto_secundario', cls.TEXT_SECONDARY)
            cls.BG_MAIN = config.get('cor_fundo', cls.BG_MAIN)
            
            # Cores derivadas
            cls.FOCUS_BORDER = cls.PRIMARY
            cls.PRIMARY_DARK = cls._escurecer_cor(cls.PRIMARY, 0.2)
            cls.PRIMARY_LIGHT = cls._clarear_cor(cls.PRIMARY, 0.3)
            cls.SUCCESS_DARK = cls._escurecer_cor(cls.SUCCESS, 0.2)
            cls.SUCCESS_LIGHT = cls._clarear_cor(cls.SUCCESS, 0.3)
            cls.DANGER_DARK = cls._escurecer_cor(cls.DANGER, 0.2)
            cls.WARNING_DARK = cls._escurecer_cor(cls.WARNING, 0.2)
            cls.INFO_DARK = cls._escurecer_cor(cls.INFO, 0.2)
            
            # Atualiza fontes
            cls.FONT_FAMILY = config.get('fonte_principal', cls.FONT_FAMILY)
            cls.FONT_SMALL = config.get('tamanho_fonte_pequeno', cls.FONT_SMALL)
            cls.FONT_NORMAL = config.get('tamanho_fonte_normal', cls.FONT_NORMAL)
            cls.FONT_MEDIUM = config.get('tamanho_fonte_medio', cls.FONT_MEDIUM)
            cls.FONT_LARGE = config.get('tamanho_fonte_grande', cls.FONT_LARGE)
            cls.FONT_XLARGE = config.get('tamanho_fonte_xlarge', cls.FONT_XLARGE)
            cls.FONT_XXLARGE = config.get('tamanho_fonte_xxlarge', cls.FONT_XXLARGE)
            cls.FONT_HUGE = config.get('tamanho_fonte_huge', cls.FONT_HUGE)
            
            # Atualiza dimensões
            cls.BORDER_RADIUS = config.get('borda_arredondada', cls.BORDER_RADIUS)
            
            cls._config = config
            
        except Exception as e:
            # Fallback para valores padrão em caso de erro
            print(f"Erro ao carregar configurações de aparência: {e}")
            pass
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Converte cor hexadecimal para RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def _rgb_to_hex(rgb):
        """Converte RGB para hexadecimal"""
        return '#{:02x}{:02x}{:02x}'.format(
            max(0, min(255, int(rgb[0]))),
            max(0, min(255, int(rgb[1]))),
            max(0, min(255, int(rgb[2])))
        )
    
    @classmethod
    def _escurecer_cor(cls, hex_color, fator=0.2):
        """Escurece uma cor por um fator (0.0 a 1.0)"""
        rgb = cls._hex_to_rgb(hex_color)
        new_rgb = tuple(c * (1 - fator) for c in rgb)
        return cls._rgb_to_hex(new_rgb)
    
    @classmethod
    def _clarear_cor(cls, hex_color, fator=0.3):
        """Clareia uma cor por um fator (0.0 a 1.0)"""
        rgb = cls._hex_to_rgb(hex_color)
        new_rgb = tuple(c + (255 - c) * fator for c in rgb)
        return cls._rgb_to_hex(new_rgb)
    
    # ===== SOMBRAS =====
    SHADOW_LIGHT = "2 2 4 #00000015"
    SHADOW_MEDIUM = "0 4 8 #00000025"
    SHADOW_HEAVY = "0 8 16 #00000035"
    
    @classmethod
    def configure_ttk_styles(cls):
        """Configura estilos TTK modernos."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== TREEVIEW MODERNO =====
        style.configure(
            "Modern.Treeview",
            background=cls.WHITE,
            foreground=cls.TEXT_PRIMARY,
            fieldbackground=cls.WHITE,
            borderwidth=0,
            relief="flat",
            font=(cls.FONT_FAMILY, cls.FONT_NORMAL),
            rowheight=40
        )
        
        style.configure(
            "Modern.Treeview.Heading",
            background=cls.BG_DARK,
            foreground=cls.TEXT_WHITE,
            borderwidth=0,
            relief="flat",
            font=(cls.FONT_FAMILY, cls.FONT_MEDIUM, "bold")
        )
        
        style.map(
            "Modern.Treeview",
            background=[('selected', cls.PRIMARY_LIGHT)],
            foreground=[('selected', cls.DARK)]
        )
        
        style.map(
            "Modern.Treeview.Heading",
            background=[('active', cls.PRIMARY_DARK)],
            foreground=[('active', cls.WHITE)]
        )
        
        # ===== ENTRY MODERNO =====
        style.configure(
            "Modern.TEntry",
            fieldbackground=cls.WHITE,
            background=cls.WHITE,
            foreground=cls.TEXT_PRIMARY,
            borderwidth=2,
            relief="flat",
            font=(cls.FONT_FAMILY, cls.FONT_NORMAL)
        )
        
        # ===== FRAME MODERNO =====
        style.configure(
            "Modern.TFrame",
            background=cls.BG_MAIN,
            borderwidth=0
        )
        
        style.configure(
            "Card.TFrame",
            background=cls.WHITE,
            borderwidth=0,
            relief="flat"
        )
    
    @classmethod
    def create_modern_button(cls, parent, text, command=None, style="primary", width=None):
        """
        Cria um botão moderno com cantos arredondados e hover.
        
        Args:
            parent: Widget pai
            text: Texto do botão
            command: Função a ser executada
            style: Estilo do botão (primary, success, danger, warning, info, secondary)
            width: Largura do botão (None para automático)
        """
        # Cores baseadas no estilo
        styles_config = {
            "primary": {
                "bg": cls.PRIMARY,
                "hover_bg": cls.PRIMARY_DARK,
                "active_bg": "#4834D4",
                "fg": cls.TEXT_WHITE
            },
            "success": {
                "bg": cls.SUCCESS,
                "hover_bg": cls.SUCCESS_DARK,
                "active_bg": "#00695C",
                "fg": cls.TEXT_WHITE
            },
            "danger": {
                "bg": cls.DANGER,
                "hover_bg": cls.DANGER_DARK,
                "active_bg": "#C0392B",
                "fg": cls.TEXT_WHITE
            },
            "warning": {
                "bg": cls.WARNING,
                "hover_bg": cls.WARNING_DARK,
                "active_bg": "#D68910",
                "fg": cls.TEXT_PRIMARY
            },
            "info": {
                "bg": cls.INFO,
                "hover_bg": cls.INFO_DARK,
                "active_bg": "#0652DD",
                "fg": cls.TEXT_WHITE
            },
            "secondary": {
                "bg": cls.GRAY_LIGHT,
                "hover_bg": cls.GRAY,
                "active_bg": cls.GRAY_DARK,
                "fg": cls.TEXT_PRIMARY
            }
        }
        
        config = styles_config.get(style, styles_config["primary"])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=(cls.FONT_FAMILY, cls.FONT_MEDIUM, "bold"),
            bg=config["bg"],
            fg=config["fg"],
            activebackground=config["active_bg"],
            activeforeground=cls.TEXT_WHITE,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=cls.PADDING_LARGE,
            pady=cls.PADDING_MEDIUM,
            highlightthickness=0
        )
        
        if width:
            btn.config(width=width)
        
        # Efeito hover
        def on_enter(e):
            btn.config(bg=config["hover_bg"])
        
        def on_leave(e):
            btn.config(bg=config["bg"])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    @classmethod
    def create_modern_entry(cls, parent, placeholder="", font_size=None, **kwargs):
        """
        Cria um campo de entrada moderno com foco visual.
        
        Args:
            parent: Widget pai
            placeholder: Texto placeholder
            font_size: Tamanho da fonte
            **kwargs: Argumentos adicionais para Entry
        """
        if font_size is None:
            font_size = cls.FONT_NORMAL
        
        # Frame container com borda
        container = tk.Frame(
            parent,
            bg=cls.GRAY_LIGHT,
            highlightthickness=2,
            highlightbackground=cls.GRAY_LIGHT,
            highlightcolor=cls.FOCUS_BORDER
        )
        
        entry = tk.Entry(
            container,
            font=(cls.FONT_FAMILY, font_size),
            bg=cls.WHITE,
            fg=cls.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            insertwidth=3,
            insertbackground=cls.PRIMARY,
            **kwargs
        )
        entry.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=cls.TEXT_LIGHT)
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=cls.TEXT_PRIMARY)
                container.config(highlightbackground=cls.FOCUS_BORDER, bg=cls.FOCUS_BG)
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=cls.TEXT_LIGHT)
                container.config(highlightbackground=cls.GRAY_LIGHT, bg=cls.WHITE)
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        else:
            # Efeito de foco sem placeholder
            def on_focus_in(e):
                container.config(highlightbackground=cls.FOCUS_BORDER, bg=cls.FOCUS_BG)
            
            def on_focus_out(e):
                container.config(highlightbackground=cls.GRAY_LIGHT, bg=cls.WHITE)
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        # Salva referência ao entry no container para facilitar acesso
        container.entry = entry
        
        return container
    
    @classmethod
    def create_card(cls, parent, title=None, **kwargs):
        """
        Cria um card moderno (frame com sombra e cantos arredondados simulados).
        
        Args:
            parent: Widget pai
            title: Título do card (opcional)
            **kwargs: Argumentos adicionais
        """
        # Frame externo (sombra simulada)
        shadow = tk.Frame(parent, bg=cls.GRAY_LIGHT)
        
        # Frame do card
        card = tk.Frame(
            shadow,
            bg=cls.WHITE,
            relief="flat",
            borderwidth=0,
            **kwargs
        )
        card.pack(padx=2, pady=2, fill="both", expand=True)
        
        # Título do card
        if title:
            header = tk.Frame(card, bg=cls.BG_DARK, height=50)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text=title,
                font=(cls.FONT_FAMILY, cls.FONT_LARGE, "bold"),
                bg=cls.BG_DARK,
                fg=cls.TEXT_WHITE
            ).pack(pady=cls.PADDING_MEDIUM)
        
        # Área de conteúdo
        content = tk.Frame(card, bg=cls.WHITE)
        content.pack(fill="both", expand=True, padx=cls.PADDING_LARGE, pady=cls.PADDING_LARGE)
        
        # Salva referência ao conteúdo
        shadow.content = content
        shadow.card = card
        
        return shadow
    
    @classmethod
    def apply_focus_style(cls, widget, focused=True):
        """
        Aplica estilo de foco a um widget.
        
        Args:
            widget: Widget para aplicar o estilo
            focused: True para foco, False para remover
        """
        if focused:
            widget.config(
                highlightthickness=3,
                highlightbackground=cls.FOCUS_BORDER,
                highlightcolor=cls.FOCUS_BORDER
            )
        else:
            widget.config(
                highlightthickness=0
            )
