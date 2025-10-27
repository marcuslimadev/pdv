"""
Serviço de gerenciamento de vendas.
"""

from typing import Optional, List
from decimal import Decimal
from datetime import date

from src.models.venda import Venda, ItemVenda
from src.models.pagamento import Pagamento
from src.models.produto import Produto
from src.dao.venda_dao import VendaDAO, ItemVendaDAO
from src.dao.pagamento_dao import PagamentoDAO
from src.dao.produto_dao import ProdutoDAO
from src.dao.caixa_dao import CaixaDAO
from src.utils.logger import Logger


class VendaService:
    """Serviço para gerenciamento de vendas."""
    
    def __init__(self):
        self.venda_atual: Optional[Venda] = None
    
    def iniciar_nova_venda(self, usuario_id: int, caixa_id: int) -> Venda:
        """
        Inicia uma nova venda.
        
        Args:
            usuario_id: ID do usuário
            caixa_id: ID do caixa
            
        Returns:
            Objeto Venda criado
        """
        numero_venda = VendaDAO.gerar_numero_venda()
        
        self.venda_atual = Venda(
            numero_venda=numero_venda,
            usuario_id=usuario_id,
            caixa_id=caixa_id,
            status=Venda.STATUS_ABERTA
        )
        
        Logger.log_operacao("Sistema", "NOVA VENDA", f"Número: {numero_venda}")
        return self.venda_atual
    
    def adicionar_produto(
        self, 
        produto: Produto, 
        quantidade: Decimal, 
        desconto: Decimal = Decimal('0.00')
    ) -> tuple[bool, str]:
        """
        Adiciona um produto à venda atual.
        
        Args:
            produto: Produto a ser adicionado
            quantidade: Quantidade
            desconto: Desconto no item
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.venda_atual:
            return False, "Nenhuma venda iniciada"
        
        if not produto.ativo:
            return False, "Produto inativo"
        
        if produto.estoque_atual < quantidade:
            return False, f"Estoque insuficiente. Disponível: {produto.estoque_atual}"
        
        # Cria item de venda
        item = ItemVenda(
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=produto.preco_venda,
            desconto=desconto
        )
        
        # Preenche dados auxiliares
        item.produto_nome = produto.nome
        item.produto_codigo_barras = produto.codigo_barras
        
        # Adiciona à venda
        self.venda_atual.adicionar_item(item)
        
        Logger.log_operacao(
            "Sistema", 
            "PRODUTO ADICIONADO", 
            f"{produto.nome} - Qtd: {quantidade}"
        )
        
        return True, "Produto adicionado com sucesso"
    
    def remover_item(self, index: int) -> tuple[bool, str]:
        """
        Remove um item da venda atual.
        
        Args:
            index: Índice do item na lista
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.venda_atual:
            return False, "Nenhuma venda iniciada"
        
        if 0 <= index < len(self.venda_atual.itens):
            item = self.venda_atual.itens[index]
            self.venda_atual.remover_item(index)
            
            Logger.log_operacao(
                "Sistema", 
                "PRODUTO REMOVIDO", 
                f"{item.produto_nome}"
            )
            
            return True, "Item removido com sucesso"
        
        return False, "Índice inválido"
    
    def aplicar_desconto(self, desconto: Decimal) -> tuple[bool, str]:
        """
        Aplica desconto na venda.
        
        Args:
            desconto: Valor do desconto
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.venda_atual:
            return False, "Nenhuma venda iniciada"
        
        if desconto < 0:
            return False, "Desconto não pode ser negativo"
        
        if desconto > self.venda_atual.subtotal:
            return False, "Desconto não pode ser maior que o subtotal"
        
        self.venda_atual.aplicar_desconto(desconto)
        
        Logger.log_operacao(
            "Sistema", 
            "DESCONTO APLICADO", 
            f"R$ {float(desconto):.2f}"
        )
        
        return True, "Desconto aplicado com sucesso"
    
    def finalizar_venda(self, pagamentos: List[Pagamento]) -> tuple[bool, str, Optional[int]]:
        """
        Finaliza a venda atual.
        
        Args:
            pagamentos: Lista de pagamentos da venda
            
        Returns:
            Tupla (sucesso, mensagem, venda_id)
        """
        if not self.venda_atual:
            return False, "Nenhuma venda iniciada", None
        
        if len(self.venda_atual.itens) == 0:
            return False, "Venda sem itens", None
        
        # Valida pagamentos
        total_pago = sum(p.valor for p in pagamentos)
        if total_pago < self.venda_atual.total:
            return False, "Valor pago insuficiente", None
        
        try:
            # Salva a venda
            venda_id = VendaDAO.criar(self.venda_atual)
            if not venda_id:
                return False, "Erro ao salvar venda", None
            
            self.venda_atual.id = venda_id
            
            # Salva os itens
            for item in self.venda_atual.itens:
                item.venda_id = venda_id
                ItemVendaDAO.criar(item)
            
            # Salva os pagamentos
            for pagamento in pagamentos:
                pagamento.venda_id = venda_id
                pagamento.aprovar()  # Marca como aprovado
                PagamentoDAO.criar(pagamento)
            
            # Finaliza a venda
            self.venda_atual.finalizar()
            VendaDAO.atualizar(self.venda_atual)
            
            # Log
            Logger.log_venda(
                self.venda_atual.numero_venda,
                "Sistema",
                float(self.venda_atual.total)
            )
            
            # Limpa venda atual
            numero_venda = self.venda_atual.numero_venda
            self.venda_atual = None
            
            return True, f"Venda {numero_venda} finalizada com sucesso!", venda_id
        
        except Exception as e:
            Logger.log_erro("FINALIZAR VENDA", e)
            return False, f"Erro ao finalizar venda: {str(e)}", None
    
    def cancelar_venda(self) -> tuple[bool, str]:
        """
        Cancela a venda atual.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.venda_atual:
            return False, "Nenhuma venda iniciada"
        
        numero_venda = self.venda_atual.numero_venda
        self.venda_atual = None
        
        Logger.log_operacao("Sistema", "VENDA CANCELADA", f"Número: {numero_venda}")
        
        return True, "Venda cancelada"
    
    def get_venda_atual(self) -> Optional[Venda]:
        """Retorna a venda atual."""
        return self.venda_atual
    
    def tem_venda_aberta(self) -> bool:
        """Verifica se há uma venda aberta."""
        return self.venda_atual is not None
    
    @staticmethod
    def buscar_venda(venda_id: int) -> Optional[Venda]:
        """Busca uma venda por ID."""
        return VendaDAO.buscar_por_id(venda_id)
    
    @staticmethod
    def buscar_vendas_periodo(data_inicio: date, data_fim: date) -> List[Venda]:
        """Busca vendas por período."""
        return VendaDAO.buscar_por_periodo(data_inicio, data_fim, Venda.STATUS_FINALIZADA)
    
    @staticmethod
    def buscar_vendas_caixa(caixa_id: int) -> List[Venda]:
        """Busca vendas de um caixa."""
        return VendaDAO.buscar_por_caixa(caixa_id)
    
    @staticmethod
    def obter_total_vendas_dia(data: date = None) -> float:
        """Obtém o total de vendas do dia."""
        return VendaDAO.obter_total_vendas_dia(data)
