"""
Tela de estorno de vendas (Admin).
Permite estornar vendas finalizadas com autenticação.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from typing import Optional

from src.dao.venda_dao import VendaDAO
from src.dao.estorno_dao import EstornoDAO
from src.services.estorno_service import EstornoService
from src.utils.formatters import Formatters


class EstornoFrame(ttk.Frame):
    """Frame para gestão de estornos."""
    
    def __init__(self, parent, usuario_atual):
        super().__init__(parent)
        self.usuario_atual = usuario_atual
        self.criar_widgets()
        self.carregar_vendas()
    
    def criar_widgets(self):
        """Cria widgets."""
        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header, 
            text="🔄 Estorno de Vendas", 
            font=("Arial", 20, "bold"),
            fg="#e74c3c"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header, 
            text="🔄 Atualizar", 
            font=("Arial", 11),
            bg="#3498db", 
            fg="white", 
            cursor="hand2", 
            relief=tk.FLAT,
            padx=20, 
            pady=8, 
            command=self.carregar_vendas
        ).pack(side=tk.RIGHT)
        
        # Filtros
        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            filtro_frame,
            text="Período:",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botões de período rápido
        tk.Button(
            filtro_frame,
            text="Hoje",
            font=("Arial", 9),
            bg="#ecf0f1",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=lambda: self.filtrar_periodo(0)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            filtro_frame,
            text="Últimos 7 dias",
            font=("Arial", 9),
            bg="#ecf0f1",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=lambda: self.filtrar_periodo(7)
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            filtro_frame,
            text="Últimos 30 dias",
            font=("Arial", 9),
            bg="#ecf0f1",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=lambda: self.filtrar_periodo(30)
        ).pack(side=tk.LEFT, padx=2)
        
        # Tabela de vendas
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame, 
            yscrollcommand=scroll.set,
            columns=("numero", "data", "total", "itens", "status"),
            show="headings"
        )
        
        self.tree.heading("numero", text="Número Venda")
        self.tree.heading("data", text="Data/Hora")
        self.tree.heading("total", text="Total")
        self.tree.heading("itens", text="Itens")
        self.tree.heading("status", text="Status")
        
        self.tree.column("numero", width=150)
        self.tree.column("data", width=180)
        self.tree.column("total", width=120, anchor=tk.E)
        self.tree.column("itens", width=80, anchor=tk.CENTER)
        self.tree.column("status", width=150)
        
        # Tags para cores
        self.tree.tag_configure('finalizada', foreground="#27ae60")
        self.tree.tag_configure('cancelada', foreground="#e74c3c")
        self.tree.tag_configure('estornada', foreground="#95a5a6")
        
        scroll.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<Double-1>', lambda e: self.ver_detalhes())
        
        # Botões de ação
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            btn_frame, 
            text="👁️ Ver Detalhes", 
            font=("Arial", 10),
            bg="#3498db", 
            fg="white", 
            cursor="hand2", 
            relief=tk.FLAT,
            padx=20, 
            pady=8, 
            command=self.ver_detalhes
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame, 
            text="🔄 ESTORNAR VENDA", 
            font=("Arial", 10, "bold"),
            bg="#e74c3c", 
            fg="white", 
            cursor="hand2", 
            relief=tk.FLAT,
            padx=20, 
            pady=8, 
            command=self.iniciar_estorno
        ).pack(side=tk.LEFT)
        
        # Informações
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            info_frame,
            text="⚠️ ATENÇÃO: Estornos revertem o estoque e cancelam a venda permanentemente!",
            font=("Arial", 9),
            fg="#e74c3c",
            bg="#ffe6e6",
            padx=10,
            pady=5
        ).pack(fill=tk.X)
    
    def filtrar_periodo(self, dias: int):
        """Filtra vendas por período."""
        if dias == 0:
            data_inicio = date.today()
            data_fim = date.today()
        else:
            data_fim = date.today()
            data_inicio = data_fim - timedelta(days=dias)
        
        self.carregar_vendas(data_inicio, data_fim)
    
    def carregar_vendas(self, data_inicio: date = None, data_fim: date = None):
        """Carrega vendas finalizadas."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Se não informado, últimos 7 dias
        if data_inicio is None:
            data_fim = date.today()
            data_inicio = data_fim - timedelta(days=7)
        
        vendas = VendaDAO.buscar_por_periodo(data_inicio, data_fim)
        
        # Filtra apenas finalizadas e canceladas
        for venda in vendas:
            if venda.status in ['finalizada', 'cancelada']:
                itens = VendaDAO.buscar_itens_venda(venda.id)
                
                # Verifica se foi estornada
                estornada = EstornoDAO.verificar_venda_estornada(venda.id)
                status_texto = "ESTORNADA" if estornada else venda.status.upper()
                tag = 'estornada' if estornada else venda.status
                
                self.tree.insert("", tk.END, values=(
                    venda.numero_venda,
                    venda.data_hora.strftime("%d/%m/%Y %H:%M") if venda.data_hora else "",
                    Formatters.formatar_moeda(venda.total),
                    len(itens),
                    status_texto
                ), tags=(str(venda.id), tag))
    
    def ver_detalhes(self):
        """Mostra detalhes da venda selecionada."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma venda!")
            return
        
        venda_id = int(self.tree.item(sel[0])['tags'][0])
        detalhes = EstornoService.obter_detalhes_venda_para_estorno(venda_id)
        
        if not detalhes:
            messagebox.showerror("Erro", "Venda não encontrada!")
            return
        
        self.mostrar_janela_detalhes(detalhes)
    
    def mostrar_janela_detalhes(self, detalhes: dict):
        """Mostra janela com detalhes da venda."""
        venda = detalhes['venda']
        itens = detalhes['itens']
        
        janela = tk.Toplevel(self)
        janela.title(f"Detalhes - {venda.numero_venda}")
        janela.geometry("600x500")
        janela.transient(self)
        janela.grab_set()
        
        # Header
        header = tk.Frame(janela, bg="#3498db", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"Venda #{venda.numero_venda}",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=15)
        
        # Corpo
        corpo = tk.Frame(janela, bg="#ffffff")
        corpo.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Informações
        info_frame = tk.Frame(corpo, bg="#ffffff")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_texto = f"""
