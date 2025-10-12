"""
@file beverage_stock.py
@brief Sistema de gerenciamento de estoque para cervejas e refrigerantes
@author Ana Beatriz Alves Hougaz
@date 2025-10-12
"""

from enum import Enum
from typing import List
import math


class TipoBebida(Enum):
    """
    @enum TipoBebida
    @brief Tipos de bebidas suportados pelo sistema
    """
    CERVEJA = 1  ##< Produtos do tipo cerveja
    REFRIGERANTE = 2  ##< Produtos do tipo refrigerante


class Produto:
    """
    @class Produto
    @brief Define uma bebida (cerveja ou refrigerante) com seus dados de custo
    
    Essa classe é usada como base para todos os cálculos de estoque e pedido.
    Contém informações sobre custos logísticos e características do produto.
    """
    
    def __init__(self, nome: str, tipo: TipoBebida, custo_manutencao: float, 
                 custo_pedido: float, preco_unitario: float):
        """
        @brief Construtor da classe Produto
        
        @param nome Nome do produto (ex: "Brahma Lata 350ml")
        @param tipo Tipo da bebida (CERVEJA ou REFRIGERANTE)
        @param custo_manutencao Custo de manutenção por unidade/mês em BRL
        @param custo_pedido Custo fixo por pedido em BRL
        @param preco_unitario Preço de compra unitário em BRL
        """
        self.nome = nome  ##< Nome comercial do produto
        
        ## @brief Define se o produto é cerveja ou refrigerante
        self.tipo = tipo
        
        ## @brief Custo de Manutenção (Holding Cost) por unidade/mês (em BRL)
        ## 
        ## Inclui custos de refrigeração, armazenagem e seguro
        self.custo_manutencao = custo_manutencao
        
        ## @brief Custo Fixo por Pedido (Ordering Cost) (em BRL)
        ##
        ## O custo logístico de fazer um novo pedido, independente da quantidade
        self.custo_pedido = custo_pedido
        
        ## @brief Preço unitário de compra do produto
        self.preco_unitario = preco_unitario
        
        ## @brief Quantidade atual em estoque
        self.quantidade_estoque = 0
    
    def __str__(self) -> str:
        """
        @brief Representação em string do produto
        @return String formatada com informações do produto
        """
        return f"{self.nome} ({self.tipo.name}) - Estoque: {self.quantidade_estoque}"


class CalculadoraCusto:
    """
    @class CalculadoraCusto
    @brief Responsável pelos cálculos de logística e gestão de estoque
    
    Implementa fórmulas clássicas de gestão de inventário como EOQ 
    (Economic Order Quantity) e cálculos de estoque de segurança.
    """
    
    @staticmethod
    def calcular_estoque_seguranca(desvio_padrao: float, dias_seguranca: int, 
                                   demanda_media_diaria: float) -> int:
        """
        @brief Calcula a quantidade ideal de Estoque de Segurança
        
        Baseado na fórmula: Fator de Serviço × Desvio Padrão × √(Lead Time)
        
        @param desvio_padrao Variação na demanda ou no prazo de entrega
        @param dias_seguranca Fator de serviço em dias (Ex: 7 dias)
        @param demanda_media_diaria Consumo médio diário do produto
        @return A quantidade mínima que deve estar sempre em estoque
        
        @note Um valor típico de dias_seguranca é 7 para produtos de alta rotação
        """
        estoque_seguranca = desvio_padrao * dias_seguranca * demanda_media_diaria
        return math.ceil(estoque_seguranca)
    
    @staticmethod
    def determinar_ponto_pedido(lead_time_dias: int, demanda_media_diaria: float, 
                               estoque_seguranca: int) -> int:
        """
        @brief Determina o Ponto de Pedido (Reorder Point - ROP)
        
        Indica quando um novo pedido deve ser feito para evitar a falta de estoque.
        Fórmula: ROP = (Lead Time × Demanda Média) + Estoque de Segurança
        
        @param lead_time_dias O tempo de entrega do fornecedor em dias
        @param demanda_media_diaria O consumo médio diário do produto
        @param estoque_seguranca O valor mínimo calculado
        @return A quantidade total que deve acionar o novo pedido
        
        @warning Se o estoque atual cair abaixo deste valor, faça um pedido imediatamente!
        """
        ponto_pedido = (lead_time_dias * demanda_media_diaria) + estoque_seguranca
        return math.ceil(ponto_pedido)
    
    @staticmethod
    def calcular_lote_economico(demanda_anual: float, custo_pedido: float, 
                               custo_manutencao: float) -> int:
        """
        @brief Calcula o Lote Econômico de Compra (EOQ - Economic Order Quantity)
        
        Determina a quantidade ideal a ser pedida que minimiza o custo total
        de estoque (custos de pedido + custos de manutenção).
        
        Fórmula EOQ: √((2 × Demanda Anual × Custo por Pedido) / Custo de Manutenção)
        
        @param demanda_anual Demanda total prevista para o ano
        @param custo_pedido Custo fixo de fazer um pedido
        @param custo_manutencao Custo de manter uma unidade em estoque por ano
        @return A quantidade ótima a ser pedida
        
        @see https://en.wikipedia.org/wiki/Economic_order_quantity
        """
        if custo_manutencao == 0:
            raise ValueError("Custo de manutenção não pode ser zero")
        
        eoq = math.sqrt((2 * demanda_anual * custo_pedido) / custo_manutencao)
        return math.ceil(eoq)


