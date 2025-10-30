"""
Módulo para alertas sonoros e visuais de estoque.
Usa winsound para emitir beeps e retorna cores para indicadores visuais.
"""

import winsound
from typing import Tuple, Optional
from src.config.config_reader import config


class EstoqueAlerta:
    """Gerencia alertas de estoque baixo/zerado."""
    
    # Frequências e durações de beeps (Hz, ms)
    BEEP_ESTOQUE_ZERO = (800, 300)      # Tom grave, longo
    BEEP_ESTOQUE_BAIXO = (600, 150)     # Tom médio, curto
    
    # Cores para indicadores visuais
    COR_ESTOQUE_OK = "#27ae60"          # Verde
    COR_ESTOQUE_BAIXO = "#f39c12"       # Laranja
    COR_ESTOQUE_ZERO = "#e74c3c"        # Vermelho
    COR_ESTOQUE_NEGATIVO = "#8e44ad"    # Roxo (crítico)
    
    @staticmethod
    def verificar_estoque(estoque_atual: int, estoque_minimo: Optional[int] = None) -> dict:
        """
        Verifica o nível de estoque e retorna informações sobre o alerta.
        
        Args:
            estoque_atual: Quantidade atual em estoque
            estoque_minimo: Quantidade mínima configurada (usa padrão se None)
            
        Returns:
            dict com: {
                'nivel': 'ok'|'baixo'|'zero'|'negativo',
                'cor': cor hexadecimal,
                'icone': emoji,
                'mensagem': texto descritivo,
                'deve_alertar': bool
            }
        """
        # Se não informado, usa o estoque mínimo padrão do config
        if estoque_minimo is None:
            estoque_minimo = config.get_estoque_minimo_padrao()
        
        # Estoque negativo (crítico - bug ou erro)
        if estoque_atual < 0:
            return {
                'nivel': 'negativo',
                'cor': EstoqueAlerta.COR_ESTOQUE_NEGATIVO,
                'icone': '⚠️',
                'mensagem': f'ESTOQUE NEGATIVO: {estoque_atual}',
                'deve_alertar': True
            }
        
        # Estoque zerado
        elif estoque_atual == 0:
            return {
                'nivel': 'zero',
                'cor': EstoqueAlerta.COR_ESTOQUE_ZERO,
                'icone': '🔴',
                'mensagem': 'ESTOQUE ZERADO',
                'deve_alertar': True
            }
        
        # Estoque baixo
        elif estoque_atual <= estoque_minimo:
            return {
                'nivel': 'baixo',
                'cor': EstoqueAlerta.COR_ESTOQUE_BAIXO,
                'icone': '🟡',
                'mensagem': f'Estoque Baixo: {estoque_atual} un.',
                'deve_alertar': True
            }
        
        # Estoque OK
        else:
            return {
                'nivel': 'ok',
                'cor': EstoqueAlerta.COR_ESTOQUE_OK,
                'icone': '🟢',
                'mensagem': f'Estoque: {estoque_atual} un.',
                'deve_alertar': False
            }
    
    @staticmethod
    def emitir_beep_estoque(nivel: str, repetir: int = 1):
        """
        Emite beep sonoro de acordo com o nível de estoque.
        
        Args:
            nivel: 'zero', 'baixo', 'negativo'
            repetir: Número de vezes para repetir o beep
        """
        try:
            if nivel in ['zero', 'negativo']:
                freq, duracao = EstoqueAlerta.BEEP_ESTOQUE_ZERO
            elif nivel == 'baixo':
                freq, duracao = EstoqueAlerta.BEEP_ESTOQUE_BAIXO
            else:
                return  # Não emite som para estoque OK
            
            for _ in range(repetir):
                winsound.Beep(freq, duracao)
                if repetir > 1:
                    winsound.Beep(0, 100)  # Pausa entre beeps
                    
        except RuntimeError:
            # Em caso de erro no winsound (sistema sem som), ignora silenciosamente
            pass
    
    @staticmethod
    def alertar_se_necessario(estoque_atual: int, estoque_minimo: Optional[int] = None, 
                              emitir_som: bool = True) -> dict:
        """
        Verifica estoque e emite alerta se necessário.
        
        Args:
            estoque_atual: Quantidade atual
            estoque_minimo: Mínimo configurado
            emitir_som: Se deve emitir beep sonoro
            
        Returns:
            dict com informações do alerta
        """
        info = EstoqueAlerta.verificar_estoque(estoque_atual, estoque_minimo)
        
        if info['deve_alertar'] and emitir_som:
            # Negativo: 3 beeps graves
            if info['nivel'] == 'negativo':
                EstoqueAlerta.emitir_beep_estoque('negativo', repetir=3)
            # Zero: 2 beeps graves
            elif info['nivel'] == 'zero':
                EstoqueAlerta.emitir_beep_estoque('zero', repetir=2)
            # Baixo: 1 beep médio
            elif info['nivel'] == 'baixo':
                EstoqueAlerta.emitir_beep_estoque('baixo', repetir=1)
        
        return info
