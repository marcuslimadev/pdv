"""
Janela principal do administrador.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from src.models.usuario import Usuario
from src.services.auth_service import auth_service
from src.dao.venda_dao import VendaDAO
from src.dao.produto_dao import ProdutoDAO
from src.utils.formatters import Formatters


class MainAdmin:
    """Interface principal do administrador."""
    
    def __init__(self, master, usuario: Usuario):
        self.master = master
        self.usuario = usuario
        
        # Cria janela principal
        self.window = tk.Toplevel(master)
        self.window.title(f"Sistema PDV - Administrador - {usuario.nome_completo}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')  # Maximiza a janela
        
        # Configuração de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Criar interface
        self.criar_widgets()
        
        # Configurar navegação por teclado
        self.configurar_navegacao_teclado()
        
        # Carrega dashboard inicial
        self.mostrar_dashboard()
    
    def criar_widgets(self):
        """Cria os widgets da interface."""
        # Container principal
        container = ttk.Frame(self.window)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Menu lateral
        self.criar_menu_lateral(container)
        
        # Área de trabalho
        self.area_trabalho = ttk.Frame(container, relief=tk.FLAT)
        self.area_trabalho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista para navegação pelos botões do menu
        self.botoes_menu = []
    
    def criar_menu_lateral(self, parent):
        """Cria o menu lateral."""
        menu_frame = tk.Frame(parent, bg="#2c3e50", width=250)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        menu_frame.pack_propagate(False)
        
        # Cabeçalho
        header_frame = tk.Frame(menu_frame, bg="#34495e", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🛒 PDV Admin",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#34495e"
        ).pack(pady=10)
        
        tk.Label(
            header_frame,
            text=self.usuario.nome_completo,
            font=("Arial", 10),
            fg="#ecf0f1",
            bg="#34495e"
        ).pack()
        
        # Separador
        tk.Frame(menu_frame, bg="#1a252f", height=2).pack(fill=tk.X, pady=5)
        
        # Botões do menu
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "📊 Dashboard", self.mostrar_dashboard))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "📦 Produtos", self.mostrar_produtos))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "🏷️ Categorias", self.mostrar_categorias))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "📦 Estoque", self.mostrar_estoque))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "👥 Usuários", self.mostrar_usuarios))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "📈 Relatórios", self.mostrar_relatorios))
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "⚙️ Configurações", self.mostrar_configuracoes))
        
        # Botão sair no final
        tk.Frame(menu_frame, bg="#2c3e50").pack(fill=tk.BOTH, expand=True)
        
        self.botoes_menu.append(self.criar_botao_menu(menu_frame, "🚪 Sair", self.sair, bg="#c0392b"))
        
        # Configurar navegação dos botões
        self.botao_ativo = 0
        self.destacar_botao_ativo()
    
    def criar_botao_menu(self, parent, texto, comando, bg="#34495e"):
        """Cria um botão no menu lateral."""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Arial", 11),
            fg="white",
            bg=bg,
            activebackground="#4a5f7f",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            anchor=tk.W,
            padx=20,
            pady=15,
            command=comando
        )
        btn.pack(fill=tk.X)
        
        # Efeito hover
        btn.bind("<Enter>", lambda e: btn.config(bg="#4a5f7f"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn
    
    def limpar_area_trabalho(self):
        """Limpa a área de trabalho."""
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Mostra o dashboard."""
        self.limpar_area_trabalho()
        
        # Título
        tk.Label(
            self.area_trabalho,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Frame de cards
        cards_frame = ttk.Frame(self.area_trabalho)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Busca dados
        total_vendas_hoje = VendaDAO.obter_total_vendas_dia()
        produtos_estoque_baixo = ProdutoDAO.buscar_estoque_baixo()
        
        # Cards
        self.criar_card_info(
            cards_frame,
            "💰 Vendas Hoje",
            Formatters.formatar_moeda(total_vendas_hoje),
            "#27ae60",
            0, 0
        )
        
        self.criar_card_info(
            cards_frame,
            "⚠️ Estoque Baixo",
            str(len(produtos_estoque_baixo)),
            "#e74c3c",
            0, 1
        )
        
        self.criar_card_info(
            cards_frame,
            "📦 Total Produtos",
            str(len(ProdutoDAO.buscar_todos())),
            "#3498db",
            0, 2
        )
        
        # Produtos com estoque baixo
        if produtos_estoque_baixo:
            tk.Label(
                self.area_trabalho,
                text="Produtos com Estoque Baixo",
                font=("Arial", 16, "bold"),
                fg="#e74c3c"
            ).pack(anchor=tk.W, pady=(20, 10))
            
            # Tabela
            tree_frame = ttk.Frame(self.area_trabalho)
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            tree = ttk.Treeview(
                tree_frame,
                columns=("codigo", "nome", "estoque", "minimo"),
                show="headings",
                yscrollcommand=scrollbar.set,
                height=10
            )
            
            tree.heading("codigo", text="Código")
            tree.heading("nome", text="Produto")
            tree.heading("estoque", text="Estoque Atual")
            tree.heading("minimo", text="Estoque Mínimo")
            
            tree.column("codigo", width=120)
            tree.column("nome", width=300)
            tree.column("estoque", width=120)
            tree.column("minimo", width=120)
            
            for produto in produtos_estoque_baixo:
                tree.insert("", tk.END, values=(
                    produto.codigo_barras,
                    produto.nome,
                    produto.estoque_atual,
                    produto.estoque_minimo
                ))
            
            scrollbar.config(command=tree.yview)
            tree.pack(fill=tk.BOTH, expand=True)
    
    def criar_card_info(self, parent, titulo, valor, cor, row, col):
        """Cria um card de informação."""
        card = tk.Frame(parent, bg=cor, relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        parent.columnconfigure(col, weight=1)
        
        tk.Label(
            card,
            text=titulo,
            font=("Arial", 12),
            fg="white",
            bg=cor
        ).pack(pady=(15, 5))
        
        tk.Label(
            card,
            text=valor,
            font=("Arial", 20, "bold"),
            fg="white",
            bg=cor
        ).pack(pady=(0, 15))
    
    def mostrar_produtos(self):
        """Mostra a tela de produtos."""
        self.limpar_area_trabalho()
        from src.ui.admin.produtos_window import ProdutosFrame
        ProdutosFrame(self.area_trabalho).pack(fill=tk.BOTH, expand=True)
    
    def mostrar_categorias(self):
        """Mostra a tela de categorias."""
        self.limpar_area_trabalho()
        from src.ui.admin.categorias_window import CategoriasFrame
        CategoriasFrame(self.area_trabalho).pack(fill=tk.BOTH, expand=True)
    
    def mostrar_estoque(self):
        """Mostra a tela de estoque."""
        self.limpar_area_trabalho()
        from src.ui.admin.estoque_window import EstoqueFrame
        EstoqueFrame(self.area_trabalho).pack(fill=tk.BOTH, expand=True)
    
    def mostrar_usuarios(self):
        """Mostra a tela de usuários."""
        self.limpar_area_trabalho()
        from src.ui.admin.usuarios_window import UsuariosFrame
        UsuariosFrame(self.area_trabalho).pack(fill=tk.BOTH, expand=True)
    
    def mostrar_relatorios(self):
        """Mostra a tela de relatórios."""
        self.limpar_area_trabalho()
        from src.ui.admin.relatorios_window import RelatoriosFrame
        RelatoriosFrame(self.area_trabalho).pack(fill=tk.BOTH, expand=True)
    
    def mostrar_configuracoes(self):
        """Mostra a tela de configurações."""
        self.limpar_area_trabalho()
        tk.Label(
            self.area_trabalho,
            text="⚙️ Configurações",
            font=("Arial", 24, "bold")
        ).pack(pady=50)
        tk.Label(
            self.area_trabalho,
            text="Módulo em desenvolvimento",
            font=("Arial", 14),
            fg="#7f8c8d"
        ).pack()
    
    def sair(self):
        """Sai do sistema."""
        if messagebox.askokcancel("Sair", "Deseja sair do sistema?"):
            auth_service.logout()
            self.window.destroy()
            from src.ui.login_window import LoginWindow
            LoginWindow(self.master)
    
    def configurar_navegacao_teclado(self):
        """Configura navegação por teclado."""
        # Binds globais para navegação no menu
        self.window.bind('<Up>', self._navegar_menu_cima)
        self.window.bind('<Down>', self._navegar_menu_baixo)
        self.window.bind('<Return>', self._executar_botao_ativo)
        self.window.bind('<space>', self._executar_botao_ativo)
        self.window.bind('<Escape>', lambda e: self.sair())
        
        # Atalhos de teclado para cada função
        self.window.bind('<F1>', lambda e: self.mostrar_dashboard())
        self.window.bind('<F2>', lambda e: self.mostrar_produtos())
        self.window.bind('<F3>', lambda e: self.mostrar_categorias())
        self.window.bind('<F4>', lambda e: self.mostrar_estoque())
        self.window.bind('<F5>', lambda e: self.mostrar_usuarios())
        self.window.bind('<F6>', lambda e: self.mostrar_relatorios())
        self.window.bind('<F7>', lambda e: self.mostrar_configuracoes())
        
        # Alt+F4 para sair
        self.window.bind('<Alt-F4>', lambda e: self.sair())
        
        # Foco inicial
        self.window.focus_set()
    
    def _navegar_menu_cima(self, event=None):
        """Navega para cima no menu."""
        self.botao_ativo = (self.botao_ativo - 1) % len(self.botoes_menu)
        self.destacar_botao_ativo()
        return 'break'
    
    def _navegar_menu_baixo(self, event=None):
        """Navega para baixo no menu."""
        self.botao_ativo = (self.botao_ativo + 1) % len(self.botoes_menu)
        self.destacar_botao_ativo()
        return 'break'
    
    def _executar_botao_ativo(self, event=None):
        """Executa o botão ativo."""
        if 0 <= self.botao_ativo < len(self.botoes_menu):
            self.botoes_menu[self.botao_ativo].invoke()
        return 'break'
    
    def destacar_botao_ativo(self):
        """Destaca o botão ativo visualmente."""
        for i, botao in enumerate(self.botoes_menu):
            if i == self.botao_ativo:
                # Botão ativo - destacado
                if i == len(self.botoes_menu) - 1:  # Botão sair
                    botao.config(bg="#e74c3c", relief=tk.RAISED, bd=2)
                else:
                    botao.config(bg="#4a5f7f", relief=tk.RAISED, bd=2)
            else:
                # Botão inativo - normal
                if i == len(self.botoes_menu) - 1:  # Botão sair
                    botao.config(bg="#c0392b", relief=tk.FLAT, bd=0)
                else:
                    botao.config(bg="#34495e", relief=tk.FLAT, bd=0)
    
    def on_closing(self):
        """Trata o fechamento da janela."""
        self.sair()
