import pickle
import os
import json


# ===========================
# Classe usada no "ataque"
# ===========================
class PayloadMalicioso:
    def __reduce__(self):
        # Comando totalmente didático/seguro para demonstração
        return (os.system, ("echo '>>> COMANDO MALICIOSO EXECUTADO DURANTE A DESSERIALIZACAO <<<'",))


# ===========================
# Versão vulnerável
# ===========================
def carregar_config_vulneravel(dados_serializados: bytes):
    """
    Desserializa qualquer coisa que chegar em 'dados_serializados'.
    Isso é perigoso se o atacante controlar esse conteúdo.
    """
    print("[VULNERÁVEL] Chamando pickle.loads em dado não confiável...")
    config = pickle.loads(dados_serializados)
    return config


# ===========================
# Versão segura (JSON)
# ===========================
def carregar_config_seguro(json_string: str):
    """
    Versão segura, utilizando JSON em vez de pickle, e validando os campos.
    """
    print("[SEGURO] Carregando configuração via JSON...")
    config = json.loads(json_string)

    # Exemplo simples de validação
    if "modo" not in config or config["modo"] not in ("dev", "prod"):
        raise ValueError("Configuração inválida")

    return config


# ===========================
# Demonstração
# ===========================
def demo():
    print("=== DEMO DESSERIALIZAÇÃO INSEGURA ===")

    # 1) Cria payload malicioso
    print("\n1) Gerando payload malicioso com pickle...")
    obj_malicioso = PayloadMalicioso()
    dados_maliciosos = pickle.dumps(obj_malicioso)

    # 2) Passa o payload malicioso para a versão vulnerável
    print("\n2) Passando payload malicioso para a função VULNERÁVEL:")
    try:
        carregar_config_vulneravel(dados_maliciosos)
    except Exception as e:
        print("Erro durante desserialização:", e)

    # 3) Exemplo seguro com JSON
    print("\n3) Versão SEGURA usando JSON:")
    json_config = '{"modo": "dev"}'
    config_segura = carregar_config_seguro(json_config)
    print("Config segura carregada:", config_segura)


if __name__ == "__main__":
    demo()