class Estoque:
    """
    @class Estoque
    @brief Gerencia a lista de Produtos e monitora os níveis
    
    Centraliza o controle de entrada e saída de produtos, além de 
    fornecer alertas quando os níveis críticos são atingidos.
    
    @todo Implementar a lógica de otimização de espaço para separar cerveja e refrigerante
    @todo Adicionar sistema de notificações por email quando atingir ponto de pedido
    """
    
    def __init__(self, nome_estoque: str = "Estoque Principal"):
        """
        @brief Construtor do Estoque
        @param nome_estoque Nome identificador do estoque
        """
        self.nome = nome_estoque  ##< Nome do estoque
        self.produtos: List[Produto] = []  ##< Lista de produtos gerenciados
        self.calculadora = CalculadoraCusto()  ##< Instância da calculadora de custos
    
    def adicionar_produto(self, produto: Produto) -> None:
        """
        @brief Adiciona um novo produto ao estoque
        @param produto Instância de Produto a ser adicionada
        """
        self.produtos.append(produto)
        print(f"✓ Produto '{produto.nome}' adicionado ao estoque")
    
    def entrada_estoque(self, nome_produto: str, quantidade: int) -> None:
        """
        @brief Registra entrada de mercadorias no estoque
        
        @param nome_produto Nome do produto para identificação
        @param quantidade Quantidade de unidades que entraram
        @throws ValueError Se o produto não for encontrado
        """
        produto = self._buscar_produto(nome_produto)
        if produto:
            produto.quantidade_estoque += quantidade
            print(f"✓ Entrada: +{quantidade} unidades de '{nome_produto}'")
        else:
            raise ValueError(f"Produto '{nome_produto}' não encontrado")
    
    def saida_estoque(self, nome_produto: str, quantidade: int) -> None:
        """
        @brief Registra saída de mercadorias do estoque
        
        @param nome_produto Nome do produto para identificação
        @param quantidade Quantidade de unidades que saíram
        @throws ValueError Se não houver estoque suficiente
        """
        produto = self._buscar_produto(nome_produto)
        if produto:
            if produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
                print(f"✓ Saída: -{quantidade} unidades de '{nome_produto}'")
            else:
                raise ValueError(f"Estoque insuficiente! Disponível: {produto.quantidade_estoque}")
        else:
            raise ValueError(f"Produto '{nome_produto}' não encontrado")
    
    def verificar_alertas(self, ponto_pedido: int, nome_produto: str) -> bool:
        """
        @brief Verifica se algum produto atingiu o ponto de pedido
        
        @param ponto_pedido Nível crítico de estoque
        @param nome_produto Nome do produto a verificar
        @return True se deve fazer pedido, False caso contrário
        """
        produto = self._buscar_produto(nome_produto)
        if produto:
            if produto.quantidade_estoque <= ponto_pedido:
                print(f"⚠️  ALERTA: '{nome_produto}' atingiu ponto de pedido!")
                return True
        return False
    
    def relatorio_estoque(self) -> None:
        """
        @brief Gera relatório completo do estoque atual
        
        Exibe todos os produtos cadastrados com suas quantidades atuais
        """
        print(f"\n{'='*60}")
        print(f"RELATÓRIO DE ESTOQUE: {self.nome}")
        print(f"{'='*60}")
        
        if not self.produtos:
            print("Nenhum produto cadastrado.")
            return
        
        for produto in self.produtos:
            print(f"• {produto}")
        print(f"{'='*60}\n")
    
    def _buscar_produto(self, nome: str) -> Produto:
        """
        @brief Método auxiliar para buscar produto por nome
        @param nome Nome do produto
        @return Instância do Produto ou None
        @private
        """
        for produto in self.produtos:
            if produto.nome == nome:
                return produto
        return None


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    """
    @brief Exemplo de uso da biblioteca BeverageStock
    
    Demonstra a criação de produtos, cálculos logísticos e gestão de estoque
    """
    
    # Criar produtos
    brahma = Produto(
        nome="Brahma Lata 350ml",
        tipo=TipoBebida.CERVEJA,
        custo_manutencao=0.50,  # R$ 0,50/unidade/mês
        custo_pedido=150.0,     # R$ 150 por pedido
        preco_unitario=2.50
    )
    
    coca_cola = Produto(
        nome="Coca-Cola 2L",
        tipo=TipoBebida.REFRIGERANTE,
        custo_manutencao=0.30,
        custo_pedido=120.0,
        preco_unitario=5.00
    )
    
    # Criar estoque e adicionar produtos
    estoque_principal = Estoque("Distribuidora Salvador")
    estoque_principal.adicionar_produto(brahma)
    estoque_principal.adicionar_produto(coca_cola)
    
    # Simular entrada de mercadorias
    estoque_principal.entrada_estoque("Brahma Lata 350ml", 500)
    estoque_principal.entrada_estoque("Coca-Cola 2L", 300)
    
    # Calcular parâmetros logísticos para Brahma
    print("\n--- CÁLCULOS LOGÍSTICOS: Brahma ---")
    
    estoque_seguranca = CalculadoraCusto.calcular_estoque_seguranca(
        desvio_padrao=0.2,
        dias_seguranca=7,
        demanda_media_diaria=50
    )
    print(f"Estoque de Segurança: {estoque_seguranca} unidades")
    
    ponto_pedido = CalculadoraCusto.determinar_ponto_pedido(
        lead_time_dias=5,
        demanda_media_diaria=50,
        estoque_seguranca=estoque_seguranca
    )
    print(f"Ponto de Pedido: {ponto_pedido} unidades")
    
    lote_economico = CalculadoraCusto.calcular_lote_economico(
        demanda_anual=18000,
        custo_pedido=brahma.custo_pedido,
        custo_manutencao=brahma.custo_manutencao * 12
    )
    print(f"Lote Econômico de Compra: {lote_economico} unidades")
    
    # Simular vendas
    print("\n--- SIMULAÇÃO DE VENDAS ---")
    estoque_principal.saida_estoque("Brahma Lata 350ml", 250)
    estoque_principal.saida_estoque("Brahma Lata 350ml", 180)
    
    # Verificar alertas
    estoque_principal.verificar_alertas(ponto_pedido, "Brahma Lata 350ml")
    
    # Relatório final
    estoque_principal.relatorio_estoque()