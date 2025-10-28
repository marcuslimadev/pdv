"""
Script para popular o banco de dados com produtos de exemplo
"""
import sys
from decimal import Decimal
from src.config.database import DatabaseConnection
from src.dao.produto_dao import ProdutoDAO
from src.dao.categoria_dao import CategoriaDAO
from src.models.produto import Produto
from src.models.categoria import Categoria

def limpar_produtos():
    """Remove todos os produtos e itens de venda."""
    DatabaseConnection.initialize_pool()
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM itens_venda")
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        print("✓ Produtos anteriores removidos")
    except Exception as e:
        conn.rollback()
        print(f"✗ Erro ao limpar produtos: {e}")
    finally:
        cursor.close()
        conn.close()

def criar_categorias():
    """Cria categorias de exemplo."""
    categorias = [
        ("Bebidas", "Refrigerantes, sucos e água"),
        ("Snacks", "Salgadinhos e petiscos"),
        ("Doces", "Chocolates, balas e doces"),
        ("Higiene", "Produtos de higiene pessoal"),
        ("Limpeza", "Produtos de limpeza")
    ]
    
    print("\n📁 Criando categorias...")
    for nome, desc in categorias:
        try:
            cat = Categoria(nome=nome, descricao=desc)
            CategoriaDAO.criar(cat)
            print(f"  ✓ {nome}")
        except Exception as e:
            print(f"  ✗ {nome}: {e}")

def criar_produtos():
    """Cria produtos de exemplo."""
    produtos = [
        # Bebidas
        ("7891234567890", "Coca-Cola 2L", 1, 8.50, 10.99, 50, "UN"),
        ("7891234567891", "Guaraná Antarctica 2L", 1, 7.50, 9.99, 45, "UN"),
        ("7891234567892", "Água Mineral 500ml", 1, 0.80, 1.99, 100, "UN"),
        ("7891234567893", "Suco Del Valle 1L", 1, 4.50, 6.99, 30, "UN"),
        ("7891234567894", "Red Bull 250ml", 1, 6.00, 12.99, 24, "UN"),
        
        # Snacks
        ("7891234567895", "Doritos 100g", 2, 3.50, 6.99, 40, "UN"),
        ("7891234567896", "Ruffles 100g", 2, 3.50, 6.99, 35, "UN"),
        ("7891234567897", "Cheetos 100g", 2, 3.50, 6.99, 38, "UN"),
        ("7891234567898", "Fandangos 100g", 2, 3.00, 5.99, 42, "UN"),
        
        # Doces
        ("7891234567899", "Chocolate Lacta 90g", 3, 4.00, 7.99, 50, "UN"),
        ("7891234567900", "Bis Xtra 45g", 3, 2.00, 3.99, 60, "UN"),
        ("7891234567901", "M&M's 100g", 3, 5.00, 9.99, 30, "UN"),
        ("7891234567902", "Trident 8g", 3, 1.00, 2.49, 80, "UN"),
        
        # Higiene
        ("7891234567903", "Sabonete Dove 90g", 4, 2.50, 4.99, 45, "UN"),
        ("7891234567904", "Shampoo Seda 325ml", 4, 8.00, 15.99, 25, "UN"),
        ("7891234567905", "Pasta Dental Colgate 90g", 4, 3.50, 6.99, 40, "UN"),
        ("7891234567906", "Desodorante Rexona 150ml", 4, 7.00, 13.99, 30, "UN"),
        
        # Limpeza
        ("7891234567907", "Detergente Ypê 500ml", 5, 1.50, 2.99, 60, "UN"),
        ("7891234567908", "Desinfetante Pinho Sol 1L", 5, 5.00, 9.99, 35, "UN"),
        ("7891234567909", "Sabão em Pó OMO 1kg", 5, 12.00, 19.99, 20, "KG"),
        ("7891234567910", "Água Sanitária 1L", 5, 2.00, 3.99, 40, "UN"),
    ]
    
    print("\n📦 Criando produtos...")
    for codigo, nome, cat_id, custo, venda, estoque, unidade in produtos:
        try:
            produto = Produto(
                codigo_barras=codigo,
                nome=nome,
                categoria_id=cat_id,
                preco_custo=Decimal(str(custo)),
                preco_venda=Decimal(str(venda)),
                estoque_minimo=10,
                estoque_atual=estoque,
                unidade_medida=unidade,
                ativo=True
            )
            ProdutoDAO.criar(produto)
            print(f"  ✓ {nome} - R$ {venda}")
        except Exception as e:
            print(f"  ✗ {nome}: {e}")

def main():
    """Função principal."""
    print("=" * 60)
    print("🏪 Populando banco de dados com produtos de exemplo")
    print("=" * 60)
    
    limpar_produtos()
    criar_categorias()
    criar_produtos()
    
    print("\n" + "=" * 60)
    print("✅ Banco de dados populado com sucesso!")
    print("=" * 60)
    print("\n💡 Agora você pode:")
    print("   - Acessar o PDV: http://localhost:5000/pdv")
    print("   - Testar vendas com os produtos cadastrados")
    print("   - Gerenciar produtos em: http://localhost:5000/produtos")
    print()

if __name__ == '__main__':
    main()
