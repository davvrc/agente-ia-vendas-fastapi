from enum import Enum
from pydantic import BaseModel, Field


class StatusPedido(str, Enum):
    PROCESSANDO = "Processando"
    EM_TRANSPORTE = "Em transporte"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"

from enum import Enum
from pydantic import BaseModel, Field


class StatusPedido(str, Enum):
    """Define os únicos status válidos para um pedido no sistema."""
    PROCESSANDO = "Processando"
    EM_TRANSPORTE = "Em transporte"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"


class PerguntaRequest(BaseModel):
    """Contrato de entrada: o que o usuário envia para o Agente de IA."""
    pergunta: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Pergunta em linguagem natural sobre clientes ou pedidos.",
        examples=["Quais pedidos o João Silva já fez e qual o valor total?"],
    )


class RespostaAgente(BaseModel):
    """Contrato de saída: o que a API devolve após o Agente processar."""
    pergunta: str
    resposta: str


class NovoPedidoRequest(BaseModel):
    """Contrato de entrada para criar um pedido via rota tradicional da API."""
    cliente_id: int = Field(..., gt=0, description="ID válido do cliente no banco.")
    produto: str = Field(..., min_length=2, description="Nome do produto.")
    valor: float = Field(..., gt=0, description="Valor do pedido (deve ser maior que zero).")