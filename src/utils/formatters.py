"""
Utilitários para formatação de dados.
"""

from decimal import Decimal
from datetime import datetime, date


class Formatters:
    """Classe com métodos de formatação."""
    
    @staticmethod
    def formatar_moeda(valor: float | Decimal) -> str:
        """
        Formata valor monetário para exibição.
        
        Args:
            valor: Valor a ser formatado
            
        Returns:
            String formatada (ex: "R$ 10,50")
        """
        if isinstance(valor, Decimal):
            valor = float(valor)
        
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def formatar_quantidade(quantidade: float | Decimal, decimais: int = 3) -> str:
        """
        Formata quantidade para exibição.
        
        Args:
            quantidade: Quantidade a ser formatada
            decimais: Número de casas decimais
            
        Returns:
            String formatada
        """
        if isinstance(quantidade, Decimal):
            quantidade = float(quantidade)
        
        formato = f"{{:,.{decimais}f}}"
        return formato.format(quantidade).replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def formatar_data(data: datetime | date, formato: str = "%d/%m/%Y") -> str:
        """
        Formata data para exibição.
        
        Args:
            data: Data a ser formatada
            formato: Formato de saída
            
        Returns:
            String formatada
        """
        if data is None:
            return ""
        
        return data.strftime(formato)
    
    @staticmethod
    def formatar_data_hora(data_hora: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
        """
        Formata data e hora para exibição.
        
        Args:
            data_hora: Data/hora a ser formatada
            formato: Formato de saída
            
        Returns:
            String formatada
        """
        if data_hora is None:
            return ""
        
        return data_hora.strftime(formato)
    
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """
        Formata CPF para exibição.
        
        Args:
            cpf: CPF (apenas números)
            
        Returns:
            String formatada (ex: "123.456.789-01")
        """
        if not cpf or len(cpf) != 11:
            return cpf
        
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """
        Formata CNPJ para exibição.
        
        Args:
            cnpj: CNPJ (apenas números)
            
        Returns:
            String formatada (ex: "12.345.678/0001-90")
        """
        if not cnpj or len(cnpj) != 14:
            return cnpj
        
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    @staticmethod
    def formatar_telefone(telefone: str) -> str:
        """
        Formata telefone para exibição.
        
        Args:
            telefone: Telefone (apenas números)
            
        Returns:
            String formatada
        """
        if not telefone:
            return telefone
        
        telefone = ''.join(filter(str.isdigit, telefone))
        
        if len(telefone) == 11:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        elif len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        
        return telefone
    
    @staticmethod
    def formatar_codigo_barras(codigo: str) -> str:
        """
        Formata código de barras para exibição.
        
        Args:
            codigo: Código de barras
            
        Returns:
            String formatada
        """
        if not codigo:
            return ""
        
        # Para EAN-13 (13 dígitos)
        if len(codigo) == 13:
            return f"{codigo[:1]} {codigo[1:7]} {codigo[7:13]}"
        
        return codigo
    
    @staticmethod
    def remover_formatacao(texto: str) -> str:
        """
        Remove formatação de um texto, deixando apenas números.
        
        Args:
            texto: Texto formatado
            
        Returns:
            String apenas com números
        """
        if not texto:
            return ""
        
        return ''.join(filter(str.isdigit, texto))
    
    @staticmethod
    def truncar_texto(texto: str, tamanho: int = 50) -> str:
        """
        Trunca texto adicionando reticências se necessário.
        
        Args:
            texto: Texto a ser truncado
            tamanho: Tamanho máximo
            
        Returns:
            Texto truncado
        """
        if not texto or len(texto) <= tamanho:
            return texto
        
        return texto[:tamanho - 3] + "..."
    
    @staticmethod
    def formatar_percentual(valor: float | Decimal, decimais: int = 2) -> str:
        """
        Formata valor percentual.
        
        Args:
            valor: Valor percentual
            decimais: Número de casas decimais
            
        Returns:
            String formatada (ex: "10,50%")
        """
        if isinstance(valor, Decimal):
            valor = float(valor)
        
        formato = f"{{:.{decimais}f}}"
        return formato.format(valor).replace('.', ',') + "%"
