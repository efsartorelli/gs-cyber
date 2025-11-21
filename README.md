# Global Solution – Segurança de Aplicações em Python

Este repositório demonstra **quatro vulnerabilidades de segurança** vistas ao longo do ano, utilizando exemplos em Python:

1. Injeção de SQL  
2. Quebra de Controle de Acesso  
3. Desserialização Insegura em Python  
4. Injeção de Comando no Sistema Operacional  

Para cada vulnerabilidade, este trabalho:

- **Descreve** o conceito e o risco;
- **Mostra um código vulnerável**;
- **Apresenta um script de ataque** simples (demonstração didática);
- **Mostra o código corrigido**, aplicando boas práticas de codificação segura;
- **Explica como a falha seria detectada** em um pipeline moderno de CI/CD (SAST / SCA / DAST).

---

## Estrutura do Projeto

Sugestão de organização dos arquivos:

``text

├─ sql_injection_demo.py
├─ access_control_demo.py
├─ insecure_deserialization_demo.py
└─ command_injection_demo.py

Cada arquivo contém:

Funções vulneráveis;

Funções seguras (corrigidas);

Uma função demo() que executa exemplos de ataque e de defesa.

Para rodar qualquer demo:

python nome_do_arquivo.py

1. Injeção de SQL
1.1. Conceito e risco

Injeção de SQL ocorre quando a aplicação monta comandos SQL concatenando diretamente dados vindos do usuário, sem validação ou parametrização.

Um atacante pode:

Burlar autenticação (logar sem saber a senha);

Ler dados sensíveis (ex.: tabela de usuários);

Alterar ou excluir registros;

Até comprometer completamente o banco de dados.

Impacta principalmente:

Confidencialidade (vazamento de dados),

Integridade (alteração indevida),

Disponibilidade (apagando tabelas, por exemplo).

1.2. Código vulnerável

Arquivo: sql_injection_demo.py

Neste exemplo, o login é feito concatenando diretamente username e senha na query SQL.

import sqlite3

