"""
Restaura configurações padrão de aparência
"""
from src.services.aparencia_service import AparenciaService

service = AparenciaService()
if service.restaurar_padrao():
    print("✓ Configurações restauradas para o padrão!")
else:
    print("✗ Erro ao restaurar configurações")
