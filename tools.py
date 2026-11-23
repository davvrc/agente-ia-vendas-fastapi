from typing import Any
from database import (
    buscar_pedidos_por_cliente,
    resumo_financeiro_clientes,
    listar_pedidos_por_status,
)
from schemas import StatusPedido


def consultar_pedidos_cliente(nome_cliente: str) -> list[dict[str, Any]]:
    """
    Busca o histórico de pedidos de um cliente específico pelo nome (aceita nome parcial).
    Use esta ferramenta quando o usuário perguntar sobre compras, produtos ou status de pedidos de uma pessoa.

    Args:
        nome_cliente: Nome completo ou primeiro nome do cliente (ex: 'João', 'Maria Oliveira').
    """
    resultados = buscar_pedidos_por_cliente(nome_cliente)
    if not resultados:
        return [{"mensagem": f"Nenhum pedido encontrado para o cliente '{nome_cliente}'."}]
    return resultados


def obter_ranking_financeiro_clientes() -> list[dict[str, Any]]:
    """
    Retorna o resumo financeiro de todos os clientes, incluindo total de pedidos válidos
    e o valor total gasto por cada um (desconsiderando pedidos cancelados), ordenado do maior para o menor.
    Use esta ferramenta para perguntas sobre faturamento, cliente que mais gastou, ranking de vendas ou visão geral.
    """
    return resumo_financeiro_clientes()


def consultar_pedidos_por_status(status: StatusPedido) -> list[dict[str, Any]]:
    """
    Filtra e lista todos os pedidos que estão em um determinado status de entrega/processamento.
    Use esta ferramenta quando o usuário perguntar quais pedidos estão pendentes, em transporte, entregues ou cancelados.

    Args:
        status: O status exato do pedido. Deve ser um dos valores permitidos:
                'Processando', 'Em transporte', 'Entregue' ou 'Cancelado'.
    """
    valor_status = status.value if isinstance(status, StatusPedido) else status
    return listar_pedidos_por_status(valor_status)


FERRAMENTAS_AGENTE = [
    consultar_pedidos_cliente,
    obter_ranking_financeiro_clientes,
    consultar_pedidos_por_status,
]