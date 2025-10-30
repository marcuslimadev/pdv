#!/usr/bin/env python3
"""
Visualizar splits pendentes para processamento manual.
"""

import json
import os
from decimal import Decimal

def visualizar_splits_pendentes():
    """Mostra todos os splits pendentes."""

    arquivo_splits = "splits_pendentes.json"

    if not os.path.exists(arquivo_splits):
        print("📄 Nenhum split pendente encontrado.")
        return

    try:
        with open(arquivo_splits, 'r', encoding='utf-8') as f:
            splits = json.load(f)

        if not splits:
            print("📄 Nenhum split pendente encontrado.")
            return

        print("=" * 80)
        print("💰 SPLITS PENDENTES PARA PROCESSAMENTO MANUAL")
        print("=" * 80)

        total_pendente = Decimal('0')

        for i, split in enumerate(splits, 1):
            print(f"\n🔹 Split #{i}")
            print(f"   Payment ID: {split['payment_id']}")
            print(f"   Valor Total: R$ {split['valor_total']:.2f}")
            print(f"   Cliente: R$ {split['valor_cliente']:.2f} ({split['percentual_cliente']}%)")
            print(f"   Plataforma: R$ {split['valor_plataforma']:.2f} ({split['percentual_plataforma']}%)")
            print(f"   PIX Plataforma: {split['pix_plataforma']}")
            print(f"   Data: {split['data_processamento']}")
            print(f"   Status: {split['status']}")

            if split['status'] == 'PENDENTE':
                total_pendente += Decimal(str(split['valor_plataforma']))

        print(f"\n💵 Total pendente para plataforma: R$ {float(total_pendente):.2f}")
        print("=" * 80)

        print(f"\n📋 Para processar os splits:")
        print(f"   1. Abra seu app de banco")
        print(f"   2. Faça PIX de R$ {float(total_pendente):.2f} para {splits[0]['pix_plataforma']}")
        print(f"   3. Execute: python limpar_splits.py")
        print("=" * 80)

    except Exception as e:
        print(f"❌ Erro ao ler splits pendentes: {e}")

if __name__ == "__main__":
    visualizar_splits_pendentes()