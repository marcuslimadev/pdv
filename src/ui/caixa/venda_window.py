"""
Tela de vendas com atalhos de teclado F2-F10 e interface otimizada.
Permite quantidade multiplicadora e navegação completa por teclado.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from src.models.usuario import Usuario
from src.models.caixa import Caixa
from src.services.venda_service import VendaService
from src.dao.produto_dao import ProdutoDAO
from src.utils.formatters import Formatters
from src.utils.logger import Logger
from src.ui.styles import ModernStyles


class VendaFrame(ttk.Frame):
    """Frame otimizado para operação de caixa por teclado."""
    
    def __init__(self, parent, usuario: Usuario, caixa: Caixa, callback_fechar_caixa):
        super().__init__(parent)
        
        # CARREGA CONFIGURAÇÕES DE APARÊNCIA DINÂMICAS
        ModernStyles.carregar_configuracoes()
        
        # Configura estilos modernos
        ModernStyles.configure_ttk_styles()
        
        self.usuario = usuario
        self.caixa = caixa
        self.callback_fechar_caixa = callback_fechar_caixa
        self.venda_service = VendaService()
        
        # Quantidade multiplicadora (digitar 3 antes de ler código)
        self.quantidade_digitada = ""
        
        # Inicia nova venda
        self.venda_service.iniciar_nova_venda(usuario.id, caixa.id)
        
        self.criar_widgets()
        self.configurar_atalhos()
        
        # Reconfigura atalhos quando a janela recebe foco
        self.bind('<FocusIn>', lambda e: self.after(50, self._reconfigurar_se_necessario))
        
        self.entry_codigo.entry.focus()  # Foco no entry interno
    
    def _reconfigurar_se_necessario(self):
        """Reconfigura atalhos se necessário (após janelas modais)."""
        if self.winfo_exists() and hasattr(self, 'entry_codigo'):
            try:
                if self.entry_codigo.winfo_exists():
                    self.configurar_atalhos()
                    self.entry_codigo.entry.focus_set()
            except:
                pass  # Ignora erros se widget foi destruído
    
    def configurar_atalhos(self):
        """Configura atalhos de teclado de forma organizada e sem duplicações."""
        # Limpa atalhos anteriores
        self._limpar_atalhos_principais()
        
        # Marca que estamos no modo venda (não pagamento)
        self.modo_pagamento = False
        
        # ===== ATALHOS PRINCIPAIS DE VENDA =====
        # F1-F2: Operações básicas
        self.bind_all('<F1>', self._handle_f1)              # Buscar produto / Dinheiro
        self.bind_all('<F2>', self._handle_f2)              # Adicionar por código / Débito
        self.bind_all('<F3>', self._handle_f3)              # Crédito (só em pagamento)
        self.bind_all('<F4>', self._handle_f4)              # PIX (só em pagamento)
        
        # F5-F6: Remoção e cancelamento
        self.bind_all('<F5>', self._handle_f5)              # Remover item
        self.bind_all('<F6>', self._handle_f6)              # Cancelar venda
        
        # F7-F8: Operações com autenticação admin
        self.bind_all('<F7>', self._handle_f7)              # Editar com admin
        self.bind_all('<F8>', self._handle_f8)              # Cancelar com admin
        
        # F9-F10: Finalização
        self.bind_all('<F9>', self._handle_f9)              # Fechar caixa
        self.bind_all('<F10>', self._handle_f10)            # Finalizar venda
        
        # ===== ATALHOS COM CTRL (ALTERNATIVOS) =====
        self.bind_all('<Control-n>', lambda e: self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id))
        self.bind_all('<Control-f>', lambda e: self.buscar_produto())
        self.bind_all('<Control-Return>', lambda e: self.finalizar_venda())
        
        # ===== NAVEGAÇÃO =====
        self.bind_all('<Delete>', lambda e: self.remover_item_selecionado())
        self.bind_all('<Escape>', self._handle_escape)
        self.bind_all('<Tab>', self._navegar_proximo)
        self.bind_all('<Shift-Tab>', self._navegar_anterior)
        
        # Navegação na lista
        self.bind_all('<Up>', self._navegar_lista_cima)
        self.bind_all('<Down>', self._navegar_lista_baixo)
        self.bind_all('<Home>', self._ir_primeiro_item)
        self.bind_all('<End>', self._ir_ultimo_item)
        self.bind_all('<Page_Up>', self._pagina_cima)
        self.bind_all('<Page_Down>', self._pagina_baixo)
    
    def _handle_f1(self, event):
        """Handler inteligente para F1."""
        if self.modo_pagamento:
            self.processar_pagamento("dinheiro")
        else:
            self.buscar_produto()
        return "break"
    
    def _handle_f2(self, event):
        """Handler inteligente para F2."""
        if self.modo_pagamento:
            self.processar_pagamento("debito")
        else:
            self.adicionar_produto_por_codigo()
        return "break"
    
    def _handle_f3(self, event):
        """Handler inteligente para F3."""
        if self.modo_pagamento:
            self.processar_pagamento("credito")
        return "break"
    
    def _handle_f4(self, event):
        """Handler inteligente para F4 - PIX Mercado Pago direto."""
        # F4 sempre vai para PIX, seja na venda ou no pagamento
        venda = self.venda_service.get_venda_atual()
        if venda and venda.itens:
            if not self.modo_pagamento:
                # Se não está no modo pagamento, vai direto para PIX Mercado Pago
                self.finalizar_venda_direto_pix()
            else:
                # Se já está no pagamento, processa PIX Mercado Pago
                self.processar_pagamento("pix")
        return "break"
    
    def _handle_f5(self, event):
        """Handler inteligente para F5."""
        if not self.modo_pagamento:
            self.remover_item_selecionado()
        return "break"
    
    def _handle_f6(self, event):
        """Handler inteligente para F6."""
        if not self.modo_pagamento:
            self.cancelar_venda()
        return "break"
    
    def _handle_f7(self, event):
        """Handler inteligente para F7."""
        if not self.modo_pagamento:
            self.editar_quantidade_com_admin()
        return "break"
    
    def _handle_f8(self, event):
        """Handler inteligente para F8."""
        if not self.modo_pagamento:
            self.cancelar_item_com_admin()
        return "break"
    
    def _handle_f9(self, event):
        """Handler inteligente para F9."""
        if self.modo_pagamento:
            self.cancelar_venda()
        else:
            self.callback_fechar_caixa()
        return "break"
    
    def _handle_f10(self, event):
        """Handler inteligente para F10."""
        if not self.modo_pagamento:
            self.finalizar_venda()
        return "break"
    
    def _handle_escape(self, event):
        """Handler inteligente para Escape."""
        # Se a busca está aberta, fecha a busca
        if hasattr(self, 'painel_busca') and self.painel_busca.winfo_ismapped():
            self.painel_busca.ocultar()
            self.frame_venda.pack(fill=tk.BOTH, expand=True)
            self.entry_codigo.entry.focus_set()
            return "break"
        
        # Se está em modo pagamento, volta para venda
        if self.modo_pagamento:
            self.voltar_para_venda()
        else:
            # Modo venda normal - limpa campo de código
            self.limpar_campo_codigo()
        return "break"
    
    def criar_widgets(self):
        """Cria interface."""
        self.main_frame = tk.Frame(self, bg=ModernStyles.BG_MAIN)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de atalhos
        self.criar_barra_atalhos(self.main_frame)
        
        # Info operador - MODERNA
        info = tk.Frame(self.main_frame, bg=ModernStyles.BG_DARK, height=42)  # Aumentado de 40 para 42
        info.pack(fill=tk.X)
        info.pack_propagate(False)
        
        info_content = tk.Frame(info, bg=ModernStyles.BG_DARK)
        info_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)  # Aumentado padding vertical
        
        tk.Label(
            info_content,
            text=f"👤 {self.usuario.nome_completo}",
            font=(ModernStyles.FONT_FAMILY, 10, "bold"),  # Tamanho fixo menor
            fg=ModernStyles.TEXT_WHITE,
            bg=ModernStyles.BG_DARK
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_content,
            text=f"💵 Caixa #{self.caixa.id}",
            font=(ModernStyles.FONT_FAMILY, 10, "bold"),  # Tamanho fixo menor
            fg=ModernStyles.SUCCESS_LIGHT,
            bg=ModernStyles.BG_DARK
        ).pack(side=tk.RIGHT)
        
        # Área principal (esquerda e direita)
        corpo = tk.Frame(self.main_frame, bg=ModernStyles.BG_MAIN)
        corpo.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Reduzido padding
        
        # Painel esquerdo (campo código + lista)
        self.painel_esquerdo = tk.Frame(corpo, bg=ModernStyles.BG_MAIN)
        self.painel_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))  # Adicionado padx
        self._montar_area_venda_esquerda()
        
        # Container para painel direito (totais / pagamento)
        self.painel_direito_container = tk.Frame(corpo, bg=ModernStyles.BG_MAIN)
        self.painel_direito_container.pack(side=tk.RIGHT, fill=tk.Y)  # Removido padx extra
        self.criar_painel_direito()
        
        # Estado da tela
        self.modo_pagamento = False

    def _montar_area_venda_esquerda(self):
        """Monta components principais da área de venda."""
        # Container para alternar entre venda e busca
        self.container_esquerdo = tk.Frame(self.painel_esquerdo, bg="#ecf0f1")
        self.container_esquerdo.pack(fill=tk.BOTH, expand=True)
        
        # Frame de venda (padrão)
        self.frame_venda = tk.Frame(self.container_esquerdo, bg="#ecf0f1")
        self.frame_venda.pack(fill=tk.BOTH, expand=True)
        
        self.criar_campo_entrada(self.frame_venda)
        self.criar_lista_produtos(self.frame_venda)
        
        # Painel de busca (inline, oculto inicialmente)
        from src.ui.caixa.busca_produto_panel import BuscaProdutoPanel
        self.painel_busca = BuscaProdutoPanel(
            self.container_esquerdo,
            callback=self.adicionar_produto_busca_inline
        )
        # Não mostra inicialmente (pack_forget já é o padrão)

    def _limpar_atalhos_principais(self):
        """Remove bindings globais para evitar duplicidade."""
        # Lista de todas as teclas de função e atalhos
        atalhos = [
            '<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>', '<F7>', '<F8>', '<F9>', '<F10>',
            '<Delete>', '<Escape>', '<Tab>', '<Shift-Tab>',
            '<Up>', '<Down>', '<Home>', '<End>', '<Page_Up>', '<Page_Down>',
            '<Control-n>', '<Control-f>', '<Control-d>', '<Control-Return>', '<Return>'
        ]
        
        # Unbind em todos os widgets
        for atalho in atalhos:
            try:
                self.unbind_all(atalho)
            except:
                pass
        
        # Garante que não há bindings duplicados
        self._atalhos_ativos = []
    
    def criar_barra_atalhos(self, parent):
        """Barra com atalhos principais do sistema - MODERNA."""
        barra = tk.Frame(parent, bg=ModernStyles.PRIMARY_DARK, height=55)  # Aumentado de 50 para 55
        barra.pack(fill=tk.X)
        barra.pack_propagate(False)
        
        # Container interno com padding
        container = tk.Frame(barra, bg=ModernStyles.PRIMARY_DARK)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)  # Ajustado padding vertical
        
        atalhos = [
            ("F1", "Buscar", ModernStyles.INFO),
            ("F2", "Código", ModernStyles.SUCCESS),
            ("F5", "Remover", ModernStyles.WARNING),
            ("F6", "Cancelar", ModernStyles.DANGER),
            ("F10", "FINALIZAR", ModernStyles.SUCCESS_DARK),
        ]
        
        for tecla, texto, cor in atalhos:
            # Frame do atalho
            frame_atalho = tk.Frame(container, bg=ModernStyles.PRIMARY_DARK)
            frame_atalho.pack(side=tk.LEFT, padx=8)  # Aumentado para 8
            
            # Tecla com destaque
            btn_tecla = tk.Label(
                frame_atalho,
                text=tecla,
                font=(ModernStyles.FONT_FAMILY, 9, "bold"),
                bg=cor,
                fg=ModernStyles.TEXT_WHITE,
                padx=10,
                pady=4,  # Reduzido para 4
                relief="flat",
                borderwidth=0
            )
            btn_tecla.pack()
            
            # Descrição
            tk.Label(
                frame_atalho,
                text=texto,
                font=(ModernStyles.FONT_FAMILY, 8),
                bg=ModernStyles.PRIMARY_DARK,
                fg=ModernStyles.TEXT_WHITE
            ).pack(pady=(2, 0))  # Aumentado para 2
    
    def criar_campo_entrada(self, parent):
        """Campo GRANDE para código - MODERNO."""
        # Card moderno
        card = ModernStyles.create_card(parent)
        card.pack(fill=tk.X, padx=8, pady=(5, 8))  # Reduzido padding superior
        
        content = card.content
        
        # Cabeçalho
        header = tk.Frame(content, bg=ModernStyles.WHITE)
        header.pack(fill=tk.X, pady=(0, 8))  # Reduzido de 12 para 8
        
        tk.Label(
            header,
            text="🔍 LEIA O CÓDIGO DE BARRAS OU DIGITE O CÓDIGO",
            font=(ModernStyles.FONT_FAMILY, 11, "bold"),  # Tamanho fixo menor
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY
        ).pack(side=tk.LEFT)
        
        # Label de quantidade (lado direito)
        self.label_quantidade = tk.Label(
            header,
            text="",
            font=(ModernStyles.FONT_FAMILY, 13, "bold"),  # Tamanho fixo menor
            bg=ModernStyles.WHITE,
            fg=ModernStyles.SUCCESS
        )
        self.label_quantidade.pack(side=tk.RIGHT, padx=8)  # Reduzido de 10 para 8
        
        # Campo de entrada MODERNO
        self.entry_codigo = ModernStyles.create_modern_entry(
            content,
            font_size=24  # Tamanho fixo menor (era XXLARGE = 28)
        )
        self.entry_codigo.pack(fill=tk.X, ipady=10)  # Reduzido de 12 para 10
        
        # Bind eventos ao entry interno
        entry_widget = self.entry_codigo.entry
        entry_widget.bind('<Return>', lambda e: self.adicionar_produto_por_codigo())
        entry_widget.bind('<KeyPress>', self.capturar_quantidade)
        
        # Dica visual
        dica_frame = tk.Frame(content, bg=ModernStyles.WHITE)
        dica_frame.pack(fill=tk.X, pady=(8, 0))  # Reduzido de 10 para 8
        
        tk.Label(
            dica_frame,
            text="💡 ",
            font=(ModernStyles.FONT_FAMILY, 8),  # Tamanho fixo menor
            bg=ModernStyles.WHITE,
            fg=ModernStyles.INFO
        ).pack(side=tk.LEFT)
        
        tk.Label(
            dica_frame,
            text="Digite quantidade antes do código (ex: 3 depois leia) | Use vírgula para peso (1,5)",
            font=(ModernStyles.FONT_FAMILY, 8, "italic"),  # Tamanho fixo menor
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(side=tk.LEFT)
        
        # Label de status para mensagens
        self.label_status = tk.Label(
            content,
            text="✓ Sistema pronto para uso",
            font=(ModernStyles.FONT_FAMILY, 9),  # Tamanho fixo menor
            bg=ModernStyles.WHITE,
            fg=ModernStyles.SUCCESS
        )
        self.label_status.pack(pady=(6, 0))  # Reduzido de 8 para 6
    
    def criar_lista_produtos(self, parent):
        """Lista de produtos - MODERNA."""
        # Card moderno
        card_container = tk.Frame(parent, bg=ModernStyles.GRAY_LIGHT)
        card_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))  # Reduzido padding
        
        card = tk.Frame(card_container, bg=ModernStyles.WHITE)
        card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Cabeçalho
        header = tk.Frame(card, bg=ModernStyles.PRIMARY, height=45)  # Reduzido de 50 para 45
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🛒 ITENS DA VENDA",
            font=(ModernStyles.FONT_FAMILY, ModernStyles.FONT_MEDIUM, "bold"),  # Reduzido de LARGE
            fg=ModernStyles.TEXT_WHITE,
            bg=ModernStyles.PRIMARY
        ).pack(pady=10)  # Reduzido de 12
        
        # Container da árvore
        tree_frame = tk.Frame(card, bg=ModernStyles.WHITE)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar moderna
        scroll = ttk.Scrollbar(tree_frame, style="Modern.Vertical.TScrollbar")
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview com estilo moderno
        self.tree_produtos = ttk.Treeview(
            tree_frame,
            yscrollcommand=scroll.set,
            height=15,
            columns=("item", "codigo", "nome", "qtd", "preco", "subtotal"),
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )
        
        # Configuração das colunas
        self.tree_produtos.heading("item", text="#")
        self.tree_produtos.heading("codigo", text="Código")
        self.tree_produtos.heading("nome", text="Produto")
        self.tree_produtos.heading("qtd", text="Qtd")
        self.tree_produtos.heading("preco", text="Preço Unit.")
        self.tree_produtos.heading("subtotal", text="Subtotal")
        
        self.tree_produtos.column("item", width=50, anchor=tk.CENTER)
        self.tree_produtos.column("codigo", width=120)
        self.tree_produtos.column("nome", width=280)
        self.tree_produtos.column("qtd", width=90, anchor=tk.CENTER)
        self.tree_produtos.column("preco", width=110, anchor=tk.E)
        self.tree_produtos.column("subtotal", width=130, anchor=tk.E)
        
        # Tags para cores alternadas
        self.tree_produtos.tag_configure('oddrow', background=ModernStyles.LIGHT)
        self.tree_produtos.tag_configure('evenrow', background=ModernStyles.WHITE)
        self.tree_produtos.tag_configure('selected', background=ModernStyles.PRIMARY_LIGHT, foreground=ModernStyles.DARK)
        
        scroll.config(command=self.tree_produtos.yview)
        self.tree_produtos.pack(fill=tk.BOTH, expand=True)
        
        # Efeito de foco visual na árvore
        def on_tree_focus_in(e):
            card_container.config(
                highlightthickness=3,
                highlightbackground=ModernStyles.FOCUS_BORDER,
                highlightcolor=ModernStyles.FOCUS_BORDER
            )
        
        def on_tree_focus_out(e):
            card_container.config(
                highlightthickness=0
            )
        
        self.tree_produtos.bind("<FocusIn>", on_tree_focus_in)
        self.tree_produtos.bind("<FocusOut>", on_tree_focus_out)
    
    def criar_painel_direito(self):
        """Display para cliente - MODERNO."""
        # Limpa container
        for widget in self.painel_direito_container.winfo_children():
            widget.destroy()
        
        # Card moderno com sombra
        card_shadow = tk.Frame(
            self.painel_direito_container,
            bg=ModernStyles.GRAY_LIGHT
        )
        card_shadow.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(card_shadow, bg=ModernStyles.WHITE)
        card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        card.configure(width=380)  # Reduzido de 420 para 380
        card.pack_propagate(False)
        
        # Cabeçalho
        header = tk.Frame(card, bg=ModernStyles.SUCCESS, height=50)  # Reduzido de 55 para 50
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="💰 DISPLAY DO CLIENTE",
            font=(ModernStyles.FONT_FAMILY, ModernStyles.FONT_MEDIUM, "bold"),  # Reduzido de LARGE
            fg=ModernStyles.TEXT_WHITE,
            bg=ModernStyles.SUCCESS
        ).pack(pady=12)  # Reduzido de 15
        
        # Área de conteúdo
        content = tk.Frame(card, bg=ModernStyles.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)  # Reduzido padding
        
        # Último item - Card interno
        ultimo_card = tk.Frame(content, bg=ModernStyles.LIGHT, relief="flat", bd=0)
        ultimo_card.pack(fill=tk.X, pady=(0, 12))  # Reduzido de 15
        
        ultimo_content = tk.Frame(ultimo_card, bg=ModernStyles.LIGHT)
        ultimo_content.pack(fill=tk.X, padx=12, pady=12)  # Reduzido de 15
        
        tk.Label(
            ultimo_content,
            text="ÚLTIMO ITEM:",
            font=(ModernStyles.FONT_FAMILY, 9, "bold"),  # Tamanho fixo menor
            bg=ModernStyles.LIGHT,
            fg=ModernStyles.TEXT_SECONDARY
        ).pack(pady=(0, 6))  # Reduzido
        
        self.label_ultimo_produto = tk.Label(
            ultimo_content,
            text="-",
            font=(ModernStyles.FONT_FAMILY, 11, "bold"),  # Tamanho fixo menor
            bg=ModernStyles.LIGHT,
            fg=ModernStyles.TEXT_PRIMARY,
            wraplength=300  # Reduzido de 350
        )
        self.label_ultimo_produto.pack(pady=(0, 6))  # Reduzido
        
        self.label_ultimo_valor = tk.Label(
            ultimo_content,
            text="R$ 0,00",
            font=(ModernStyles.FONT_FAMILY, 22, "bold"),  # Reduzido
            bg=ModernStyles.LIGHT,
            fg=ModernStyles.SUCCESS
        )
        self.label_ultimo_valor.pack(pady=(0, 4))  # Reduzido
        
        # Separador
        tk.Frame(content, bg=ModernStyles.GRAY, height=2).pack(fill=tk.X, pady=10)  # Reduzido
        
        # Totais
        totais = tk.Frame(content, bg=ModernStyles.WHITE)
        totais.pack(fill=tk.X, pady=8)  # Reduzido
        
        self.criar_linha_total(totais, "ITENS:", "label_qtd_itens", "0", ModernStyles.TEXT_SECONDARY, 10)
        self.criar_linha_total(totais, "SUBTOTAL:", "label_subtotal", "R$ 0,00", ModernStyles.TEXT_SECONDARY, 11)
        self.criar_linha_total(totais, "DESCONTO:", "label_desconto", "R$ 0,00", ModernStyles.DANGER, 10)
        
        # Separador destaque
        tk.Frame(totais, bg=ModernStyles.SUCCESS, height=3).pack(fill=tk.X, pady=12)  # Reduzido
        
        # Total a pagar - Destaque
        total_card = tk.Frame(totais, bg=ModernStyles.SUCCESS, relief="flat", bd=0)
        total_card.pack(fill=tk.X, pady=4)  # Reduzido
        
        total_content = tk.Frame(total_card, bg=ModernStyles.SUCCESS)
        total_content.pack(fill=tk.X, padx=12, pady=12)  # Reduzido
        
        tk.Label(
            total_content,
            text="TOTAL A PAGAR",
            font=(ModernStyles.FONT_FAMILY, 12, "bold"),  # Reduzido
            bg=ModernStyles.SUCCESS,
            fg=ModernStyles.TEXT_WHITE
        ).pack(pady=(0, 4))  # Reduzido
        
        self.label_total = tk.Label(
            total_content,
            text="R$ 0,00",
            font=(ModernStyles.FONT_FAMILY, 30, "bold"),  # Reduzido
            bg=ModernStyles.SUCCESS,
            fg=ModernStyles.TEXT_WHITE
        )
        self.label_total.pack(pady=(0, 4))  # Reduzido
        
        # Espaçador fixo menor
        tk.Frame(content, bg=ModernStyles.WHITE, height=8).pack(fill=tk.X)  # Fixo
        
        # Instruções
        instr_card = tk.Frame(content, bg=ModernStyles.LIGHT, relief="flat", bd=0)
        instr_card.pack(fill=tk.X, pady=(0, 8))  # Reduzido
        
        tk.Label(
            instr_card,
            text="⌨️ Pressione F10 para FINALIZAR",
            font=(ModernStyles.FONT_FAMILY, 10, "bold"),  # Tamanho fixo
            bg=ModernStyles.LIGHT,
            fg=ModernStyles.SUCCESS
        ).pack(pady=10)  # Reduzido
    
    def criar_linha_total(self, parent, label, attr, valor, cor, tamanho):
        """Cria linha de total - MODERNA."""
        f = tk.Frame(parent, bg=ModernStyles.WHITE)
        f.pack(fill=tk.X, pady=6)
        
        tk.Label(
            f,
            text=label,
            font=(ModernStyles.FONT_FAMILY, tamanho),
            bg=ModernStyles.WHITE,
            fg=cor
        ).pack(side=tk.LEFT)
        
        lbl = tk.Label(
            f,
            text=valor,
            font=(ModernStyles.FONT_FAMILY, tamanho, "bold"),
            bg=ModernStyles.WHITE,
            fg=ModernStyles.TEXT_PRIMARY if "desconto" not in attr else cor
        )
        lbl.pack(side=tk.RIGHT)
        setattr(self, attr, lbl)
    
    def capturar_quantidade(self, event):
        """Captura dígitos para multiplicador."""
        if event.char.isdigit() or event.char in '.,':
            if self.entry_codigo.entry.get() == "" and event.char.isdigit():
                self.quantidade_digitada += event.char
                self.label_quantidade.config(text=f"Qtd: {self.quantidade_digitada} X")
                return "break"
            elif self.quantidade_digitada and (event.char.isdigit() or event.char in '.,'):
                self.quantidade_digitada += event.char
                self.label_quantidade.config(text=f"Qtd: {self.quantidade_digitada} X")
                return "break"
    
    def adicionar_produto_por_codigo(self):
        """Adiciona produto."""
        codigo = self.entry_codigo.entry.get().strip()
        if not codigo:
            return
        
        try:
            quantidade = Decimal(self.quantidade_digitada.replace(',', '.') if self.quantidade_digitada else '1')
        except:
            messagebox.showerror("Erro", "Quantidade inválida!")
            self.quantidade_digitada = ""
            self.label_quantidade.config(text="")
            return
            
        produto = ProdutoDAO.buscar_por_codigo_barras(codigo)
        
        if not produto:
            produtos = ProdutoDAO.buscar_por_nome(codigo)
            if len(produtos) == 1:
                produto = produtos[0]
            elif len(produtos) > 1:
                self.buscar_produto(codigo)
                self.quantidade_digitada = ""
                self.label_quantidade.config(text="")
                return
        
        if produto:
            sucesso, msg = self.venda_service.adicionar_produto(produto, quantidade)
            if sucesso:
                self.atualizar_lista_produtos()
                self.label_ultimo_produto.config(text=f"{produto.nome}\n{quantidade} x {Formatters.formatar_moeda(produto.preco_venda)}")
                self.label_ultimo_valor.config(text=Formatters.formatar_moeda(quantidade * produto.preco_venda))
                self.entry_codigo.entry.delete(0, tk.END)
                self.quantidade_digitada = ""
                self.label_quantidade.config(text="")
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", f"Produto não encontrado: {codigo}")
    
    def atualizar_lista_produtos(self):
        """Atualiza lista."""
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        venda = self.venda_service.get_venda_atual()
        if venda:
            for idx, item in enumerate(venda.itens, 1):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree_produtos.insert("", tk.END, values=(
                    idx, item.produto_codigo_barras or "", item.produto_nome or "",
                    Formatters.formatar_quantidade(item.quantidade),
                    Formatters.formatar_moeda(item.preco_unitario),
                    Formatters.formatar_moeda(item.subtotal)
                ), tags=(tag,))
        self.atualizar_totais()
    
    def atualizar_totais(self):
        """Atualiza totais."""
        venda = self.venda_service.get_venda_atual()
        if venda:
            self.label_qtd_itens.config(text=str(len(venda.itens)))
            self.label_subtotal.config(text=Formatters.formatar_moeda(venda.subtotal))
            self.label_desconto.config(text=Formatters.formatar_moeda(venda.desconto))
            self.label_total.config(text=Formatters.formatar_moeda(venda.total))
    
    def buscar_produto(self, termo=""):
        """Toggle do painel de busca inline."""
        # Se painel já está visível, oculta
        if self.painel_busca.winfo_ismapped():
            self.painel_busca.ocultar()
            self.frame_venda.pack(fill=tk.BOTH, expand=True)
            self.entry_codigo.entry.focus_set()
        else:
            # Oculta área de venda e mostra painel de busca
            self.frame_venda.pack_forget()
            termo_busca = termo or self.entry_codigo.entry.get()
            self.painel_busca.mostrar(termo_busca)
    
    def adicionar_produto_busca_inline(self, produto):
        """Callback quando produto é selecionado no painel inline."""
        if produto is None:
            # Cancelou a busca - volta para venda
            self.frame_venda.pack(fill=tk.BOTH, expand=True)
            self.entry_codigo.entry.focus_set()
            return
        
        # Adiciona produto
        from decimal import Decimal
        qtd = Decimal("1")
        sucesso, msg = self.venda_service.adicionar_produto(produto, qtd)
        if sucesso:
            self.atualizar_lista_produtos()
            self.label_ultimo_produto.config(text=f"{produto.nome}\n{qtd} x {Formatters.formatar_moeda(produto.preco_venda)}")
            self.label_ultimo_valor.config(text=Formatters.formatar_moeda(qtd * produto.preco_venda))
            self.entry_codigo.entry.delete(0, tk.END)
            self.mostrar_mensagem_temporaria(f"✅ {produto.nome} adicionado", "#27ae60")
        else:
            self.mostrar_mensagem_temporaria(f"❌ {msg}", "#e74c3c")
        
        # Volta para área de venda
        self.frame_venda.pack(fill=tk.BOTH, expand=True)
        self.entry_codigo.entry.focus_set()
    
    def adicionar_produto_busca(self, produto):
        """Método legado - redireciona para inline."""
        self.adicionar_produto_busca_inline(produto)
    
    def solicitar_quantidade(self):
        """F3 - Solicita quantidade inline (sem popup)."""
        # Remove o popup - agora o usuário digita direto antes do código
        # Exemplo: digitar "3" + código de barras = adiciona 3 unidades
        self.mostrar_mensagem_temporaria("💡 Digite a quantidade + código de barras", "#3498db")
        self.entry_codigo.entry.focus()
    
    def solicitar_quantidade_para_produto(self, produto):
        """Adiciona produto com quantidade padrão 1 (sem popup)."""
        from decimal import Decimal
        qtd = Decimal("1")
        sucesso, msg = self.venda_service.adicionar_produto(produto, qtd)
        if sucesso:
            self.atualizar_lista_produtos()
            self.label_ultimo_produto.config(text=f"{produto.nome}\n{qtd} x {Formatters.formatar_moeda(produto.preco_venda)}")
            self.label_ultimo_valor.config(text=Formatters.formatar_moeda(qtd * produto.preco_venda))
            self.entry_codigo.entry.delete(0, tk.END)
            self.entry_codigo.entry.focus()
            self.mostrar_mensagem_temporaria(f"✅ {produto.nome} adicionado", "#27ae60")
        else:
            self.mostrar_mensagem_temporaria(f"❌ {msg}", "#e74c3c")
    
    def remover_item_selecionado(self):
        """F5 - Remove item."""
        sel = self.tree_produtos.selection()
        if not sel:
            itens = self.tree_produtos.get_children()
            if itens:
                self.tree_produtos.selection_set(itens[-1])
                sel = self.tree_produtos.selection()
            else:
                return
        
        idx = self.tree_produtos.index(sel[0])
        sucesso, _ = self.venda_service.remover_item(idx)
        if sucesso:
            self.atualizar_lista_produtos()
        self.entry_codigo.entry.focus()
    
    def aplicar_desconto(self):
        """F4 - Desabilitado (sem popup de desconto)."""
        self.mostrar_mensagem_temporaria("⚠️ Função de desconto desabilitada", "#f39c12")
        self.entry_codigo.entry.focus()
    
    def cancelar_venda(self):
        """F6 - Cancela venda."""
        venda = self.venda_service.get_venda_atual()
        if venda and len(venda.itens) > 0:
            if messagebox.askyesno("Confirmar", "Deseja cancelar a venda atual?"):
                self.venda_service.cancelar_venda()
                self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id)
                self.atualizar_lista_produtos()
                self.label_ultimo_produto.config(text="-")
                self.label_ultimo_valor.config(text="R$ 0,00")
        self.entry_codigo.entry.focus()
    
    def finalizar_venda(self):
        """F10 - Finaliza venda."""
        # Se painel de busca está aberto, fecha
        if self.painel_busca.winfo_ismapped():
            self.painel_busca.ocultar()
            self.frame_venda.pack(fill=tk.BOTH, expand=True)
        
        venda = self.venda_service.get_venda_atual()
        if not venda or len(venda.itens) == 0:
            # Mostrar mensagem na própria tela em vez de popup
            self.mostrar_mensagem_temporaria("⚠️ ADICIONE PRODUTOS À VENDA", "#e74c3c")
            return
        
        # Mostrar área de pagamento integrada em vez de popup
        self.mostrar_area_pagamento()
    
    def callback_venda_finalizada(self):
        """Callback após venda finalizada."""
        self.venda_service.iniciar_nova_venda(self.usuario.id, self.caixa.id)
        self.atualizar_lista_produtos()
        self.label_ultimo_produto.config(text="-")
        self.label_ultimo_valor.config(text="R$ 0,00")
        self.entry_codigo.entry.focus()
    
    def mostrar_area_pagamento(self):
        """Mostra área de pagamento integrada na própria tela."""
        # Esconde o container de venda (mas não destrói)
        self.container_esquerdo.pack_forget()
        
        # Criar área de pagamento no painel esquerdo
        self.criar_area_pagamento_integrada()
        
        # Foco na primeira opção de pagamento
        self.opcoes_pagamento[0].focus_set()
        self.modo_pagamento = True
    
    def finalizar_venda_direto_pix(self):
        """Finaliza venda indo direto para PIX sem mostrar área de pagamento."""
        venda = self.venda_service.get_venda_atual()
        
        # Esconde o container de venda
        self.container_esquerdo.pack_forget()
        
        # Ativa modo pagamento
        self.modo_pagamento = True
        
        # Vai direto para PIX
        self.processar_pix_mercado_pago(venda)
    
    def finalizar_venda_direto_pix_estático(self):
        """Finaliza venda usando PIX estático (gerado localmente)."""
        venda = self.venda_service.get_venda_atual()
        
        # Esconde o container de venda
        self.container_esquerdo.pack_forget()
        
        # Ativa modo pagamento
        self.modo_pagamento = True
        
        # Vai direto para PIX estático
        self.processar_pix_estatico(venda)
    
    def criar_area_pagamento_integrada(self):
        """Cria área de pagamento integrada."""
        # Frame principal do pagamento
        self.frame_pagamento = tk.Frame(self.painel_esquerdo, bg="#ffffff", relief=tk.RAISED, bd=2)  # Reduzido bd
        self.frame_pagamento.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)  # Reduzido padding
        
        # Título
        titulo_frame = tk.Frame(self.frame_pagamento, bg="#27ae60", height=45)  # Reduzido altura
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="💳 FINALIZAR VENDA", font=("Segoe UI", 14, "bold"),  # Reduzido tamanho fonte
                 bg="#27ae60", fg="white").pack(expand=True)
        
        # Valor total
        total_frame = tk.Frame(self.frame_pagamento, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, padx=12, pady=12)  # Reduzido padding
        
        tk.Label(total_frame, text="TOTAL A PAGAR", font=("Segoe UI", 11, "bold"),  # Reduzido
                 bg="#ecf0f1", fg="#2c3e50").pack(pady=(8, 4))  # Reduzido padding
        
        venda = self.venda_service.get_venda_atual()
        tk.Label(total_frame, text=Formatters.formatar_moeda(venda.total), font=("Segoe UI", 22, "bold"),  # Reduzido
                 bg="#ecf0f1", fg="#27ae60").pack(pady=(0, 8))  # Reduzido padding
        
        # Opções de pagamento
        opcoes_frame = tk.Frame(self.frame_pagamento, bg="#ffffff")
        opcoes_frame.pack(fill=tk.X, padx=12, pady=12)  # Reduzido padding
        
        tk.Label(opcoes_frame, text="ESCOLHA A FORMA DE PAGAMENTO:", font=("Segoe UI", 11, "bold"),  # Reduzido
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 10))  # Reduzido padding
        
        # Botões de pagamento
        self.opcoes_pagamento = []
        
        # F1 - Dinheiro
        btn_dinheiro = tk.Button(opcoes_frame, text="F1 - 💵 DINHEIRO", font=("Segoe UI", 12, "bold"),  # Reduzido
                                bg="#27ae60", fg="white", relief=tk.FLAT, pady=12,  # Reduzido
                                command=lambda: self.processar_pagamento("dinheiro"))
        btn_dinheiro.pack(fill=tk.X, pady=4)  # Reduzido
        self.opcoes_pagamento.append(btn_dinheiro)
        
        # F2 - Débito
        btn_debito = tk.Button(opcoes_frame, text="F2 - 💳 CARTÃO DÉBITO", font=("Segoe UI", 12, "bold"),  # Reduzido
                              bg="#3498db", fg="white", relief=tk.FLAT, pady=12,  # Reduzido
                              command=lambda: self.processar_pagamento("debito"))
        btn_debito.pack(fill=tk.X, pady=4)  # Reduzido
        self.opcoes_pagamento.append(btn_debito)
        
        # F3 - Crédito
        btn_credito = tk.Button(opcoes_frame, text="F3 - 💳 CARTÃO CRÉDITO", font=("Segoe UI", 12, "bold"),  # Reduzido
                               bg="#9b59b6", fg="white", relief=tk.FLAT, pady=12,  # Reduzido
                               command=lambda: self.processar_pagamento("credito"))
        btn_credito.pack(fill=tk.X, pady=4)  # Reduzido
        self.opcoes_pagamento.append(btn_credito)
        
        # F4 - PIX
        btn_pix = tk.Button(opcoes_frame, text="F4 - 📱 PIX MERCADO PAGO", font=("Segoe UI", 12, "bold"),  # Reduzido
                           bg="#16a085", fg="white", relief=tk.FLAT, pady=12,  # Reduzido
                           command=lambda: self.processar_pagamento("pix"))
        btn_pix.pack(fill=tk.X, pady=4)  # Reduzido
        self.opcoes_pagamento.append(btn_pix)
        
        # Status do pagamento
        self.status_pagamento = tk.Label(self.frame_pagamento, text="⌨️ Use F1-F4 para escolher | ↑↓ para navegar | ESC para voltar",
                                        font=("Segoe UI", 9), bg="#ffffff", fg="#7f8c8d")  # Reduzido
        self.status_pagamento.pack(pady=8)  # Reduzido
        
        # Botões de ação
        acoes_frame = tk.Frame(self.frame_pagamento, bg="#ffffff")
        acoes_frame.pack(fill=tk.X, padx=12, pady=10)  # Reduzido padding
        
        tk.Button(acoes_frame, text="ESC - VOLTAR", font=("Segoe UI", 11, "bold"),  # Reduzido
                  bg="#95a5a6", fg="white", relief=tk.FLAT, pady=8,  # Reduzido
                  command=self.voltar_para_venda).pack(fill=tk.X, pady=(0, 4))  # Reduzido
        
        tk.Button(acoes_frame, text="F9 - CANCELAR VENDA", font=("Segoe UI", 11, "bold"),  # Reduzido
                  bg="#e74c3c", fg="white", relief=tk.FLAT, pady=8,  # Reduzido
                  command=self.cancelar_venda).pack(fill=tk.X)
        
        # Configurar navegação por teclado
        self.configurar_navegacao_pagamento()
    
    def configurar_navegacao_pagamento(self):
        """Configura navegação por teclado na área de pagamento."""
        # Marca que estamos em modo pagamento
        self.modo_pagamento = True
        
        # Remove os bindings de navegação da lista (que não fazem sentido no pagamento)
        try:
            self.unbind_all('<Up>')
            self.unbind_all('<Down>')
            self.unbind_all('<Return>')
        except:
            pass
        
        # Adiciona navegação específica para pagamento
        self.bind_all('<Up>', self._navegar_pagamento_cima)
        self.bind_all('<Down>', self._navegar_pagamento_baixo)
        self.bind_all('<Return>', self._executar_pagamento_selecionado)
    
    def _navegar_pagamento_cima(self, event):
        """Navega para cima nas opções de pagamento."""
        focused = self.focus_get()
        try:
            index = self.opcoes_pagamento.index(focused)
            if index > 0:
                self.opcoes_pagamento[index - 1].focus_set()
        except (ValueError, AttributeError):
            self.opcoes_pagamento[-1].focus_set()
        return "break"
    
    def _navegar_pagamento_baixo(self, event):
        """Navega para baixo nas opções de pagamento."""
        focused = self.focus_get()
        try:
            index = self.opcoes_pagamento.index(focused)
            if index < len(self.opcoes_pagamento) - 1:
                self.opcoes_pagamento[index + 1].focus_set()
        except (ValueError, AttributeError):
            self.opcoes_pagamento[0].focus_set()
        return "break"
    
    def _executar_pagamento_selecionado(self, event):
        """Executa o pagamento do botão selecionado."""
        focused = self.focus_get()
        if focused in self.opcoes_pagamento:
            focused.invoke()
        return "break"
    
    def mostrar_mensagem_temporaria(self, mensagem, cor="#e74c3c"):
        """Mostra mensagem temporária na tela."""
        # Usar o status label existente para mostrar mensagem
        original_text = self.label_status.cget("text")
        original_bg = self.label_status.cget("bg")
        
        self.label_status.config(text=mensagem, bg=cor, fg="white")
        self.after(3000, lambda: self.label_status.config(text=original_text, bg=original_bg, fg="black"))
    
    def processar_pagamento(self, tipo):
        """Processa pagamento do tipo especificado."""
        venda = self.venda_service.get_venda_atual()
        
        # Valida se existe venda ativa
        if not venda or not venda.itens:
            messagebox.showwarning("Aviso", "Adicione produtos à venda primeiro!")
            return
        
        if tipo == "dinheiro":
            self.processar_dinheiro(venda)
        elif tipo == "debito":
            self.processar_debito(venda)
        elif tipo == "credito":
            self.processar_credito(venda)
        elif tipo == "pix":
            self.processar_pix_mercado_pago(venda)
    
    def processar_dinheiro(self, venda):
        """Processa pagamento em dinheiro com cálculo de troco."""
        # Limpa área de pagamento e mostra interface de troco
        for widget in self.frame_pagamento.winfo_children():
            widget.pack_forget()
        
        # Frame principal do troco
        frame_troco = tk.Frame(self.frame_pagamento, bg="#ffffff")
        frame_troco.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            frame_troco,
            text="💵 PAGAMENTO EM DINHEIRO",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        ).pack(pady=(0, 20))
        
        # Total a pagar
        tk.Label(
            frame_troco,
            text=f"Total: {Formatters.formatar_moeda(venda.total)}",
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(0, 10))
        
        # Entrada de valor pago
        frame_entrada = tk.Frame(frame_troco, bg="#ffffff")
        frame_entrada.pack(pady=10)
        
        tk.Label(
            frame_entrada,
            text="Valor Pago:",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(side="left", padx=(0, 10))
        
        entry_valor_pago = tk.Entry(
            frame_entrada,
            font=("Segoe UI", 14),
            width=15,
            justify="center"
        )
        entry_valor_pago.pack(side="left")
        entry_valor_pago.focus()
        
        # Label de troco
        label_troco = tk.Label(
            frame_troco,
            text="",
            font=("Segoe UI", 20, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        label_troco.pack(pady=20)
        
        # Botões de valores sugeridos
        frame_sugestoes = tk.Frame(frame_troco, bg="#ffffff")
        frame_sugestoes.pack(pady=10)
        
        tk.Label(
            frame_sugestoes,
            text="Valores Sugeridos:",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#7f8c8d"
        ).pack()
        
        frame_botoes_valores = tk.Frame(frame_sugestoes, bg="#ffffff")
        frame_botoes_valores.pack(pady=5)
        
        # Calcula sugestões baseadas no total
        total = float(venda.total)
        sugestoes = []
        for valor in [10, 20, 50, 100, 200]:
            if valor >= total:
                sugestoes.append(valor)
            if len(sugestoes) >= 4:
                break
        
        def aplicar_valor(valor):
            entry_valor_pago.delete(0, tk.END)
            entry_valor_pago.insert(0, f"{valor:.2f}".replace('.', ','))
            calcular_troco()
        
        for valor in sugestoes:
            tk.Button(
                frame_botoes_valores,
                text=f"R$ {valor}",
                font=("Segoe UI", 10),
                bg="#ecf0f1",
                fg="#2c3e50",
                relief="flat",
                padx=15,
                pady=5,
                command=lambda v=valor: aplicar_valor(v)
            ).pack(side="left", padx=5)
        
        # Função para calcular troco
        def calcular_troco(*args):
            try:
                valor_pago = float(entry_valor_pago.get().replace(",", "."))
                troco = valor_pago - total
                
                if troco < 0:
                    label_troco.config(
                        text=f"⚠️ Valor insuficiente! Faltam {Formatters.formatar_moeda(abs(troco))}",
                        fg="#e74c3c"
                    )
                elif troco == 0:
                    label_troco.config(
                        text="✓ Valor exato",
                        fg="#27ae60"
                    )
                else:
                    label_troco.config(
                        text=f"Troco: {Formatters.formatar_moeda(troco)}",
                        fg="#27ae60"
                    )
            except ValueError:
                label_troco.config(text="", fg="#27ae60")
        
        entry_valor_pago.bind("<KeyRelease>", calcular_troco)
        
        # Função para confirmar pagamento
        def confirmar_pagamento():
            try:
                from decimal import Decimal
                from src.models.pagamento import Pagamento
                
                valor_pago = Decimal(entry_valor_pago.get().replace(",", "."))
                
                if valor_pago < venda.total:
                    label_troco.config(
                        text="❌ Valor insuficiente!",
                        fg="#e74c3c"
                    )
                    return
                
                troco = valor_pago - venda.total
                
                pagamento = Pagamento(
                    forma_pagamento=Pagamento.FORMA_DINHEIRO,
                    valor=venda.total,
                    valor_pago=valor_pago,
                    troco=troco,
                    status=Pagamento.STATUS_APROVADO
                )
                
                sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
                
                if sucesso:
                    # Mostra troco antes de finalizar
                    if troco > 0:
                        label_troco.config(
                            text=f"💰 TROCO: {Formatters.formatar_moeda(troco)}",
                            fg="#27ae60",
                            font=("Segoe UI", 24, "bold")
                        )
                        self.after(2000, self.finalizar_venda_com_sucesso)
                    else:
                        self.finalizar_venda_com_sucesso()
                else:
                    label_troco.config(text=f"❌ Erro: {mensagem}", fg="#e74c3c")
            except ValueError:
                label_troco.config(text="❌ Valor inválido!", fg="#e74c3c")
        
        entry_valor_pago.bind("<Return>", lambda e: confirmar_pagamento())
        
        # Botões de ação
        frame_botoes = tk.Frame(frame_troco, bg="#ffffff")
        frame_botoes.pack(pady=20)
        
        tk.Button(
            frame_botoes,
            text="✓ Confirmar (Enter)",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=confirmar_pagamento
        ).pack(side="left", padx=5)
        
        tk.Button(
            frame_botoes,
            text="← Voltar (Esc)",
            font=("Segoe UI", 12),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.voltar_para_venda
        ).pack(side="left", padx=5)
        
        # Atalhos para a tela de troco
        def handle_escape_troco(e):
            self.voltar_para_venda()
            return "break"
        
        # Unbind ESC global temporariamente e bind local
        self.unbind_all('<Escape>')
        frame_troco.bind("<Escape>", handle_escape_troco)
        entry_valor_pago.bind("<Escape>", handle_escape_troco)
    
    def processar_debito(self, venda):
        """Processa pagamento no débito."""
        self.status_pagamento.config(text="💳 Processando cartão de débito...", fg="#3498db")
        
        # Simula processamento
        self.after(2000, lambda: self._finalizar_cartao(venda, "debito"))
    
    def processar_credito(self, venda):
        """Processa pagamento no crédito."""
        self.status_pagamento.config(text="💳 Processando cartão de crédito...", fg="#9b59b6")
        
        # Simula processamento
        self.after(2000, lambda: self._finalizar_cartao(venda, "credito"))
    
    def _finalizar_cartao(self, venda, tipo):
        """Finaliza processamento do cartão."""
        from src.models.pagamento import Pagamento
        
        forma = Pagamento.FORMA_DEBITO if tipo == "debito" else Pagamento.FORMA_CREDITO
        
        pagamento = Pagamento(
            forma_pagamento=forma,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO,
            nsu="123456",
            codigo_autorizacao="789012"
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            self.finalizar_venda_com_sucesso()
        else:
            self.status_pagamento.config(text=f"❌ Erro: {mensagem}", fg="#e74c3c")
    
    def processar_pix_mercado_pago(self, venda):
        """Processa PIX via Mercado Pago."""
        Logger.debug(f"processar_pix_mercado_pago chamado para venda {venda.numero_venda}")
        
        # Mostrar tela de loading
        self.mostrar_loading_pix()
        
        # Timeout de 30 segundos
        self._timeout_pix = self.after(30000, lambda: self._timeout_loading_pix())
        
        # Processar PIX em background
        def processar_async():
            try:
                Logger.debug("Iniciando thread de processamento PIX...")
                from src.services.mercado_pago_service import MercadoPagoService
                from src.ui.caixa.pix_frame import PIXFrame
                
                Logger.debug("Imports realizados")
                
                # Instanciar o serviço Mercado Pago
                Logger.debug("Instanciando MercadoPagoService...")
                mp_service = MercadoPagoService()
                
                # Criar pagamento PIX
                Logger.debug(f"Criando pagamento PIX para valor: R$ {float(venda.total):.2f}")
                Logger.debug("Chamando mp_service.criar_pagamento_pix...")
                
                payment_data = mp_service.criar_pagamento_pix(
                    valor=float(venda.total),
                    descricao=f"Venda PDV #{venda.numero_venda}"
                )
                
                Logger.debug("criar_pagamento_pix RETORNOU!")
                Logger.debug(f"Payment data recebido: {payment_data is not None}")
                if payment_data:
                    Logger.debug(f"Payment ID: {payment_data.get('id', 'N/A')}")
                else:
                    Logger.debug("Payment data é None!")
                
                Logger.debug("Cancelando timeout...")
                # Cancelar timeout
                if hasattr(self, '_timeout_pix'):
                    self.after_cancel(self._timeout_pix)
                
                Logger.debug("Agendando _finalizar_loading_pix...")
                # Voltar para thread principal para atualizar UI
                self.after(0, lambda: self._finalizar_loading_pix(payment_data, venda))
                Logger.debug("_finalizar_loading_pix agendado!")
                
            except Exception as e:
                Logger.error(f"Erro no PIX Mercado Pago: {e}")
                import traceback
                traceback.print_exc()
                
                # Cancelar timeout
                if hasattr(self, '_timeout_pix'):
                    self.after_cancel(self._timeout_pix)
                
                self.after(0, lambda: self._erro_loading_pix(str(e)))
        
        # Executar em thread separada
        import threading
        thread = threading.Thread(target=processar_async, daemon=True)
        thread.start()
        Logger.debug("Thread iniciada")
    
    def mostrar_loading_pix(self):
        """Mostra tela de loading enquanto gera PIX."""
        # Limpar tela atual
        if hasattr(self, 'frame_pagamento') and self.frame_pagamento.winfo_exists():
            for widget in self.frame_pagamento.winfo_children():
                widget.destroy()
            parent = self.frame_pagamento
        else:
            # Se não tem frame de pagamento, criar no painel esquerdo
            for widget in self.painel_esquerdo.winfo_children():
                widget.destroy()
            parent = self.painel_esquerdo
        
        # Frame de loading
        loading_frame = tk.Frame(parent, bg="#ffffff")
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            loading_frame,
            text="📱 GERANDO PIX",
            font=("Segoe UI", 20, "bold"),
            bg="#ffffff",
            fg="#16a085"
        ).pack(pady=(50, 30))
        
        # Mensagem
        tk.Label(
            loading_frame,
            text="Aguarde, estamos gerando seu código PIX...",
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#7f8c8d"
        ).pack(pady=(0, 30))
        
        # Barra de progresso indeterminada
        self.progress_bar = ttk.Progressbar(
            loading_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.start(10)  # Velocidade da animação
        
        # Ícone animado (pontos)
        self.loading_label = tk.Label(
            loading_frame,
            text="●",
            font=("Segoe UI", 24),
            bg="#ffffff",
            fg="#16a085"
        )
        self.loading_label.pack(pady=20)
        
        # Animar pontos
        self._animar_loading(0)
    
    def _animar_loading(self, counter):
        """Anima os pontos de loading."""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            pontos = ["●", "●●", "●●●", "●●●●"]
            self.loading_label.config(text=pontos[counter % 4])
            self.after(300, lambda: self._animar_loading(counter + 1))
    
    def _finalizar_loading_pix(self, payment_data, venda):
        """Finaliza loading e mostra interface PIX."""
        Logger.debug(f"_finalizar_loading_pix chamado. Payment data: {payment_data is not None}")
        
        # Para progress bar
        if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
            self.progress_bar.stop()
        
        if payment_data:
            Logger.debug("Mostrando interface PIX...")
            # Mostrar interface PIX
            self.mostrar_pix_interface(payment_data, venda)
        else:
            Logger.debug("Payment data é None, mostrando erro")
            self.mostrar_mensagem_temporaria("❌ Erro ao gerar PIX", "#e74c3c")
            self.voltar_para_venda()
    
    def _erro_loading_pix(self, erro):
        """Mostra erro do loading."""
        Logger.debug(f"_erro_loading_pix chamado: {erro}")
        # Para progress bar
        if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
            self.progress_bar.stop()
        
        self.mostrar_mensagem_temporaria(f"❌ Erro PIX: {erro}", "#e74c3c")
        self.voltar_para_venda()
    
    def _timeout_loading_pix(self):
        """Timeout do loading PIX."""
        Logger.debug("Timeout do PIX - 30 segundos")
        # Para progress bar
        if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
            self.progress_bar.stop()
        
        self.mostrar_mensagem_temporaria("⏱️ Tempo esgotado ao gerar PIX. Tente novamente.", "#e74c3c")
        self.voltar_para_venda()
    

    def mostrar_pix_interface(self, payment_data, venda):
        """Mostra interface PIX integrada."""
        # Ocultar frame de pagamento
        if hasattr(self, 'frame_pagamento'):
            self.frame_pagamento.pack_forget()
        
        # Criar frame PIX
        try:
            from src.ui.caixa.pix_frame import PIXFrame
            
            self.pix_frame = PIXFrame(
                parent=self.painel_esquerdo,
                payment_data=payment_data,
                callback_aprovado=lambda: self.pix_aprovado(venda),
                callback_cancelado=self.voltar_para_venda
            )
            self.pix_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Erro ao criar PIX frame: {e}")
            import traceback
            traceback.print_exc()
            self.voltar_para_venda()
    
    def processar_pix_estatico(self, venda):
        """Processa PIX estático (gerado localmente)."""
        try:
            from src.services.pix_service import PixService
            from src.ui.caixa.pix_window import PIXWindow
            
            self.status_pagamento.config(text="📱 Gerando PIX estático...", fg="#16a085")
            
            # Gerar PIX estático
            pix_service = PixService()
            pix_data = pix_service.gerar_pix_estatico(
                valor=float(venda.total),
                descricao=f"Venda PDV #{venda.numero_venda}"
            )
            
            if pix_data:
                # Mostrar interface PIX estático
                self.mostrar_pix_estatico_interface(pix_data, venda)
            else:
                if hasattr(self, 'status_pagamento'):
                    self.status_pagamento.config(text="❌ Erro ao gerar PIX", fg="#e74c3c")
                else:
                    self.mostrar_mensagem_temporaria("❌ Erro ao gerar PIX", "#e74c3c")
                self.voltar_para_venda()
                
        except Exception as e:
            if hasattr(self, 'status_pagamento'):
                self.status_pagamento.config(text=f"❌ Erro PIX: {str(e)}", fg="#e74c3c")
            else:
                self.mostrar_mensagem_temporaria(f"❌ Erro PIX: {str(e)}", "#e74c3c")
            print(f"Erro no PIX estático: {e}")
            import traceback
            traceback.print_exc()
            self.voltar_para_venda()

    def mostrar_pix_estatico_interface(self, pix_data, venda):
        """Mostra interface PIX estático."""
        # Limpa área de pagamento
        for widget in self.frame_pagamento.winfo_children():
            widget.pack_forget()
        
        # Frame principal do PIX
        frame_pix = tk.Frame(self.frame_pagamento, bg="#ffffff")
        frame_pix.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            frame_pix,
            text="📱 PIX ESTÁTICO",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg="#8e44ad"
        ).pack(pady=(0, 20))
        
        # Total
        tk.Label(
            frame_pix,
            text=f"Valor: {Formatters.formatar_moeda(venda.total)}",
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(0, 20))
        
        # QR Code (representação textual)
        qr_frame = tk.Frame(frame_pix, bg="#f8f9fa", relief=tk.RAISED, bd=2)
        qr_frame.pack(fill="x", pady=10)
        
        tk.Label(
            qr_frame,
            text="QR CODE PIX",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(pady=10)
        
        # Código PIX Copia e Cola
        pix_code_frame = tk.Frame(frame_pix, bg="#ffffff")
        pix_code_frame.pack(fill="x", pady=10)
        
        tk.Label(
            pix_code_frame,
            text="PIX Copia e Cola:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        # Entry com código PIX
        pix_entry = tk.Text(
            pix_code_frame,
            height=4,
            font=("Courier", 9),
            wrap=tk.WORD,
            bg="#f8f9fa"
        )
        pix_entry.pack(fill="x", pady=5)
        pix_entry.insert("1.0", pix_data.get("qr_code", "Erro ao gerar código PIX"))
        pix_entry.config(state="readonly")
        
        # Botões
        btn_frame = tk.Frame(frame_pix, bg="#ffffff")
        btn_frame.pack(fill="x", pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Confirmar Pagamento",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=lambda: self.confirmar_pix_estatico(venda)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Cancelar",
            font=("Segoe UI", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.voltar_para_venda
        ).pack(side=tk.RIGHT, padx=5)

    def confirmar_pix_estatico(self, venda):
        """Confirma pagamento PIX estático."""
        from src.models.pagamento import Pagamento
        
        pagamento = Pagamento(
            forma_pagamento=Pagamento.FORMA_PIX,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            messagebox.showinfo("Sucesso", "Venda finalizada com PIX!")
            self.callback_venda_finalizada()
        else:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {mensagem}")

    def pix_aprovado(self, venda):
        """Callback quando PIX é aprovado."""
        from src.models.pagamento import Pagamento
        
        pagamento = Pagamento(
            forma_pagamento=Pagamento.FORMA_PIX,
            valor=venda.total,
            status=Pagamento.STATUS_APROVADO
        )
        
        sucesso, mensagem, venda_id = self.venda_service.finalizar_venda([pagamento])
        
        if sucesso:
            self.finalizar_venda_com_sucesso()
        else:
            self.mostrar_mensagem_temporaria(f"Erro: {mensagem}", "#e74c3c")
    
    def finalizar_venda_com_sucesso(self):
        """Finaliza venda com sucesso e pergunta sobre cupom."""
        # Limpar área de pagamento
        for widget in self.painel_esquerdo.winfo_children():
            widget.destroy()
        
        # Mostrar pergunta sobre cupom (com timeout automático)
        self.mostrar_pergunta_cupom()
        self.modo_pagamento = False
        
        # Auto-avançar para nova venda após 5 segundos se não escolher
        self._timeout_cupom = self.after(5000, self.nova_venda)
    
    def mostrar_pergunta_cupom(self):
        """Mostra pergunta sobre imprimir cupom não fiscal."""
        # Limpa bindings antigos
        self._limpar_atalhos_principais()
        
        frame_cupom = tk.Frame(self.painel_esquerdo, bg="#ffffff", relief=tk.RAISED, bd=3)
        frame_cupom.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_frame = tk.Frame(frame_cupom, bg="#27ae60", height=50)
        titulo_frame.pack(fill=tk.X)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="✅ VENDA FINALIZADA!", font=("Arial", 16, "bold"),
                 bg="#27ae60", fg="white").pack(expand=True)
        
        # Conteúdo
        content_frame = tk.Frame(frame_cupom, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(content_frame, text="🎉 Venda realizada com sucesso!", font=("Arial", 16, "bold"),
                 bg="#ffffff", fg="#27ae60").pack(pady=(0, 20))
        
        tk.Label(content_frame, text="Deseja imprimir cupom não fiscal?", font=("Arial", 14),
                 bg="#ffffff", fg="#2c3e50").pack(pady=(0, 30))
        
        # Botões
        botoes_frame = tk.Frame(content_frame, bg="#ffffff")
        botoes_frame.pack(fill=tk.X)
        
        btn_sim = tk.Button(botoes_frame, text="ENTER - SIM", font=("Arial", 14, "bold"),
                           bg="#27ae60", fg="white", relief=tk.FLAT, pady=15,
                           command=self.imprimir_cupom)
        btn_sim.pack(fill=tk.X, pady=(0, 10))
        
        btn_nao = tk.Button(botoes_frame, text="ESC - NÃO", font=("Arial", 14, "bold"),
                           bg="#95a5a6", fg="white", relief=tk.FLAT, pady=15,
                           command=self.nova_venda)
        btn_nao.pack(fill=tk.X)
        
        # Status e countdown
        status_text = tk.Label(content_frame, text="⌨️ ENTER = Imprimir | ESC = Próxima venda", font=("Arial", 10),
                 bg="#ffffff", fg="#7f8c8d")
        status_text.pack(pady=(10, 0))
        
        self.label_timeout = tk.Label(content_frame, text="⏱️ Próxima venda automática em 5 segundos...", 
                                      font=("Arial", 9), bg="#ffffff", fg="#95a5a6")
        self.label_timeout.pack(pady=(5, 0))
        
        # Inicia contagem regressiva
        self._contador_timeout = 5
        self._atualizar_countdown()
        
        # Configurar navegação - handlers específicos para esta tela
        def handle_enter(e):
            self.imprimir_cupom()
            return "break"
        
        def handle_escape(e):
            self.nova_venda()
            return "break"
        
        self.bind_all('<Return>', handle_enter)
        self.bind_all('<Escape>', handle_escape)
        
        # Auto-foco no primeiro botão
        btn_sim.focus_set()
    
    def _atualizar_countdown(self):
        """Atualiza contador regressivo visual."""
        if hasattr(self, 'label_timeout') and self.label_timeout.winfo_exists():
            if self._contador_timeout > 0:
                self.label_timeout.config(text=f"⏱️ Próxima venda automática em {self._contador_timeout} segundos...")
                self._contador_timeout -= 1
                self.after(1000, self._atualizar_countdown)
            else:
                self.label_timeout.config(text="⏱️ Iniciando nova venda...")
    
    def imprimir_cupom(self):
        """Simula impressão do cupom não fiscal."""
        # Cancela timeout automático
        if hasattr(self, '_timeout_cupom'):
            self.after_cancel(self._timeout_cupom)
        
        self.mostrar_mensagem_temporaria("🖨️ Cupom impresso!", "#27ae60")
        self.after(2000, self.nova_venda)
    
    def nova_venda(self):
        """Inicia nova venda."""
        # Cancela timeout automático se existir
        if hasattr(self, '_timeout_cupom'):
            self.after_cancel(self._timeout_cupom)
        
        # Primeiro volta para venda (isso já reconfigura os atalhos)
        self.voltar_para_venda()
        # Depois executa o callback que reinicia os dados da venda
        self.callback_venda_finalizada()
    
    def voltar_para_venda(self):
        """Volta para a tela de venda."""
        # Destruir frames de pagamento ou PIX se existirem
        if hasattr(self, 'frame_pagamento'):
            try:
                if self.frame_pagamento.winfo_exists():
                    self.frame_pagamento.destroy()
            except:
                pass
        
        if hasattr(self, 'pix_frame'):
            try:
                if self.pix_frame.winfo_exists():
                    self.pix_frame.destroy()
            except:
                pass
        
        # Limpar qualquer widget filho do painel esquerdo que não seja o container
        for widget in self.painel_esquerdo.winfo_children():
            if widget != self.container_esquerdo:
                try:
                    widget.destroy()
                except:
                    pass
        
        # Mostrar container de venda novamente
        self.container_esquerdo.pack(fill=tk.BOTH, expand=True)
        
        # Garantir que o frame de venda está visível
        if hasattr(self, 'painel_busca') and self.painel_busca.winfo_ismapped():
            self.painel_busca.ocultar()
        
        if hasattr(self, 'frame_venda'):
            self.frame_venda.pack(fill=tk.BOTH, expand=True)
        
        # Restaurar modo venda (importante!)
        self.modo_pagamento = False
        
        # Reconfigurar TODOS os atalhos de teclado para modo venda
        self.configurar_atalhos()
        
        # Atualizar e focar
        self.atualizar_lista_produtos()
        
        if hasattr(self, 'entry_codigo'):
            try:
                self.entry_codigo.entry.focus_set()
            except:
                pass
    
    # ==================== MÉTODOS DE NAVEGAÇÃO ====================
    
    def limpar_campo_codigo(self):
        """Limpa o campo de código e volta foco para ele."""
        self.entry_codigo.entry.delete(0, tk.END)
        self.quantidade_digitada = ""
        self.label_quantidade.config(text="")
        self.entry_codigo.entry.focus()
        return 'break'
    
    def _navegar_proximo(self, event=None):
        """Navega para o próximo widget focalizável."""
        if event:
            # Se estiver no campo de código, vai para a lista
            if event.widget == self.entry_codigo:
                self._focar_lista_produtos()
            else:
                event.widget.tk_focusNext().focus()
            return 'break'
    
    def _navegar_anterior(self, event=None):
        """Navega para o widget anterior."""
        if event:
            # Se estiver na lista, volta para o campo de código
            if event.widget == self.tree_produtos:
                self.entry_codigo.entry.focus()
            else:
                event.widget.tk_focusPrev().focus()
            return 'break'
    
    def _focar_lista_produtos(self):
        """Foca na lista de produtos."""
        self.tree_produtos.focus()
        # Se não há seleção, seleciona o primeiro item
        if not self.tree_produtos.selection():
            items = self.tree_produtos.get_children()
            if items:
                self.tree_produtos.selection_set(items[0])
                self.tree_produtos.focus(items[0])
    
    def _navegar_lista_cima(self, event=None):
        """Navega para cima na lista de produtos."""
        # Só funciona se o foco estiver na lista ou campo de código
        if hasattr(event, 'widget') and event.widget not in [self.tree_produtos, self.entry_codigo]:
            return
        
        if not self.tree_produtos.focus():
            self._focar_lista_produtos()
            return 'break'
        
        # Se há seleção, move para cima
        current = self.tree_produtos.focus()
        if current:
            prev_item = self.tree_produtos.prev(current)
            if prev_item:
                self.tree_produtos.selection_set(prev_item)
                self.tree_produtos.focus(prev_item)
                self.tree_produtos.see(prev_item)
        return 'break'
    
    def _navegar_lista_baixo(self, event=None):
        """Navega para baixo na lista de produtos."""
        # Só funciona se o foco estiver na lista ou campo de código
        if hasattr(event, 'widget') and event.widget not in [self.tree_produtos, self.entry_codigo]:
            return
        
        if not self.tree_produtos.focus():
            self._focar_lista_produtos()
            return 'break'
        
        # Se há seleção, move para baixo
        current = self.tree_produtos.focus()
        if current:
            next_item = self.tree_produtos.next(current)
            if next_item:
                self.tree_produtos.selection_set(next_item)
                self.tree_produtos.focus(next_item)
                self.tree_produtos.see(next_item)
        return 'break'
    
    def _ir_primeiro_item(self, event=None):
        """Vai para o primeiro item da lista."""
        items = self.tree_produtos.get_children()
        if items:
            self.tree_produtos.selection_set(items[0])
            self.tree_produtos.focus(items[0])
            self.tree_produtos.see(items[0])
        return 'break'
    
    def _ir_ultimo_item(self, event=None):
        """Vai para o último item da lista."""
        items = self.tree_produtos.get_children()
        if items:
            last_item = items[-1]
            self.tree_produtos.selection_set(last_item)
            self.tree_produtos.focus(last_item)
            self.tree_produtos.see(last_item)
        return 'break'
    
    def _pagina_cima(self, event=None):
        """Navega uma página para cima."""
        items = self.tree_produtos.get_children()
        if not items:
            return 'break'
        
        current = self.tree_produtos.focus()
        if current:
            current_index = items.index(current)
            # Move 10 itens para cima (ou vai para o primeiro)
            new_index = max(0, current_index - 10)
            new_item = items[new_index]
            self.tree_produtos.selection_set(new_item)
            self.tree_produtos.focus(new_item)
            self.tree_produtos.see(new_item)
        return 'break'
    
    def _pagina_baixo(self, event=None):
        """Navega uma página para baixo."""
        items = self.tree_produtos.get_children()
        if not items:
            return 'break'
        
        current = self.tree_produtos.focus()
        if current:
            current_index = items.index(current)
            # Move 10 itens para baixo (ou vai para o último)
            new_index = min(len(items) - 1, current_index + 10)
            new_item = items[new_index]
            self.tree_produtos.selection_set(new_item)
            self.tree_produtos.focus(new_item)
            self.tree_produtos.see(new_item)
        return 'break'
