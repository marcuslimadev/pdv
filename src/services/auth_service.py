"""
Serviço de autenticação e gerenciamento de sessão.
"""

from typing import Optional
from src.dao.usuario_dao import UsuarioDAO
from src.models.usuario import Usuario
from src.utils.logger import Logger


class AuthService:
    """Serviço de autenticação."""
    
    _instance = None
    _usuario_logado: Optional[Usuario] = None
    
    def __new__(cls):
        """Implementação Singleton."""
        if cls._instance is None:
            cls._instance = super(AuthService, cls).__new__(cls)
        return cls._instance
    
    def login(self, username: str, senha: str) -> tuple[bool, str, Optional[Usuario]]:
        """
        Realiza o login do usuário.
        
        Args:
            username: Nome de usuário
            senha: Senha
            
        Returns:
            Tupla (sucesso, mensagem, usuario)
        """
        try:
            usuario = UsuarioDAO.autenticar(username, senha)
            
            if usuario:
                self._usuario_logado = usuario
                Logger.log_operacao(usuario.nome_completo, "LOGIN", f"Tipo: {usuario.tipo}")
                return True, "Login realizado com sucesso!", usuario
            else:
                Logger.log_operacao(username, "LOGIN FALHOU", "Credenciais inválidas")
                return False, "Usuário ou senha incorretos!", None
        
        except Exception as e:
            Logger.log_erro("LOGIN", e)
            return False, f"Erro ao realizar login: {str(e)}", None
    
    def logout(self):
        """Realiza o logout do usuário."""
        if self._usuario_logado:
            Logger.log_operacao(
                self._usuario_logado.nome_completo, 
                "LOGOUT", 
                f"ID: {self._usuario_logado.id}"
            )
            self._usuario_logado = None
    
    def get_usuario_logado(self) -> Optional[Usuario]:
        """Retorna o usuário logado."""
        return self._usuario_logado
    
    def is_logged_in(self) -> bool:
        """Verifica se há um usuário logado."""
        return self._usuario_logado is not None
    
    def is_admin(self) -> bool:
        """Verifica se o usuário logado é administrador."""
        return self._usuario_logado and self._usuario_logado.is_admin()
    
    def is_operador(self) -> bool:
        """Verifica se o usuário logado é operador."""
        return self._usuario_logado and self._usuario_logado.is_operador()
    
    def verificar_permissao(self, tipo_requerido: str) -> bool:
        """
        Verifica se o usuário tem a permissão necessária.
        
        Args:
            tipo_requerido: Tipo de usuário requerido ('admin' ou 'operador')
            
        Returns:
            True se tem permissão
        """
        if not self.is_logged_in():
            return False
        
        if tipo_requerido == Usuario.TIPO_ADMIN:
            return self.is_admin()
        elif tipo_requerido == Usuario.TIPO_OPERADOR:
            return self.is_operador() or self.is_admin()
        
        return False


# Instância global do serviço de autenticação
auth_service = AuthService()
