"""Tela de configurações administrativas."""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

from src.services.config_service import config_service


class ConfiguracoesFrame(ttk.Frame):
    """Frame para editar configurações do sistema."""

    def __init__(self, parent):
        super().__init__(parent)
        self.var_plataforma = tk.StringVar()
        self.var_cliente = tk.StringVar()
        self.status_var = tk.StringVar()

        self._carregar_valores_iniciais()
        self._criar_widgets()
        self._configurar_bindings()

    def _carregar_valores_iniciais(self) -> None:
        cliente, plataforma = config_service.get_pix_split_percentages()
        self.var_plataforma.set(f"{plataforma:.2f}")
        self.var_cliente.set(f"{cliente:.2f}")
        self.status_var.set("")

    def _criar_widgets(self) -> None:
        tk.Label(
            self,
            text="⚙️ Configurações do Sistema",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 20))

        explicacao = tk.Label(
            self,
            text=(
                "Defina como as vendas PIX serão divididas. O percentual da plataforma"
                " é descontado automaticamente e o restante segue para a conta do cliente."
            ),
            font=("Arial", 11),
            fg="#7f8c8d",
            justify=tk.LEFT,
            wraplength=700
        )
        explicacao.pack(fill=tk.X, pady=(0, 20))

        box = ttk.LabelFrame(self, text="Divisão PIX")
        box.pack(fill=tk.X, padx=10, pady=(0, 20))

        form = ttk.Frame(box, padding=10)
        form.pack(fill=tk.X)

        ttk.Label(
            form,
            text="Percentual da Plataforma (sua conta):",
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w")

        self.entry_plataforma = ttk.Entry(form, textvariable=self.var_plataforma, width=10, font=("Arial", 12))
        self.entry_plataforma.grid(row=0, column=1, padx=(10, 0))

        ttk.Label(
            form,
            text="%",
            font=("Arial", 11)
        ).grid(row=0, column=2, sticky="w", padx=(5, 0))

        ttk.Label(
            form,
            text="Percentual do Cliente (destinatário principal):",
            font=("Arial", 11)
        ).grid(row=1, column=0, sticky="w", pady=(10, 0))

        ttk.Label(
            form,
            textvariable=self.var_cliente,
            font=("Arial", 12, "bold")
        ).grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(10, 0))

        ttk.Label(
            form,
            text="%",
            font=("Arial", 11)
        ).grid(row=1, column=2, sticky="w", padx=(5, 0), pady=(10, 0))

        avisos = tk.Label(
            box,
            text=(
                "A soma deve ser 100%. A plataforma deve permanecer com pelo menos 0% e"
                " no máximo 100%."
            ),
            font=("Arial", 10),
            fg="#7f8c8d",
            anchor="w",
            justify=tk.LEFT
        )
        avisos.pack(fill=tk.X, padx=10, pady=(10, 0))

        botoes = ttk.Frame(self)
        botoes.pack(fill=tk.X, pady=(10, 0))

        self.status_label = tk.Label(
            botoes,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(side=tk.LEFT)

        salvar_btn = tk.Button(
            botoes,
            text="💾 Salvar Configurações",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            command=self._salvar
        )
        salvar_btn.pack(side=tk.RIGHT)

    def _configurar_bindings(self) -> None:
        self.entry_plataforma.bind('<Return>', lambda e: self._salvar())
        self.entry_plataforma.bind('<FocusOut>', lambda e: self._atualizar_cliente_label())

    def _atualizar_cliente_label(self) -> None:
        try:
            plataforma = Decimal(self.var_plataforma.get().replace(',', '.'))
        except (InvalidOperation, AttributeError):
            plataforma = Decimal("0")
        plataforma = max(Decimal("0"), min(Decimal("100"), plataforma))
        cliente = Decimal("100") - plataforma
        self.var_cliente.set(f"{cliente:.2f}")

    def _salvar(self) -> None:
        try:
            valor = Decimal(self.var_plataforma.get().replace(',', '.'))
        except (InvalidOperation, AttributeError):
            messagebox.showerror("Configurações", "Informe um número válido para o percentual da plataforma.")
            self.entry_plataforma.focus_set()
            return

        if valor < 0 or valor > 100:
            messagebox.showerror("Configurações", "O percentual deve ficar entre 0 e 100%.")
            self.entry_plataforma.focus_set()
            return

        cliente, plataforma = config_service.set_pix_platform_percent(valor)
        self.var_plataforma.set(f"{plataforma:.2f}")
        self.var_cliente.set(f"{cliente:.2f}")
        self.status_var.set("Configurações salvas com sucesso.")
        self.after(4000, lambda: self.status_var.set(""))
        self.entry_plataforma.focus_set()
