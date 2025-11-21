import os
import subprocess


# ===========================
# Versão vulnerável
# ===========================
def listar_arquivos_vulneravel(alvo):
    """
    Monta um comando usando concatenação de string.
    Qualquer coisa que vier em 'alvo' vai ser passada direto para o shell.
    """
    comando = f"echo Listando arquivos de {alvo}"
    print("[VULNERÁVEL] Comando enviado para o sistema:", comando)
    os.system(comando)


# ===========================
# Versão segura
# ===========================
def listar_arquivos_seguro(alvo):
    """
    Usa subprocess.run com lista de argumentos, sem passar pelo shell.
    Isso impede que operadores como ';' ou '&&' sejam interpretados como novos comandos.
    """
    print("[SEGURO] Executando comando com argumentos separados:", ["echo", "Listando arquivos de", alvo])
    resultado = subprocess.run(
        ["echo", "Listando arquivos de", alvo],
        capture_output=True,
        text=True,
        check=True
    )
    print("Saída:", resultado.stdout.strip())


# ===========================
# Demonstração
# ===========================
def demo():
    print("=== DEMO INJEÇÃO DE COMANDO ===")

    alvo_normal = "meu_diretorio"
    alvo_malicioso = "meu_diretorio && echo '>>> COMANDO EXTRA INJETADO <<<'"  # payload didático

    print("\n1) Versão VULNERÁVEL com input normal:")
    listar_arquivos_vulneravel(alvo_normal)

    print("\n2) Versão VULNERÁVEL com payload malicioso:")
    listar_arquivos_vulneravel(alvo_malicioso)

    print("\n3) Versão SEGURA com payload malicioso (não deve injetar):")
    listar_arquivos_seguro(alvo_malicioso)


if __name__ == "__main__":
    demo()
