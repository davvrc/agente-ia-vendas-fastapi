import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import FERRAMENTAS_AGENTE

load_dotenv()
client = genai.Client()

SYSTEM_INSTRUCTION = """
Você é um assistente analítico de vendas e atendimento ao cliente.
Sua função é responder perguntas sobre clientes, pedidos e faturamento consultando exclusivamente o banco de dados por meio das ferramentas disponíveis.

Regras obrigatórias:
1. NUNCA invente clientes, produtos, valores ou status de pedidos.
2. Sempre utilize as ferramentas disponíveis antes de responder a perguntas sobre dados do sistema.
3. Se a ferramenta retornar que nenhum registro foi encontrado, informe isso claramente ao usuário.
4. Formate valores monetários em Reais (R$) e seja objetivo, claro e profissional na resposta.
"""


def perguntar_ao_agente(pergunta: str) -> str:
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("A variável de ambiente GEMINI_API_KEY não está configurada.")

    # Cria uma sessão de chat isolada (padrão recomendado pelo SDK para Automatic Function Calling)
    chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=FERRAMENTAS_AGENTE,
            temperature=0.1,
        ),
    )

    response = chat.send_message(pergunta)
    return response.text or "Não foi possível gerar uma resposta no momento."


if __name__ == "__main__":
    from database import init_db

    init_db()

    perguntas_teste = [
        "Quais pedidos o João Silva já fez e qual foi o valor total?",
        "Quem é o cliente que mais gastou até agora (desconsiderando cancelados)?",
        "Existe algum pedido em transporte no momento? Para quem?",
    ]

    for p in perguntas_teste:
        print(f"\nPergunta: {p}")
        resposta = perguntar_ao_agente(p)
        print(f"Agente: {resposta}")
        print("-" * 60)
