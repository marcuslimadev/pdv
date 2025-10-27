"""
Script para testar o login dos usuários.
"""

import sys
sys.path.insert(0, 'src')

from src.dao.usuario_dao import UsuarioDAO
from src.models.usuario import Usuario
import bcrypt

def test_usuarios():
    """Testa os usuários cadastrados."""
    print("=== TESTE DE USUÁRIOS ===")
    
    # Lista todos os usuários
    usuarios = UsuarioDAO.buscar_todos(apenas_ativos=True)
    print(f"\nUsuários cadastrados: {len(usuarios)}")
    
    for usuario in usuarios:
        print(f"- ID: {usuario.id}")
        print(f"  Username: {usuario.username}")
        print(f"  Nome: {usuario.nome_completo}")
        print(f"  Tipo: {usuario.tipo}")
        print(f"  Ativo: {usuario.ativo}")
        print(f"  Hash da senha: {usuario.senha_hash[:50]}...")
        print()
    
    # Testa login do admin
    print("=== TESTE DE LOGIN ===")
    print("Testando login do admin...")
    
    admin = UsuarioDAO.autenticar('admin', 'admin123')
    if admin:
        print("✓ Login do admin funcionou!")
        print(f"  Usuário: {admin.nome_completo}")
    else:
        print("✗ Login do admin FALHOU!")
    
    # Testa login do operador
    print("\nTestando login do operador...")
    operador = UsuarioDAO.autenticar('operador', 'operador123')
    if operador:
        print("✓ Login do operador funcionou!")
        print(f"  Usuário: {operador.nome_completo}")
    else:
        print("✗ Login do operador FALHOU!")
    
    # Testa senha errada
    print("\nTestando senha errada...")
    teste_erro = UsuarioDAO.autenticar('admin', 'senha_errada')
    if teste_erro:
        print("✗ PROBLEMA! Login com senha errada funcionou!")
    else:
        print("✓ Login com senha errada foi rejeitado corretamente")

if __name__ == "__main__":
    test_usuarios()