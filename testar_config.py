"""
Script para testar a leitura de configurações do config.ini
"""

from src.config.config_reader import config

def testar_config():
    """Testa todas as configurações."""
    
    print("=" * 60)
    print("TESTE DE CONFIGURAÇÕES - config.ini")
    print("=" * 60)
    
    print("\n[DATABASE]")
    print(f"Host: {config.get_db_host()}")
    print(f"Port: {config.get_db_port()}")
    print(f"User: {config.get_db_user()}")
    print(f"Password: {'*' * len(config.get_db_password())}")
    print(f"Database: {config.get_db_name()}")
    print(f"Pool Size: {config.get_db_pool_size()}")
    
    print("\n[MERCADO PAGO]")
    mp_token = config.get_mp_access_token()
    print(f"Access Token: {mp_token[:20] + '...' if mp_token else 'Não configurado'}")
    mp_key = config.get_mp_public_key()
    print(f"Public Key: {mp_key[:20] + '...' if mp_key else 'Não configurado'}")
    print(f"Percentual Plataforma: {config.get_mp_percentual_plataforma()}%")
    print(f"Webhook URL: {config.get_mp_webhook_url() or 'Não configurado'}")
    
    print("\n[PIX]")
    print(f"Chave PIX: {config.get_pix_chave() or 'Não configurado'}")
    print(f"Nome Recebedor: {config.get_pix_nome_recebedor()}")
    print(f"Cidade: {config.get_pix_cidade_recebedor()}")
    
    print("\n[SISTEMA]")
    print(f"Nome Empresa: {config.get_nome_empresa()}")
    print(f"CNPJ: {config.get_cnpj() or 'Não configurado'}")
    print(f"Endereço: {config.get_endereco() or 'Não configurado'}")
    print(f"Telefone: {config.get_telefone() or 'Não configurado'}")
    print(f"Log Path: {config.get_log_path()}")
    print(f"Backup Path: {config.get_backup_path()}")
    print(f"Reports Path: {config.get_reports_path()}")
    print(f"Log Level: {config.get_log_level()}")
    print(f"Estoque Mínimo Padrão: {config.get_estoque_minimo_padrao()}")
    
    print("\n" + "=" * 60)
    print("✓ Configurações carregadas com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        testar_config()
    except FileNotFoundError as e:
        print(f"\n✗ ERRO: {e}")
        print("\nPor favor, copie config.ini.example para config.ini e configure.")
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
