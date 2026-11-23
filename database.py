import sqlite3
from pathlib import Path
from schemas import StatusPedido
from typing import Any

DB_PATH = Path(__file__).parent / "vendas.db"


def get_connection() -> sqlite3.Connection:  
    conn = sqlite3.connect(DB_PATH)
    
    # Faz cada linha retornada se comportar como um dicionário (acesso pelo nome da coluna)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    
    return conn

def init_db() -> None:
    """Cria as tabelas caso não existam e insere dados iniciais de teste."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cidade TEXT NOT NULL
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                produto TEXT NOT NULL,
                valor REAL NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('Processando', 'Em transporte', 'Entregue', 'Cancelado')),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );
        """)

        # 3. Verifica se já existem clientes para não duplicar os dados de teste
        total_clientes = conn.execute("SELECT COUNT(*) FROM clientes;").fetchone()[0]

        if total_clientes == 0:
            clientes_iniciais = [
                ("João Silva", "joao.silva@email.com", "Vitória"),
                ("Maria Oliveira", "maria.oliveira@email.com", "Vila Velha"),
                ("Carlos Santos", "carlos.santos@email.com", "Serra"),
            ]
            conn.executemany(
                "INSERT INTO clientes (nome, email, cidade) VALUES (?, ?, ?);",
                clientes_iniciais,
            )

            pedidos_iniciais = [
                (1, "Notebook Dell Inspiron", 4200.00, "Entregue"),
                (1, "Mouse sem fio Logitech", 150.00, "Entregue"),
                (2, "Monitor LG 27 polegadas", 1350.00, "Em transporte"),
                (2, "Teclado Mecânico Keychron", 580.00, "Processando"),
                (3, "Headset HyperX Cloud", 420.00, "Cancelado"),
            ]
            conn.executemany(
                "INSERT INTO pedidos (cliente_id, produto, valor, status) VALUES (?, ?, ?, ?);",
                pedidos_iniciais,
            )

    from typing import Any

def buscar_pedidos_por_cliente(nome_cliente: str) -> list[dict[str, Any]]:
    query = """
        SELECT 
            c.nome AS cliente,
            c.cidade,
            p.id AS pedido_id,
            p.produto,
            p.valor,
            p.status
        FROM pedidos p
        INNER JOIN clientes c ON p.cliente_id = c.id
        WHERE c.nome LIKE ?
        ORDER BY p.id DESC;
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (f"%{nome_cliente}%",))
        return [dict(row) for row in cursor.fetchall()]


def resumo_financeiro_clientes() -> list[dict[str, Any]]:
    """Agrega total de pedidos e valor gasto por cliente, desconsiderando cancelados."""
    
    query = """
        SELECT 
            c.id AS cliente_id,
            c.nome AS cliente,
            c.cidade,
            COUNT(p.id) AS total_pedidos,
            COALESCE(SUM(p.valor), 0.0) AS valor_total_gasto
        FROM clientes c
        LEFT JOIN pedidos p 
            ON c.id = p.cliente_id AND p.status != 'Cancelado'
        GROUP BY c.id, c.nome, c.cidade
        ORDER BY valor_total_gasto DESC;
    """
    with get_connection() as conn:
        cursor = conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]


def listar_pedidos_por_status(status: str) -> list[dict[str, Any]]:
    """Lista pedidos filtrados por um status específico com dados do cliente."""
    query = """
        SELECT 
            p.id AS pedido_id,
            c.nome AS cliente,
            c.cidade,
            p.produto,
            p.valor,
            p.status
        FROM pedidos p
        INNER JOIN clientes c ON p.cliente_id = c.id
        WHERE p.status = ?
        ORDER BY p.id ASC;
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (status,))
        return [dict(row) for row in cursor.fetchall()]


def criar_pedido(cliente_id: int, produto: str, valor: float) -> dict[str, Any]:
    """Insere um novo pedido no banco com status inicial 'Processando'."""
    query = """
        INSERT INTO pedidos (cliente_id, produto, valor, status)
        VALUES (?, ?, ?, 'Processando');
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (cliente_id, produto, valor))
        novo_id = cursor.lastrowid
        return {
            "pedido_id": novo_id,
            "cliente_id": cliente_id,
            "produto": produto,
            "valor": valor,
            "status": "Processando",
        }

if __name__ == "__main__":
    init_db()
    print("Banco inicializado!")