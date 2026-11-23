from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from database import init_db
from agent import perguntar_ao_agente
from schemas import PerguntaRequest, RespostaAgente  

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Assistente Inteligente de Suporte e Vendas",
    description="API de Agente de IA conectado a banco de dados SQLite via Function Calling.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Monitoramento"])
def health_check():
    """Verifica se a API está online."""
    return {"status": "online"}


@app.post("/perguntar", response_model=RespostaAgente, tags=["Agente IA"])
def consultar_agente(payload: PerguntaRequest):
    """Recebe uma pergunta, aciona o Agente com acesso ao SQLite e retorna a resposta."""
    try:
        resposta_agente = perguntar_ao_agente(payload.pergunta)
        return RespostaAgente(
            pergunta=payload.pergunta,
            resposta=resposta_agente,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao processar requisição com o agente: {str(e)}",
        )