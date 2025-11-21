# Basezinha de "pedidos" em memória
pedidos_db = [
    {"id": 1, "usuario_id": 1, "valor": 100.0},
    {"id": 2, "usuario_id": 2, "valor": 250.0},
]


# ===========================
# Versão vulnerável
# ===========================
def get_pedido_vulneravel(pedido_id, usuario_logado_id):
    """
    NÃO verifica se o pedido pertence ao usuário logado.
    """
    for pedido in pedidos_db:
        if pedido["id"] == pedido_id:
            return pedido
    return None


# ===========================
# Versão segura
# ===========================
def get_pedido_seguro(pedido_id, usuario_logado_id):
    """
    Verifica se o pedido é do usuário logado.
    """
    for pedido in pedidos_db:
        if pedido["id"] == pedido_id:
            if pedido["usuario_id"] == usuario_logado_id:
                return pedido
            else:
                # Acesso negado
                return None
    return None


# ===========================
# Demonstração
# ===========================
def demo():
    usuario_logado_id = 1
    pedido_alvo = 2  # Pedido que pertence ao usuário 2

    print("=== DEMO QUEBRA DE CONTROLE DE ACESSO ===")
    print(f"Usuário logado: {usuario_logado_id}")
    print(f"Tentando acessar pedido ID {pedido_alvo}, que é do usuário 2.\n")

    print("1) Versão VULNERÁVEL:")
    res_vuln = get_pedido_vulneravel(pedido_alvo, usuario_logado_id)
    print("Resultado:", res_vuln)

    print("\n2) Versão SEGURA:")
    res_seguro = get_pedido_seguro(pedido_alvo, usuario_logado_id)
    print("Resultado:", res_seguro)


if __name__ == "__main__":
    demo()
