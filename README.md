# Assistente Inteligente de Suporte e Vendas

Projeto prático desenvolvido para estudar e aplicar na prática a integração entre **Large Language Models (LLMs)**, **Tool Calling**, **FastAPI** e bancos de dados relacionais (**SQLite**).

## O que este projeto faz

A aplicação cria uma API simples (`POST /perguntar`) onde um agente de IA recebe perguntas em linguagem natural sobre clientes e pedidos, decide qual função Python acionar para consultar o banco de dados de forma segura e formula uma resposta amigável com base nos dados reais.

## Estrutura do Projeto

- `database.py`: Criação das tabelas (`clientes` e `pedidos`), dados fictícios e consultas SQL parametrizadas (`JOIN` e agregações).
- `schemas.py`: Validação dos dados de entrada e saída da API usando Pydantic.
- `tools.py`: Funções Python documentadas que servem como ferramentas para o modelo de IA consultar o banco.
- `main.py`: Configuração da API REST com FastAPI e orquestração das chamadas ao LLM.
