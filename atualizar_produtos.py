"""
Script para verificar e corrigir produtos no banco de dados.
"""

import sys
sys.path.insert(0, 'src')

import mysql.connector
from src.config.database import DatabaseConnection

def verificar_produtos():
    """Verifica os produtos atuais no banco."""
    try:
        with DatabaseConnection.get_cursor() as cursor:
            cursor.execute("SELECT * FROM produtos ORDER BY id")
            produtos = cursor.fetchall()
            
            print("=== PRODUTOS ATUAIS ===")
            for produto in produtos:
                print(f"ID: {produto['id']}")
                print(f"Código: {produto['codigo_barras']}")
                print(f"Nome: {produto['nome']}")
                print(f"Descrição: {produto['descricao']}")
                print(f"Categoria ID: {produto['categoria_id']}")
                print(f"Preço: R$ {produto['preco_venda']}")
                print(f"Estoque: {produto['estoque_atual']}")
                print("-" * 50)
            
            return produtos
    except Exception as e:
        print(f"Erro ao verificar produtos: {e}")
        return []

def corrigir_e_adicionar_produtos():
    """Corrige acentuação e adiciona novos produtos."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pdv_sistema',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        print("=== CORRIGINDO E ADICIONANDO PRODUTOS ===")
        
        # Remove produtos existentes para recriar com acentuação correta
        cursor.execute("DELETE FROM produtos")
        
        # Lista completa de produtos com acentuação correta
        produtos = [
            # Categoria 5 - Mercearia/Alimentos Básicos
            ('7891234567890', 'Arroz Branco 1kg', 'Arroz tipo 1 de qualidade', 5, 3.50, 5.99, 50, 10, 'UN'),
            ('7891234567891', 'Feijão Preto 1kg', 'Feijão preto tipo 1', 5, 4.00, 6.99, 40, 10, 'UN'),
            ('7891234567892', 'Açúcar Cristal 1kg', 'Açúcar cristal refinado', 5, 2.50, 4.49, 30, 10, 'UN'),
            ('7891234567893', 'Café Torrado 500g', 'Café torrado e moído tradicional', 1, 8.00, 12.99, 25, 5, 'UN'),
            ('7891234567894', 'Óleo de Soja 900ml', 'Óleo de soja refinado', 5, 4.20, 6.99, 35, 10, 'UN'),
            ('7891234567895', 'Sal Refinado 1kg', 'Sal refinado iodado', 5, 1.20, 2.49, 60, 15, 'UN'),
            ('7891234567896', 'Farinha de Trigo 1kg', 'Farinha de trigo especial', 5, 3.80, 5.99, 45, 12, 'UN'),
            ('7891234567897', 'Macarrão Espaguete 500g', 'Macarrão espaguete sêmola', 5, 2.80, 4.49, 55, 15, 'UN'),
            
            # Categoria 1 - Alimentos Frescos
            ('7891234567898', 'Leite Integral 1L', 'Leite integral longa vida', 1, 3.00, 4.99, 60, 15, 'UN'),
            ('7891234567899', 'Iogurte Natural 170g', 'Iogurte natural cremoso', 1, 1.80, 3.49, 40, 10, 'UN'),
            ('7891234567900', 'Margarina 500g', 'Margarina com sal', 1, 4.50, 6.99, 30, 8, 'UN'),
            ('7891234567901', 'Presunto Fatiado 200g', 'Presunto suíno fatiado', 1, 6.50, 9.99, 20, 5, 'UN'),
            ('7891234567902', 'Queijo Mussarela 200g', 'Queijo mussarela fatiado', 1, 7.80, 11.99, 25, 6, 'UN'),
            ('7891234567903', 'Ovos Brancos 12un', 'Ovos de galinha brancos', 1, 5.20, 7.99, 35, 8, 'DZ'),
            
            # Categoria 2 - Bebidas
            ('7891234567904', 'Refrigerante Cola 2L', 'Refrigerante sabor cola', 2, 4.50, 7.99, 35, 10, 'UN'),
            ('7891234567905', 'Água Mineral 1,5L', 'Água mineral natural sem gás', 2, 1.50, 2.99, 100, 20, 'UN'),
            ('7891234567906', 'Suco de Laranja 1L', 'Suco de laranja integral', 2, 3.80, 5.99, 25, 8, 'UN'),
            ('7891234567907', 'Cerveja Lata 350ml', 'Cerveja pilsen lata', 2, 2.20, 3.49, 48, 12, 'UN'),
            ('7891234567908', 'Energético 250ml', 'Bebida energética', 2, 4.20, 6.99, 30, 10, 'UN'),
            ('7891234567909', 'Água de Coco 200ml', 'Água de coco natural', 2, 2.50, 3.99, 40, 12, 'UN'),
            
            # Categoria 3 - Limpeza
            ('7891234567910', 'Detergente Líquido 500ml', 'Detergente neutro concentrado', 3, 1.80, 2.99, 45, 10, 'UN'),
            ('7891234567911', 'Sabão em Pó 1kg', 'Sabão em pó para roupas', 3, 6.00, 9.99, 30, 8, 'UN'),
            ('7891234567912', 'Desinfetante 500ml', 'Desinfetante uso geral', 3, 3.20, 4.99, 25, 8, 'UN'),
            ('7891234567913', 'Água Sanitária 1L', 'Água sanitária alvejante', 3, 2.80, 3.99, 35, 12, 'UN'),
            ('7891234567914', 'Esponja de Aço 8un', 'Esponja de aço multiuso', 3, 2.50, 3.99, 50, 15, 'PC'),
            ('7891234567915', 'Papel Higiênico 4un', 'Papel higiênico folha dupla', 3, 5.80, 8.99, 40, 12, 'PC'),
            
            # Categoria 4 - Higiene Pessoal
            ('7891234567916', 'Sabonete 90g', 'Sabonete em barra glicerina', 4, 1.20, 2.49, 80, 20, 'UN'),
            ('7891234567917', 'Shampoo 350ml', 'Shampoo para cabelos normais', 4, 6.50, 9.99, 20, 6, 'UN'),
            ('7891234567918', 'Condicionador 350ml', 'Condicionador hidratante', 4, 6.80, 10.49, 18, 6, 'UN'),
            ('7891234567919', 'Pasta de Dente 90g', 'Creme dental com flúor', 4, 3.20, 4.99, 35, 10, 'UN'),
            ('7891234567920', 'Desodorante Spray 150ml', 'Desodorante antitranspirante', 4, 8.50, 12.99, 25, 8, 'UN'),
            ('7891234567921', 'Absorvente 8un', 'Absorvente higiênico suave', 4, 4.80, 7.49, 30, 10, 'PC'),
            
            # Produtos Adicionais - Categoria 1 (Alimentos)
            ('7891234567922', 'Pão de Açúcar 500g', 'Pão de açúcar tradicional', 1, 4.20, 6.49, 25, 8, 'UN'),
            ('7891234567923', 'Biscoito Recheado 140g', 'Biscoito recheado chocolate', 1, 2.80, 4.49, 45, 12, 'UN'),
            ('7891234567924', 'Chocolate ao Leite 90g', 'Chocolate ao leite cremoso', 1, 3.50, 5.49, 35, 10, 'UN'),
            ('7891234567925', 'Sardinha em Lata 125g', 'Sardinha em óleo comestível', 1, 3.80, 5.99, 40, 12, 'UN'),
            ('7891234567926', 'Molho de Tomate 340g', 'Molho de tomate tradicional', 1, 2.20, 3.49, 50, 15, 'UN'),
            
            # Produtos Sazonais/Especiais
            ('7891234567927', 'Sorvete 2L', 'Sorvete napolitano família', 1, 8.50, 12.99, 15, 5, 'UN'),
            ('7891234567928', 'Pizza Congelada 460g', 'Pizza congelada mussarela', 1, 9.20, 13.99, 20, 6, 'UN'),
            ('7891234567929', 'Batata Frita 500g', 'Batata pré-frita congelada', 1, 6.80, 9.99, 25, 8, 'UN'),
            ('7891234567930', 'Frango Congelado 1kg', 'Frango inteiro congelado', 1, 7.50, 11.49, 30, 10, 'KG'),
        ]
        
        # Insere os produtos
        for produto in produtos:
            cursor.execute("""
                INSERT INTO produtos (
                    codigo_barras, nome, descricao, categoria_id, 
                    preco_custo, preco_venda, estoque_atual, estoque_minimo, 
                    unidade_medida, ativo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (*produto, True))
        
        conn.commit()
        print(f"✅ {len(produtos)} produtos inseridos com sucesso!")
        
        # Verifica as categorias também
        cursor.execute("SELECT * FROM categorias ORDER BY id")
        categorias = cursor.fetchall()
        
        print("\n=== CATEGORIAS DISPONÍVEIS ===")
        for cat in categorias:
            cursor.execute("SELECT COUNT(*) as total FROM produtos WHERE categoria_id = %s", (cat[0],))
            total = cursor.fetchone()[0]
            print(f"ID {cat[0]}: {cat[1]} - {total} produtos")
        
        cursor.close()
        conn.close()
        
        print("\n✅ PRODUTOS ATUALIZADOS COM SUCESSO!")
        print("🛒 Agora o sistema tem uma variedade completa de produtos para teste!")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Verificando produtos atuais...")
    verificar_produtos()
    
    print("\nCorrigindo e adicionando produtos...")
    corrigir_e_adicionar_produtos()
    
    print("\nVerificando produtos após atualização...")
    verificar_produtos()