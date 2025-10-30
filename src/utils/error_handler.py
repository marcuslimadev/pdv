"""
Módulo para tratamento de erros e mensagens user-friendly.
Converte exceções técnicas em mensagens compreensíveis.
"""

from typing import Tuple
from mysql.connector import Error as MySQLError
import traceback
from src.utils.logger import Logger


class ErrorHandler:
    """Gerenciador de erros com mensagens user-friendly."""
    
    # Mapeamento de erros comuns
    ERROR_MESSAGES = {
        # Erros de conexão
        '2002': 'Não foi possível conectar ao banco de dados. Verifique se o MySQL está rodando.',
        '2003': 'Não foi possível conectar ao banco de dados. Servidor MySQL não encontrado.',
        '1045': 'Erro de autenticação no banco de dados. Verifique usuário e senha.',
        '1049': 'Banco de dados não encontrado. Execute o script de instalação.',
        '2006': 'Conexão com o banco perdida. Tentando reconectar...',
        '2013': 'Tempo limite de conexão excedido. Verifique a rede.',
        
        # Erros de integridade
        '1062': 'Este registro já existe no sistema.',
        '1451': 'Não é possível excluir: existem registros relacionados.',
        '1452': 'Erro de referência: registro relacionado não encontrado.',
        
        # Erros de dados
        '1054': 'Erro na estrutura do banco. Execute as migrações pendentes.',
        '1146': 'Tabela não encontrada. Execute o script de instalação.',
        '1366': 'Valor inválido para este campo.',
        '1406': 'Texto muito longo para este campo.',
    }
    
    @staticmethod
    def handle_exception(error: Exception, context: str = "") -> Tuple[bool, str]:
        """
        Trata uma exceção e retorna mensagem user-friendly.
        
        Args:
            error: Exceção capturada
            context: Contexto da operação (ex: "criar produto")
            
        Returns:
            (sucesso=False, mensagem_usuario)
        """
        # Log completo do erro
        error_trace = traceback.format_exc()
        Logger.error(f"Erro em {context}: {error}")
        Logger.error(f"Stack trace:\n{error_trace}")
        
        # Se for erro do MySQL, tenta mensagem específica
        if isinstance(error, MySQLError):
            error_code = str(error.errno) if hasattr(error, 'errno') else None
            
            if error_code and error_code in ErrorHandler.ERROR_MESSAGES:
                mensagem = ErrorHandler.ERROR_MESSAGES[error_code]
            else:
                mensagem = f"Erro no banco de dados: {str(error)}"
            
            return False, mensagem
        
        # Erros gerais
        mensagem = f"Erro ao {context}: {str(error)}"
        return False, mensagem
    
    @staticmethod
    def log_and_show_error(error: Exception, context: str, show_technical: bool = False) -> str:
        """
        Loga erro e retorna mensagem para mostrar ao usuário.
        
        Args:
            error: Exceção
            context: Contexto
            show_technical: Se deve incluir detalhes técnicos
            
        Returns:
            Mensagem formatada
        """
        _, mensagem = ErrorHandler.handle_exception(error, context)
        
        if show_technical:
            mensagem += f"\n\nDetalhes técnicos: {str(error)}"
        
        return mensagem
    
    @staticmethod
    def safe_execute(func, *args, context="executar operação", **kwargs) -> Tuple[bool, str, any]:
        """
        Executa uma função com tratamento de erros seguro.
        
        Args:
            func: Função a executar
            *args: Argumentos posicionais
            context: Contexto da operação
            **kwargs: Argumentos nomeados
            
        Returns:
            (sucesso, mensagem, resultado)
        """
        try:
            resultado = func(*args, **kwargs)
            return True, "Operação realizada com sucesso", resultado
        except Exception as e:
            sucesso, mensagem = ErrorHandler.handle_exception(e, context)
            return sucesso, mensagem, None
