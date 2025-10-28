"""
Tela de relatórios.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from decimal import Decimal

from src.dao.venda_dao import VendaDAO
from src.dao.pagamento_dao import PagamentoDAO
from src.dao.produto_dao import ProdutoDAO
from src.config.database import DatabaseConnection
from src.utils.formatters import Formatters


class RelatoriosFrame(ttk.Frame):
    """Frame para relatórios."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.criar_widgets()
    
    def criar_widgets(self):
        """Cria widgets."""
        tk.Label(self, text="📈 Relatórios", font=("Arial", 20, "bold"),
                 fg="#2c3e50").pack(pady=(0, 30))
        
        # Grid de botões
        grid = ttk.Frame(self)
        grid.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        self.criar_botao_relatorio(grid, "📊 Vendas do Dia", "#27ae60",
                                    self.relatorio_vendas_dia, 0, 0)
        
        self.criar_botao_relatorio(grid, "📅 Vendas por Período", "#3498db",
                                    self.relatorio_vendas_periodo, 0, 1)
        
        self.criar_botao_relatorio(grid, "💰 Formas de Pagamento", "#9b59b6",
                                    self.relatorio_formas_pagamento, 1, 0)
        
        self.criar_botao_relatorio(grid, "📦 Produtos Mais Vendidos", "#e67e22",
                                    self.relatorio_produtos_vendidos, 1, 1)
        
        self.criar_botao_relatorio(grid, "⚠️ Estoque Baixo", "#e74c3c",
                                    self.relatorio_estoque_baixo, 2, 0)
        
        for i in range(2):
            grid.columnconfigure(i, weight=1)
        for i in range(3):
            grid.rowconfigure(i, weight=1)
    
    def criar_botao_relatorio(self, parent, texto, cor, comando, row, col):
        """Cria botão de relatório."""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Arial", 14, "bold"),
            bg=cor,
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=40,
            command=comando
        )
        btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
    
    def relatorio_vendas_dia(self):
        """Relatório de vendas do dia."""
        hoje = date.today()
        vendas = VendaDAO.buscar_por_periodo(hoje, hoje, "finalizada")
        total = VendaDAO.obter_total_vendas_dia(hoje)
        
        self.mostrar_relatorio_vendas(f"Vendas do Dia - {Formatters.formatar_data(hoje)}",
                                       vendas, total)
    
    def relatorio_vendas_periodo(self):
        """Relatório de vendas por período."""
        d = tk.Toplevel(self)
        d.title("Período do Relatório")
        d.geometry("350x250")
        d.transient(self)
        d.grab_set()
        
        f = ttk.Frame(d, padding="20")
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(f, text="Selecione o Período", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        tk.Label(f, text="Data Inicial:", font=("Arial", 10)).pack(pady=(0, 5))
        entry_inicio = ttk.Entry(f, font=("Arial", 11))
        entry_inicio.pack(pady=(0, 10))
        entry_inicio.insert(0, (date.today() - timedelta(days=7)).strftime("%d/%m/%Y"))
        
        tk.Label(f, text="Data Final:", font=("Arial", 10)).pack(pady=(0, 5))
        entry_fim = ttk.Entry(f, font=("Arial", 11))
        entry_fim.pack(pady=(0, 20))
        entry_fim.insert(0, date.today().strftime("%d/%m/%Y"))
        
        def gerar():
            try:
                from datetime import datetime
                inicio = datetime.strptime(entry_inicio.get(), "%d/%m/%Y").date()
                fim = datetime.strptime(entry_fim.get(), "%d/%m/%Y").date()
                
                vendas = VendaDAO.buscar_por_periodo(inicio, fim, "finalizada")
                total = sum(v.total for v in vendas)
                
                d.destroy()
                self.mostrar_relatorio_vendas(
                    f"Vendas: {Formatters.formatar_data(inicio)} a {Formatters.formatar_data(fim)}",
                    vendas, total
                )
            except:
                messagebox.showerror("Erro", "Data inválida! Use formato DD/MM/AAAA")
        
        tk.Button(f, text="Gerar Relatório", font=("Arial", 11, "bold"), bg="#3498db",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=gerar).pack()
    
    def mostrar_relatorio_vendas(self, titulo, vendas, total):
        """Mostra relatório de vendas."""
        w = tk.Toplevel(self)
        w.title(titulo)
        w.geometry("900x600")
        
        main = ttk.Frame(w, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text=titulo, font=("Arial", 16, "bold")).pack(pady=(0, 10))
        
        tk.Label(main, text=f"Total de Vendas: {len(vendas)}  |  Valor Total: {Formatters.formatar_moeda(total)}",
                 font=("Arial", 12, "bold"), fg="#27ae60").pack(pady=(0, 15))
        
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
            columns=("numero", "data", "usuario", "total"), show="headings")
        
        tree.heading("numero", text="Número")
        tree.heading("data", text="Data/Hora")
        tree.heading("usuario", text="Operador")
        tree.heading("total", text="Total")
        
        tree.column("numero", width=150)
        tree.column("data", width=180)
        tree.column("usuario", width=200)
        tree.column("total", width=120)
        
        scroll.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
        for v in vendas:
            tree.insert("", tk.END, values=(
                v.numero_venda,
                Formatters.formatar_data_hora(v.data_hora),
                getattr(v, 'usuario_nome', ''),
                Formatters.formatar_moeda(v.total)
            ))
        
        tk.Button(main, text="Fechar", font=("Arial", 11), bg="#95a5a6",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=w.destroy).pack(pady=(15, 0))
    
    def relatorio_formas_pagamento(self):
        """Relatório de formas de pagamento."""
        hoje = date.today()
        totais = PagamentoDAO.obter_total_por_forma_pagamento(hoje)
        
        w = tk.Toplevel(self)
        w.title(f"Formas de Pagamento - {Formatters.formatar_data(hoje)}")
        w.geometry("500x400")
        
        main = ttk.Frame(w, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="💰 Formas de Pagamento", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        for forma, dados in totais.items():
            f = tk.Frame(main, bg="#ecf0f1", relief=tk.RAISED, bd=2)
            f.pack(fill=tk.X, pady=5)
            
            tk.Label(f, text=forma.upper(), font=("Arial", 12, "bold"),
                     bg="#ecf0f1").pack(side=tk.LEFT, padx=20, pady=15)
            
            info = tk.Frame(f, bg="#ecf0f1")
            info.pack(side=tk.RIGHT, padx=20, pady=15)
            
            tk.Label(info, text=f"{dados['quantidade']} transações",
                     font=("Arial", 10), bg="#ecf0f1").pack()
            
            tk.Label(info, text=Formatters.formatar_moeda(dados['total']),
                     font=("Arial", 14, "bold"), fg="#27ae60", bg="#ecf0f1").pack()
        
        total_geral = sum(d['total'] for d in totais.values())
        tk.Label(main, text=f"Total Geral: {Formatters.formatar_moeda(total_geral)}",
                 font=("Arial", 14, "bold"), fg="#27ae60").pack(pady=(20, 0))
        
        tk.Button(main, text="Fechar", font=("Arial", 11), bg="#95a5a6",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=w.destroy).pack(pady=(20, 0))
    
    def relatorio_produtos_vendidos(self):
        """Relatório de produtos mais vendidos."""
        # Busca dados do banco
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT 
                    p.id,
                    p.codigo_barras,
                    p.nome,
                    SUM(iv.quantidade) as total_vendido,
                    SUM(iv.subtotal) as receita_total,
                    COUNT(DISTINCT v.id) as num_vendas
                FROM produtos p
                INNER JOIN itens_venda iv ON p.id = iv.produto_id
                INNER JOIN vendas v ON iv.venda_id = v.id
                WHERE v.cancelada = 0
                GROUP BY p.id
                ORDER BY total_vendido DESC
                LIMIT 50
            """
            cursor.execute(query)
            produtos = cursor.fetchall()
            
            if not produtos:
                messagebox.showinfo("Aviso", "Nenhuma venda registrada ainda.")
                return
            
            # Cria janela
            w = tk.Toplevel(self)
            w.title("Produtos Mais Vendidos")
            w.geometry("900x600")
            
            main = ttk.Frame(w, padding="20")
            main.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(main, text="🏆 Top 50 Produtos Mais Vendidos", 
                     font=("Arial", 16, "bold"), fg="#27ae60").pack(pady=(0, 15))
            
            tk.Label(main, text=f"Total de produtos: {len(produtos)}",
                     font=("Arial", 12)).pack(pady=(0, 15))
            
            # Treeview
            tree_frame = ttk.Frame(main)
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            scroll = ttk.Scrollbar(tree_frame)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
                columns=("pos", "codigo", "nome", "qtd", "vendas", "receita"), 
                show="headings")
            
            tree.heading("pos", text="#")
            tree.heading("codigo", text="Código")
            tree.heading("nome", text="Produto")
            tree.heading("qtd", text="Quantidade")
            tree.heading("vendas", text="N° Vendas")
            tree.heading("receita", text="Receita Total")
            
            tree.column("pos", width=50, anchor=tk.CENTER)
            tree.column("codigo", width=120)
            tree.column("nome", width=350)
            tree.column("qtd", width=100, anchor=tk.CENTER)
            tree.column("vendas", width=100, anchor=tk.CENTER)
            tree.column("receita", width=120, anchor=tk.E)
            
            scroll.config(command=tree.yview)
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Preenche
            for i, p in enumerate(produtos, 1):
                tree.insert("", tk.END, values=(
                    f"{i}º",
                    p['codigo_barras'],
                    p['nome'],
                    f"{p['total_vendido']:.0f}",
                    p['num_vendas'],
                    Formatters.formatar_moeda(Decimal(str(p['receita_total'])))
                ))
            
            # Totais
            total_receita = sum(Decimal(str(p['receita_total'])) for p in produtos)
            tk.Label(main, text=f"Receita Total (Top 50): {Formatters.formatar_moeda(total_receita)}", 
                     font=("Arial", 14, "bold"), fg="#27ae60").pack(pady=(20, 0))
            
            tk.Button(main, text="Fechar", font=("Arial", 11), bg="#95a5a6",
                      fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                      command=w.destroy).pack(pady=(20, 0))
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    def relatorio_estoque_baixo(self):
        """Relatório de estoque baixo."""
        produtos = ProdutoDAO.buscar_estoque_baixo()
        
        w = tk.Toplevel(self)
        w.title("Produtos com Estoque Baixo")
        w.geometry("800x500")
        
        main = ttk.Frame(w, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="⚠️ Produtos com Estoque Baixo", font=("Arial", 16, "bold"),
                 fg="#e74c3c").pack(pady=(0, 15))
        
        tk.Label(main, text=f"Total: {len(produtos)} produtos",
                 font=("Arial", 12)).pack(pady=(0, 15))
        
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=scroll.set,
            columns=("codigo", "nome", "estoque", "minimo"), show="headings")
        
        tree.heading("codigo", text="Código")
        tree.heading("nome", text="Produto")
        tree.heading("estoque", text="Estoque")
        tree.heading("minimo", text="Mínimo")
        
        tree.column("codigo", width=120)
        tree.column("nome", width=400)
        tree.column("estoque", width=100)
        tree.column("minimo", width=100)
        
        scroll.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
        for p in produtos:
            tree.insert("", tk.END, values=(
                p.codigo_barras or "",
                p.nome,
                p.estoque_atual,
                p.estoque_minimo
            ))
        
        tk.Button(main, text="Fechar", font=("Arial", 11), bg="#95a5a6",
                  fg="white", cursor="hand2", relief=tk.FLAT, padx=30, pady=10,
                  command=w.destroy).pack(pady=(15, 0))
