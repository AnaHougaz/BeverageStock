# BeverageStock

Sistema de gerenciamento de estoque para distribuidoras de bebidas (cervejas e refrigerantes) com cálculos logísticos automáticos.

## O que faz

Calcula automaticamente quando comprar, quanto comprar e quanto manter em estoque usando fórmulas clássicas de gestão de inventário. Evita falta de produto e reduz custos de armazenamento.

## Instalação

```bash
# Clone o repositório
git clone [seu-repo]
cd beverage-stock

# Sem dependências externas - usa apenas biblioteca padrão Python
python beverage_stock.py
```

## Uso rápido

```python
from beverage_stock import Produto, TipoBebida, Estoque, CalculadoraCusto

# Criar produto
skol = Produto(
    nome="Skol Lata 350ml",
    tipo=TipoBebida.CERVEJA,
    custo_manutencao=0.50,  # R$/unidade/mês
    custo_pedido=150.0,      # R$ por pedido
    preco_unitario=2.50
)

# Criar estoque
estoque = Estoque("Minha Distribuidora")
estoque.adicionar_produto(skol)

# Entrada de mercadoria
estoque.entrada_estoque("Skol Lata 350ml", 1000)

# Calcular quando pedir
ponto_pedido = CalculadoraCusto.determinar_ponto_pedido(
    lead_time_dias=5,           # Fornecedor entrega em 5 dias
    demanda_media_diaria=50,    # Vende 50/dia
    estoque_seguranca=70        # Buffer de segurança
)
# Resultado: quando tiver 320 unidades, faça novo pedido

# Calcular quanto pedir
lote = CalculadoraCusto.calcular_lote_economico(
    demanda_anual=18000,        # Vende 18k/ano
    custo_pedido=150.0,
    custo_manutencao=6.0        # R$ 0.50/mês * 12
)
# Resultado: peça 948 unidades por vez

# Verificar alertas
estoque.verificar_alertas(ponto_pedido, "Skol Lata 350ml")
```

## Funcionalidades

### Cálculos automáticos

- **EOQ (Lote Econômico)**: Quantidade ideal para minimizar custos totais
- **Ponto de Pedido**: Quando fazer novo pedido para não faltar produto
- **Estoque de Segurança**: Buffer para lidar com variações de demanda

### Gestão de estoque

- Entrada e saída de mercadorias
- Alertas automáticos quando atingir níveis críticos
- Relatórios de estoque atual
- Suporte para cervejas e refrigerantes

## Estrutura do código

```
beverage_stock.py
├── TipoBebida (Enum)          # CERVEJA ou REFRIGERANTE
├── Produto                     # Define bebida com custos
├── CalculadoraCusto            # Fórmulas logísticas
└── Estoque                     # Gerencia produtos
```

## Documentação técnica

O projeto usa Doxygen para documentação automática do código.

### Gerar documentação

```bash
# Instalar Doxygen
sudo apt install doxygen  # Ubuntu/Debian
brew install doxygen      # macOS

# Gerar docs
doxygen Doxyfile

# Abrir no navegador
open docs/index.html
```

### Configuração (Doxyfile)

- **INPUT**: Diretório atual
- **OUTPUT_DIRECTORY**: docs/
- **EXTRACT_ALL**: Extrai tudo (público e privado)
- **PYTHON_DOCSTRING**: Suporte a docstrings Python
- **CLASS_DIAGRAMS**: Gera diagramas de classe
- **SOURCE_BROWSER**: Inclui código fonte navegável

A documentação é gerada em HTML com:
- Índice de classes e métodos
- Diagramas de colaboração
- Lista de TODOs e bugs
- Código fonte navegável

## Exemplo real

```python
# Cenário: Distribuidora vende 50 Brahmas/dia
# Fornecedor entrega em 5 dias
# Custo de pedido: R$ 150
# Custo de manter em estoque: R$ 0.50/mês

estoque_seguranca = 70  # 7 dias de buffer
ponto_pedido = 320      # (5 dias * 50) + 70
lote_economico = 948    # Quantidade ótima

# Quando estoque chegar em 320, peça 948 unidades
```

## TODOs pendentes

- Otimização de espaço para separar cerveja/refrigerante
- Sistema de notificações por email
- Integração com API de fornecedores

## Requisitos

- Python 3.7+
- Doxygen (apenas para gerar documentação)

## Licença

Livre para uso acadêmico e comercial.

---

**Autor**: Ana Beatriz Alves Hougaz  
**Versão**: 1.0  
**Data**: 2025-10-12