Data/Hora: {venda.data_hora.strftime("%d/%m/%Y %H:%M:%S") if venda.data_hora else "N/A"}
Status: {venda.status.upper()}
Total: {Formatters.formatar_moeda(venda.total)}
Itens: {len(itens)}
        """
        
        tk.Label(
            info_frame,
            text=info_texto,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Itens
        tk.Label(
            corpo,
            text="Itens da Venda:",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(10, 5))
        
        tree_itens = ttk.Treeview(
            corpo,
            columns=("produto", "qtd", "preco", "subtotal"),
            show="headings",
            height=8
        )
        
        tree_itens.heading("produto", text="Produto")
        tree_itens.heading("qtd", text="Qtd")
        tree_itens.heading("preco", text="Preço Unit.")
        tree_itens.heading("subtotal", text="Subtotal")
        
        tree_itens.column("produto", width=300)
        tree_itens.column("qtd", width=80, anchor=tk.CENTER)
        tree_itens.column("preco", width=100, anchor=tk.E)
        tree_itens.column("subtotal", width=100, anchor=tk.E)
        
        for item in itens:
            from src.dao.produto_dao import ProdutoDAO
            produto = ProdutoDAO.buscar_por_id(item.produto_id)
            nome_produto = produto.nome if produto else f"Produto ID {item.produto_id}"
            
            tree_itens.insert("", tk.END, values=(
                nome_produto,
                f"{item.quantidade:.2f}".replace('.', ','),
                Formatters.formatar_moeda(item.preco_unitario),
                Formatters.formatar_moeda(item.subtotal)
            ))
        
        tree_itens.pack(fill=tk.BOTH, expand=True)
        
        # Botão fechar
        tk.Button(
            janela,
            text="Fechar",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=janela.destroy
        ).pack(pady=15)
    
    def iniciar_estorno(self):
        """Inicia processo de estorno."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma venda para estornar!")
            return
        
        venda_id = int(self.tree.item(sel[0])['tags'][0])
        
        # Valida estorno
        sucesso, mensagem, venda = EstornoService.validar_estorno(venda_id)
        if not sucesso:
            messagebox.showerror("Erro", mensagem)
            return
        
        # Confirmação
        confirma = messagebox.askyesno(
            "Confirmar Estorno",
            f"Estornar venda #{venda.numero_venda}?\n\n"
            f"Valor: {Formatters.formatar_moeda(venda.total)}\n\n"
            "⚠️ Esta ação NÃO pode ser desfeita!\n"
            "O estoque será revertido e a venda cancelada.",
            icon='warning'
        )
        
        if not confirma:
            return
        
        # Solicita motivo
        self.solicitar_motivo_estorno(venda_id)
    
    def solicitar_motivo_estorno(self, venda_id: int):
        """Solicita motivo do estorno."""
        janela = tk.Toplevel(self)
        janela.title("Motivo do Estorno")
        janela.geometry("500x350")
        janela.transient(self)
        janela.grab_set()
        
        # Header
        header = tk.Frame(janela, bg="#e74c3c", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Informar Motivo do Estorno",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white"
        ).pack(pady=15)
        
        # Corpo
        corpo = tk.Frame(janela, bg="#ffffff")
        corpo.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            corpo,
            text="Motivo: *",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        motivo_text = tk.Text(
            corpo,
            font=("Arial", 11),
            height=5,
            wrap=tk.WORD
        )
        motivo_text.pack(fill=tk.X, pady=(0, 15))
        motivo_text.focus()
        
        tk.Label(
            corpo,
            text="Observações:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        obs_text = tk.Text(
            corpo,
            font=("Arial", 11),
            height=3,
            wrap=tk.WORD
        )
        obs_text.pack(fill=tk.X)
        
        # Botões
        btn_frame = tk.Frame(janela, bg="#ffffff")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        def confirmar():
            motivo = motivo_text.get("1.0", tk.END).strip()
            if not motivo:
                messagebox.showwarning("Aviso", "Informe o motivo do estorno!")
                motivo_text.focus()
                return
            
            observacoes = obs_text.get("1.0", tk.END).strip() or None
            
            # Processa estorno
            sucesso, msg = EstornoService.processar_estorno(
                venda_id=venda_id,
                usuario_id=self.usuario_atual.id,
                motivo=motivo,
                observacoes=observacoes
            )
            
            janela.destroy()
            
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.carregar_vendas()
            else:
                messagebox.showerror("Erro", msg)
        
        tk.Button(
            btn_frame,
            text="✓ Confirmar Estorno",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=confirmar
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=janela.destroy
        ).pack(side=tk.LEFT)
