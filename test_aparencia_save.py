"""
Script de teste para debug da gravação de aparência
"""
import traceback
from src.services.aparencia_service import AparenciaService

def test_save():
    print("="*60)
    print("TESTE DE GRAVAÇÃO DE APARÊNCIA")
    print("="*60)
    
    service = AparenciaService()
    
    # Teste 1: Carregar configurações existentes
    print("\n1. Carregando configurações atuais...")
    try:
        config_atual = service.get_configuracoes()
        print(f"   ✓ Configurações carregadas: {len(config_atual)} campos")
        for key, value in config_atual.items():
            print(f"   - {key}: {value}")
    except Exception as e:
        print(f"   ✗ Erro ao carregar: {e}")
        traceback.print_exc()
        return
    
    # Teste 2: Modificar uma cor
    print("\n2. Modificando cor primária...")
    config_teste = config_atual.copy()
    config_teste['cor_primaria'] = '#FF5733'  # Laranja
    print(f"   Nova cor primária: {config_teste['cor_primaria']}")
    
    # Teste 3: Tentar salvar
    print("\n3. Salvando configurações...")
    try:
        resultado = service.salvar_configuracoes(config_teste)
        if resultado:
            print("   ✓ Configurações salvas com sucesso!")
        else:
            print("   ✗ Falha ao salvar (retornou False)")
    except Exception as e:
        print(f"   ✗ Exceção ao salvar: {e}")
        traceback.print_exc()
        return
    
    # Teste 4: Verificar se foi salvo
    print("\n4. Verificando se foi salvo...")
    try:
        service._config_cache = None  # Limpa cache
        config_verificacao = service.get_configuracoes()
        if config_verificacao['cor_primaria'] == '#FF5733':
            print(f"   ✓ Salvo corretamente! Cor primária = {config_verificacao['cor_primaria']}")
        else:
            print(f"   ✗ Não foi salvo. Cor primária = {config_verificacao['cor_primaria']}")
    except Exception as e:
        print(f"   ✗ Erro ao verificar: {e}")
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("FIM DO TESTE")
    print("="*60)

if __name__ == "__main__":
    test_save()
