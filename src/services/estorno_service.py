"""
Service para operações de estorno de vendas.
Gerencia reversão de estoque e validações.
"""

from typing import Tuple, Optional
from decimal import Decimal
from src.models.estorno import Estorno
from src.models.venda import Venda
from src.dao.estorno_dao import EstornoDAO
from src.dao.venda_dao import VendaDAO
from src.dao.produto_dao import ProdutoDAO
from src.utils.logger import Logger


class EstornoService:
    """Service para processar estornos de vendas."""
    
    @staticmethod
    def validar_estorno(venda_id: int) -> Tuple[bool, str, Optional[Venda]]:
        """
        Valida se uma venda pode ser estornada.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            (sucesso, mensagem, venda)
        """
        # Busca a venda
        venda = VendaDAO.buscar_por_id(venda_id)
        if not venda:
            return False, "Venda não encontrada!", None
        
        # Verifica se está finalizada
        if venda.status != Venda.STATUS_FINALIZADA:
            return False, "Apenas vendas finalizadas podem ser estornadas!", None
        
        # Verifica se já foi estornada
        if EstornoDAO.verificar_venda_estornada(venda_id):
            return False, "Esta venda já foi estornada!", None
        
        return True, "Venda pode ser estornada", venda
    
    @staticmethod
    def processar_estorno(venda_id: int, usuario_id: int, motivo: str, 
                          observacoes: Optional[str] = None) -> Tuple[bool, str]:
        """
        Processa o estorno de uma venda.
        
        Args:
            venda_id: ID da venda
            usuario_id: ID do usuário admin que autorizou
            motivo: Motivo do estorno
            observacoes: Observações adicionais
            
        Returns:
            (sucesso, mensagem)
        """
        try:
            # Valida estorno
            sucesso, mensagem, venda = EstornoService.validar_estorno(venda_id)
            if not sucesso:
                return False, mensagem
            
            # Busca itens da venda
            itens = VendaDAO.buscar_itens_venda(venda_id)
            if not itens:
                return False, "Venda sem itens!"
            
            # Cria registro de estorno
            estorno = Estorno(
                venda_id=venda_id,
                usuario_id=usuario_id,
                motivo=motivo,
                valor_estornado=venda.total,
                observacoes=observacoes
            )
            
            estorno_id = EstornoDAO.criar(estorno)
            if not estorno_id:
                return False, "Erro ao criar registro de estorno!"
            
            # Reverte estoque de cada item
            for item in itens:
                produto = ProdutoDAO.buscar_por_id(item.produto_id)
                if produto:
                    novo_estoque = produto.estoque_atual + item.quantidade
                    ProdutoDAO.atualizar_estoque(item.produto_id, novo_estoque)
                    
                    Logger.info(
                        f"Estoque revertido: Produto {produto.nome} - "
                        f"Quantidade: +{item.quantidade} - "
                        f"Estoque: {produto.estoque_atual} -> {novo_estoque}"
                    )
            
            # Atualiza status da venda para cancelada
            VendaDAO.cancelar_venda(venda_id)
            
            # Log do estorno
            Logger.warning(
                f"ESTORNO PROCESSADO - Venda #{venda.numero_venda} - "
                f"Valor: R$ {venda.total:.2f} - "
                f"Motivo: {motivo} - "
                f"Admin ID: {usuario_id} - "
                f"Estorno ID: {estorno_id}"
            )
            
            return True, f"Estorno processado com sucesso! (ID: {estorno_id})"
            
        except Exception as e:
            Logger.error(f"Erro ao processar estorno: {e}")
            return False, f"Erro ao processar estorno: {str(e)}"
    
    @staticmethod
    def obter_detalhes_venda_para_estorno(venda_id: int) -> Optional[dict]:
        """
        Obtém detalhes da venda para exibir antes do estorno.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            dict com informações da venda ou None
        """
        venda = VendaDAO.buscar_por_id(venda_id)
        if not venda:
            return None
        
        itens = VendaDAO.buscar_itens_venda(venda_id)
        
        return {
            'venda': venda,
            'itens': itens,
            'total_itens': len(itens),
            'pode_estornar': not EstornoDAO.verificar_venda_estornada(venda_id)
        }
