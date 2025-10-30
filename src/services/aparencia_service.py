"""
Serviço de Aparência - Gerencia configurações visuais do sistema
"""
import os
from typing import Dict, Any, Optional
from src.config.database import DatabaseConnection
from src.utils.logger import Logger

class AparenciaService:
    """Gerencia configurações de aparência personalizáveis"""
    
    # Configurações padrão
    DEFAULTS = {
        'cor_primaria': '#6C5CE7',
        'cor_secundaria': '#00B894',
        'cor_destaque': '#FDCB6E',
        'cor_perigo': '#D63031',
        'cor_info': '#74B9FF',
        'cor_aviso': '#FFEAA7',
        'cor_texto_primario': '#2D3436',
        'cor_texto_secundario': '#636E72',
        'cor_fundo': '#F5F6FA',
        'fonte_principal': 'Segoe UI',
        'tamanho_fonte_pequeno': 8,
        'tamanho_fonte_normal': 10,
        'tamanho_fonte_medio': 11,
        'tamanho_fonte_grande': 13,
        'tamanho_fonte_xlarge': 16,
        'tamanho_fonte_xxlarge': 24,
        'tamanho_fonte_huge': 32,
        'borda_arredondada': 4,
        'logotipo_path': None,
        'mostrar_logotipo': False,
        'logotipo_largura': 150,
        'logotipo_altura': 50
    }
    
    def __init__(self):
        self.logger = Logger()
        self._config_cache = None
    
    def get_configuracoes(self) -> Dict[str, Any]:
        """Obtém todas as configurações de aparência"""
        if self._config_cache is not None:
            return self._config_cache
        
        conn = None
        cursor = None
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    cor_primaria, cor_secundaria, cor_destaque, cor_perigo, cor_info, cor_aviso,
                    cor_texto_primario, cor_texto_secundario, cor_fundo,
                    fonte_principal,
                    tamanho_fonte_pequeno, tamanho_fonte_normal, tamanho_fonte_medio,
                    tamanho_fonte_grande, tamanho_fonte_xlarge, tamanho_fonte_xxlarge, tamanho_fonte_huge,
                    borda_arredondada, logotipo_path, mostrar_logotipo, logotipo_largura, logotipo_altura
                FROM aparencia_config
                WHERE id = 1
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            
            if result:
                # Converte booleano
                result['mostrar_logotipo'] = bool(result.get('mostrar_logotipo', False))
                self._config_cache = result
                return result
            else:
                # Retorna configurações padrão
                return self.DEFAULTS.copy()
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações de aparência: {e}")
            return self.DEFAULTS.copy()
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def salvar_configuracoes(self, config: Dict[str, Any]) -> bool:
        """Salva configurações de aparência"""
        conn = None
        cursor = None
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            
            # Verifica se já existe configuração
            cursor.execute("SELECT id FROM aparencia_config WHERE id = 1")
            existing = cursor.fetchone()
            
            if existing:
                # Atualiza
                cursor.execute("""
                    UPDATE aparencia_config SET
                        cor_primaria = %s,
                        cor_secundaria = %s,
                        cor_destaque = %s,
                        cor_perigo = %s,
                        cor_info = %s,
                        cor_aviso = %s,
                        cor_texto_primario = %s,
                        cor_texto_secundario = %s,
                        cor_fundo = %s,
                        fonte_principal = %s,
                        tamanho_fonte_pequeno = %s,
                        tamanho_fonte_normal = %s,
                        tamanho_fonte_medio = %s,
                        tamanho_fonte_grande = %s,
                        tamanho_fonte_xlarge = %s,
                        tamanho_fonte_xxlarge = %s,
                        tamanho_fonte_huge = %s,
                        borda_arredondada = %s,
                        logotipo_path = %s,
                        mostrar_logotipo = %s,
                        logotipo_largura = %s,
                        logotipo_altura = %s
                    WHERE id = 1
                """, (
                    config.get('cor_primaria', self.DEFAULTS['cor_primaria']),
                    config.get('cor_secundaria', self.DEFAULTS['cor_secundaria']),
                    config.get('cor_destaque', self.DEFAULTS['cor_destaque']),
                    config.get('cor_perigo', self.DEFAULTS['cor_perigo']),
                    config.get('cor_info', self.DEFAULTS['cor_info']),
                    config.get('cor_aviso', self.DEFAULTS['cor_aviso']),
                    config.get('cor_texto_primario', self.DEFAULTS['cor_texto_primario']),
                    config.get('cor_texto_secundario', self.DEFAULTS['cor_texto_secundario']),
                    config.get('cor_fundo', self.DEFAULTS['cor_fundo']),
                    config.get('fonte_principal', self.DEFAULTS['fonte_principal']),
                    config.get('tamanho_fonte_pequeno', self.DEFAULTS['tamanho_fonte_pequeno']),
                    config.get('tamanho_fonte_normal', self.DEFAULTS['tamanho_fonte_normal']),
                    config.get('tamanho_fonte_medio', self.DEFAULTS['tamanho_fonte_medio']),
                    config.get('tamanho_fonte_grande', self.DEFAULTS['tamanho_fonte_grande']),
                    config.get('tamanho_fonte_xlarge', self.DEFAULTS['tamanho_fonte_xlarge']),
                    config.get('tamanho_fonte_xxlarge', self.DEFAULTS['tamanho_fonte_xxlarge']),
                    config.get('tamanho_fonte_huge', self.DEFAULTS['tamanho_fonte_huge']),
                    config.get('borda_arredondada', self.DEFAULTS['borda_arredondada']),
                    config.get('logotipo_path'),
                    config.get('mostrar_logotipo', False),
                    config.get('logotipo_largura', self.DEFAULTS['logotipo_largura']),
                    config.get('logotipo_altura', self.DEFAULTS['logotipo_altura'])
                ))
            else:
                # Insere novo
                cursor.execute("""
                    INSERT INTO aparencia_config (
                        id,
                        cor_primaria, cor_secundaria, cor_destaque, cor_perigo, cor_info, cor_aviso,
                        cor_texto_primario, cor_texto_secundario, cor_fundo,
                        fonte_principal,
                        tamanho_fonte_pequeno, tamanho_fonte_normal, tamanho_fonte_medio,
                        tamanho_fonte_grande, tamanho_fonte_xlarge, tamanho_fonte_xxlarge, tamanho_fonte_huge,
                        borda_arredondada, logotipo_path, mostrar_logotipo, logotipo_largura, logotipo_altura
                    ) VALUES (
                        1,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    config.get('cor_primaria', self.DEFAULTS['cor_primaria']),
                    config.get('cor_secundaria', self.DEFAULTS['cor_secundaria']),
                    config.get('cor_destaque', self.DEFAULTS['cor_destaque']),
                    config.get('cor_perigo', self.DEFAULTS['cor_perigo']),
                    config.get('cor_info', self.DEFAULTS['cor_info']),
                    config.get('cor_aviso', self.DEFAULTS['cor_aviso']),
                    config.get('cor_texto_primario', self.DEFAULTS['cor_texto_primario']),
                    config.get('cor_texto_secundario', self.DEFAULTS['cor_texto_secundario']),
                    config.get('cor_fundo', self.DEFAULTS['cor_fundo']),
                    config.get('fonte_principal', self.DEFAULTS['fonte_principal']),
                    config.get('tamanho_fonte_pequeno', self.DEFAULTS['tamanho_fonte_pequeno']),
                    config.get('tamanho_fonte_normal', self.DEFAULTS['tamanho_fonte_normal']),
                    config.get('tamanho_fonte_medio', self.DEFAULTS['tamanho_fonte_medio']),
                    config.get('tamanho_fonte_grande', self.DEFAULTS['tamanho_fonte_grande']),
                    config.get('tamanho_fonte_xlarge', self.DEFAULTS['tamanho_fonte_xlarge']),
                    config.get('tamanho_fonte_xxlarge', self.DEFAULTS['tamanho_fonte_xxlarge']),
                    config.get('tamanho_fonte_huge', self.DEFAULTS['tamanho_fonte_huge']),
                    config.get('borda_arredondada', self.DEFAULTS['borda_arredondada']),
                    config.get('logotipo_path'),
                    config.get('mostrar_logotipo', False),
                    config.get('logotipo_largura', self.DEFAULTS['logotipo_largura']),
                    config.get('logotipo_altura', self.DEFAULTS['logotipo_altura'])
                ))
            
            conn.commit()
            
            # Limpa cache
            self._config_cache = None
            
            self.logger.info("Configurações de aparência salvas com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações de aparência: {e}")
            import traceback
            traceback.print_exc()
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def restaurar_padrao(self) -> bool:
        """Restaura configurações padrão"""
        return self.salvar_configuracoes(self.DEFAULTS)
    
    def validar_cor(self, cor: str) -> bool:
        """Valida formato de cor hexadecimal"""
        import re
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', cor))
    
    def validar_logotipo(self, path: Optional[str]) -> bool:
        """Valida se o arquivo de logotipo existe"""
        if not path:
            return True
        return os.path.exists(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
