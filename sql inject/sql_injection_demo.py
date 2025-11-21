import sqlite3

# ===========================
# Setup simples do banco
# ===========================
def init_db():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            senha TEXT NOT NULL
        )
    """)

    # Insere um usuário padrão se não existir
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
    conn.close()


# ===========================
# Versão vulnerável
# ===========================
def login_vulneravel(username, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # CONCATENAÇÃO DIRETA (VULNERÁVEL)
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND senha = '{senha}'"
    print("[VULNERÁVEL] Executando query:", query)

    cursor.execute(query)
    resultado = cursor.fetchone()

    conn.close()
    return resultado


# ===========================
# Versão segura
# ===========================
def login_seguro(username, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # QUERY PARAMETRIZADA (SEGURA)
    query = "SELECT * FROM usuarios WHERE username = ? AND senha = ?"
    print("[SEGURO] Executando query parametrizada:", query, (username, senha))

    cursor.execute(query, (username, senha))
    resultado = cursor.fetchone()

    conn.close()
    return resultado


# ===========================
# Demonstração
# ===========================
def demo():
    init_db()

    print("=== DEMO INJEÇÃO DE SQL ===")
    print("\n1) Tentativa normal com senha errada (VULNERÁVEL):")
    res = login_vulneravel("admin", "senha_errada")
    print("Resultado:", res)

    print("\n2) Ataque de injeção usando payload \"' OR '1'='1\" (VULNERÁVEL):")
    payload = "' OR '1'='1"
    res = login_vulneravel("admin", payload)
    print("Resultado:", res)

    print("\n3) Mesma tentativa de ataque na versão SEGURA:")
    res = login_seguro("admin", payload)
    print("Resultado:", res)


if __name__ == "__main__":
    demo()
