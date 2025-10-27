"""
Utilitários para validação de dados.
"""

import re
from decimal import Decimal, InvalidOperation


class Validators:
    """Classe com métodos de validação."""
    
    @staticmethod
    def validar_codigo_barras(codigo: str) -> bool:
        """
        Valida código de barras (EAN-13 ou similar).
        
        Args:
            codigo: Código de barras
            
        Returns:
            True se válido
        """
        if not codigo:
            return False
        
        # Remove espaços e caracteres especiais
        codigo = re.sub(r'[^0-9]', '', codigo)
        
        # Verifica se tem entre 8 e 14 dígitos
        return 8 <= len(codigo) <= 14
    
    @staticmethod
    def validar_preco(preco: str) -> tuple[bool, Decimal]:
        """
        Valida e converte preço.
        
        Args:
            preco: Preço como string
            
        Returns:
            Tupla (válido, valor_decimal)
        """
        try:
            valor = Decimal(preco.replace(',', '.'))
            if valor < 0:
                return False, Decimal('0')
            return True, valor
        except (InvalidOperation, ValueError, AttributeError):
            return False, Decimal('0')
    
    @staticmethod
    def validar_quantidade(quantidade: str) -> tuple[bool, Decimal]:
        """
        Valida e converte quantidade.
        
        Args:
            quantidade: Quantidade como string
            
        Returns:
            Tupla (válido, valor_decimal)
        """
        try:
            valor = Decimal(quantidade.replace(',', '.'))
            if valor <= 0:
                return False, Decimal('0')
            return True, valor
        except (InvalidOperation, ValueError, AttributeError):
            return False, Decimal('0')
    
    @staticmethod
    def validar_username(username: str) -> tuple[bool, str]:
        """
        Valida username.
        
        Args:
            username: Nome de usuário
            
        Returns:
            Tupla (válido, mensagem_erro)
        """
        if not username:
            return False, "Username não pode ser vazio"
        
        if len(username) < 3:
            return False, "Username deve ter no mínimo 3 caracteres"
        
        if len(username) > 50:
            return False, "Username deve ter no máximo 50 caracteres"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username deve conter apenas letras, números e underscore"
        
        return True, ""
    
    @staticmethod
    def validar_senha(senha: str) -> tuple[bool, str]:
        """
        Valida senha.
        
        Args:
            senha: Senha
            
        Returns:
            Tupla (válido, mensagem_erro)
        """
        if not senha:
            return False, "Senha não pode ser vazia"
        
        if len(senha) < 6:
            return False, "Senha deve ter no mínimo 6 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida formato de email.
        
        Args:
            email: Endereço de email
            
        Returns:
            True se válido
        """
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """
        Valida CPF (formato básico).
        
        Args:
            cpf: CPF
            
        Returns:
            True se válido
        """
        if not cpf:
            return False
        
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não é uma sequência de dígitos iguais
        if cpf == cpf[0] * 11:
            return False
        
        return True
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """
        Valida CNPJ (formato básico).
        
        Args:
            cnpj: CNPJ
            
        Returns:
            True se válido
        """
        if not cnpj:
            return False
        
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verifica se não é uma sequência de dígitos iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        return True