def login_vulneravel(username, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # CÓDIGO VULNERÁVEL: concatena diretamente os dados do usuário
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND senha = '{senha}'"
    print("[VULNERÁVEL] Executando query:", query)

    cursor.execute(query)
    resultado = cursor.fetchone()

    conn.close()
    return resultado


Problema:
Se o usuário inserir um payload malicioso, ele é incluído como parte da query SQL, e não apenas como dado.

1.3. Script de ataque (explorando a falha)

Ainda em sql_injection_demo.py, o demo() simula um ataque:

def demo():
    init_db()  # cria a tabela usuarios e insere admin/1234 se não existir

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


No passo 2, a query gerada fica aproximadamente:

SELECT * FROM usuarios
WHERE username = 'admin'
  AND senha = '' OR '1'='1'


'1'='1' é sempre verdadeiro → a condição do WHERE se torna verdadeira, permitindo login indevido.

1.4. Código corrigido (defesa)

A correção é usar queries parametrizadas:

def login_seguro(username, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # CÓDIGO SEGURO: uso de parâmetros (prepared statements)
    query = "SELECT * FROM usuarios WHERE username = ? AND senha = ?"
    print("[SEGURO] Executando query parametrizada:", query, (username, senha))

    cursor.execute(query, (username, senha))
    resultado = cursor.fetchone()

    conn.close()
    return resultado


Boas práticas aplicadas:

Nunca concatenar input do usuário em SQL;

Usar placeholders (?) e passagem de parâmetros;

Deixar o próprio driver/banco fazer o escape correto.

1.5. Detecção no CI/CD (SAST / SCA / DAST)

SAST (Static Application Security Testing)

Analisa o código-fonte e detecta uso de concatenação de strings em queries SQL.

Ferramentas típicas: SonarQube, Semgrep, Bandit (para Python), etc.

DAST (Dynamic Application Security Testing)

Testa a aplicação rodando, enviando payloads como "' OR '1'='1" para verificar se a autenticação ou consultas são quebradas.

SCA (Software Composition Analysis)

Menos relevante aqui, pois o problema está no código da aplicação (não em dependências vulneráveis).

Ferramenta mais adequada para automatizar a detecção dessa falha: SAST, com complemento de DAST.

2. Quebra de Controle de Acesso
2.1. Conceito e risco

Quebra de controle de acesso acontece quando a aplicação não valida corretamente se o usuário possui permissão para acessar determinado recurso.

Exemplos:

Usuário comum acessando dados de outro usuário (IDOR – Insecure Direct Object Reference);

Usuário não admin acessando rotas administrativas;

Usuário alterando dados de outros apenas mudando o ID na URL.

Riscos:

Vazamento de dados sensíveis de outros usuários;

Alteração/remoção de dados de terceiros;

Impactos legais e de privacidade.

2.2. Código vulnerável

Arquivo: access_control_demo.py

pedidos_db = [
    {"id": 1, "usuario_id": 1, "valor": 100.0},
    {"id": 2, "usuario_id": 2, "valor": 250.0},
]

def get_pedido_vulneravel(pedido_id, usuario_logado_id):
    """
    NÃO verifica se o pedido pertence ao usuário logado.
    """
    for pedido in pedidos_db:
        if pedido["id"] == pedido_id:
            return pedido
    return None


O problema:
A função simplesmente retorna o pedido pelo ID, ignorando quem está logado (usuario_logado_id).

2.3. Script de ataque (explorando a falha)

No demo():

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


Saída esperada:

Versão vulnerável → retorna o pedido do usuário 2, mesmo logado como usuário 1;

Versão segura → retorna None (acesso negado).

2.4. Código corrigido (defesa)
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


Boas práticas:

Sempre verificar a propriedade do recurso (ex.: usuario_id) em relação ao usuário logado;

Nunca confiar apenas em IDs enviados na URL ou no corpo da requisição;

Implementar uma camada clara de autorização (roles, permissões).

2.5. Detecção no CI/CD (SAST / SCA / DAST)

SAST

Pode apontar funções que acessam recursos sensíveis sem verificar o usuário logado ou regras de autorização.

DAST

Muito eficaz: automatiza testes trocando IDs (ex.: tenta acessar /pedido/2 com usuário 1) e verifica se a aplicação devolve dados que não deveriam ser acessíveis.

SCA

Pouco relevante aqui; o problema está na lógica de autorização da aplicação.

Ferramenta de DevSecOps mais importante neste caso: DAST, com apoio de SAST.

3. Desserialização Insegura em Python
3.1. Conceito e risco

Desserialização insegura acontece quando a aplicação desserializa dados não confiáveis (vindos de usuários, rede, arquivos externos) usando mecanismos que podem executar código arbitrário, como pickle.loads.

Se o atacante controlar o conteúdo serializado, ele pode:

Criar objetos maliciosos;

Executar comandos no servidor durante a desserialização;

Comprometer o sistema (execução remota de código – RCE).

3.2. Código vulnerável

Arquivo: insecure_deserialization_demo.py

import pickle

def carregar_config_vulneravel(dados_serializados: bytes):
    """
    Desserializa qualquer coisa que chegar em 'dados_serializados'.
    Isso é perigoso se o atacante controlar esse conteúdo.
    """
    print("[VULNERÁVEL] Chamando pickle.loads em dado não confiável...")
    config = pickle.loads(dados_serializados)
    return config


Aqui, pickle.loads está sendo chamado diretamente em dados potencialmente controlados pelo usuário.

3.3. Script de ataque (explorando a falha)

Classe maliciosa e uso:

import os

class PayloadMalicioso:
    def __reduce__(self):
        # Comando didático para demonstração
        return (os.system, ("echo '>>> COMANDO MALICIOSO EXECUTADO DURANTE A DESSERIALIZACAO <<<'",))

def demo():
    print("=== DEMO DESSERIALIZAÇÃO INSEGURA ===")

    # 1) Cria payload malicioso
    print("\n1) Gerando payload malicioso com pickle...")
    obj_malicioso = PayloadMalicioso()
    dados_maliciosos = pickle.dumps(obj_malicioso)

    # 2) Passa o payload malicioso para a versão vulnerável
    print("\n2) Passando payload malicioso para a função VULNERÁVEL:")
    carregar_config_vulneravel(dados_maliciosos)


Ao executar demo(), ao desserializar dados_maliciosos, o Python:

Chama os.system("echo '>>> COMANDO MALICIOSO EXECUTADO DURANTE A DESSERIALIZACAO <<<'");

Mostra a mensagem no console, evidenciando execução de comando durante a desserialização.

3.4. Código corrigido (defesa)

Solução: usar formato de dados seguro (JSON) + validação:

import json

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


Boas práticas:

Evitar pickle (e similares) para dados vindos de fontes não confiáveis;

Preferir formatos como JSON, que são apenas dados, e não código executável;

Validar explicitamente os campos esperados.

3.5. Detecção no CI/CD (SAST / SCA / DAST)

SAST

Identifica chamadas a funções perigosas (pickle.loads, yaml.load sem safe_load, etc.) com dados externos.

SCA

Detecta bibliotecas de desserialização vulneráveis ou configurações inseguras em dependências.

DAST

Pode detectar comportamentos estranhos, mas não é a melhor abordagem para achar desserialização insegura.

Ferramentas mais adequadas: SAST (principal) e SCA (quando envolver libs de terceiros).

4. Injeção de Comando
4.1. Conceito e risco

Injeção de comando acontece quando a aplicação monta um comando para o sistema operacional concatenando dados vindos do usuário e executa isso via shell (os.system, subprocess com shell=True, etc.).

O atacante pode:

Injetar comandos adicionais usando ;, &&, |, etc.;

Executar qualquer comando que o usuário do processo tiver permissão;

Comprometer o servidor por completo.

4.2. Código vulnerável

Arquivo: command_injection_demo.py

import os

def listar_arquivos_vulneravel(alvo):
    """
    Monta um comando usando concatenação de string.
    Qualquer coisa que vier em 'alvo' vai ser passada direto para o shell.
    """
    comando = f"echo Listando arquivos de {alvo}"
    print("[VULNERÁVEL] Comando enviado para o sistema:", comando)
    os.system(comando)


Aqui, alvo vai direto para a string de comando, o que abre espaço para injeção.

4.3. Script de ataque (explorando a falha)

Ainda no demo():

def demo():
    print("=== DEMO INJEÇÃO DE COMANDO ===")

    alvo_normal = "meu_diretorio"
    alvo_malicioso = "meu_diretorio && echo '>>> COMANDO EXTRA INJETADO <<<'"

    print("\n1) Versão VULNERÁVEL com input normal:")
    listar_arquivos_vulneravel(alvo_normal)

    print("\n2) Versão VULNERÁVEL com payload malicioso:")
    listar_arquivos_vulneravel(alvo_malicioso)


O comando final executado será algo como:

echo Listando arquivos de meu_diretorio && echo '>>> COMANDO EXTRA INJETADO <<<'


O && faz com que o shell execute dois comandos: o echo normal e o comando extra injetado.

4.4. Código corrigido (defesa)

Utilizando subprocess.run com lista de argumentos (sem shell):

import subprocess

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


Boas práticas:

Evitar os.system e subprocess com shell=True ao receber dados do usuário;

Passar o comando como lista de argumentos, não como string única;

Validar/limitar os valores que o usuário pode enviar (lista branca de diretórios, por exemplo).

4.5. Detecção no CI/CD (SAST / SCA / DAST)

SAST

Detecta uso de APIs perigosas (os.system, subprocess.Popen com shell=True, etc.) em combinação com dados não validados.

DAST

Testa a aplicação enviando inputs com caracteres especiais (;, &&, |) e observa se há execução de comandos inesperados.

SCA

Pouco relevante aqui; o problema é a forma de uso das APIs, não uma biblioteca vulnerável.

Ferramenta principal para detectar: SAST, com DAST validando em ambiente de teste.

5. Resumo – Ferramentas DevSecOps (SAST, SCA, DAST)

Tabela comparativa:

Vulnerabilidade	SAST (Estático)	SCA (Dependências)	DAST (Dinâmico)
Injeção de SQL	Detecta concatenação de input em queries SQL	–	Testa payloads de SQL injection em endpoints da aplicação
Quebra de Controle de Acesso	Aponta funções sem checagem de autorização	–	Testa troca de IDs / perfis (IDOR)
Desserialização Insegura em Python	Detecta uso de pickle.loads com dados não confiáveis	Aponta libs de desserialização vulneráveis	Pode observar efeitos, mas não é o principal
Injeção de Comando	Detecta os.system / subprocess com shell + input	–	Testa entradas com ;, &&, `
6. Como este trabalho atende aos critérios de avaliação

Clareza na descrição das vulnerabilidades (conceito e risco)

Cada vulnerabilidade possui uma seção dedicada explicando o conceito, impacto e riscos.

Precisão técnica dos exemplos de código (vulnerável e corrigido)

Os arquivos .py apresentam códigos vulneráveis reais e versões corrigidas, seguindo boas práticas de segurança em Python.

Demonstração de scripts de ataque

Em cada caso há um “mini ataque” que explora a falha de forma didática (injeção de SQL, acesso indevido, execução de comando via desserialização, e injeção de comando no SO).

Correlação com DevSecOps (SAST, SCA, DAST)

Para cada vulnerabilidade, há uma explicação específica de como seria detectada em um pipeline moderno de CI/CD, identificando a ferramenta mais adequada (SAST, SCA, DAST).
