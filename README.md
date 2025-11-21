📘 GLOBAL SOLUTION – SEGURANÇA DE APLICAÇÕES EM PYTHON  
=======================================================

Este projeto demonstra QUATRO vulnerabilidades de segurança muito comuns em aplicações Python.  
Para cada vulnerabilidade você encontrará:

🔹 Explicação do conceito e do risco  
🔹 Código vulnerável  
🔹 Script simples de ataque (demonstração didática)  
🔹 Código corrigido (defesa)  
🔹 Explicação de como o CI/CD detectaria o problema (SAST / SCA / DAST)  

As vulnerabilidades implementadas são:

1️⃣ Injeção de SQL  
2️⃣ Quebra de Controle de Acesso  
3️⃣ Desserialização Insegura  
4️⃣ Injeção de Comando no Sistema Operacional  

Cada arquivo `.py` possui sua própria demonstração através de uma função `demo()`.

=======================================================
📂 ESTRUTURA DO PROJETO
=======================================================

sql_injection_demo.py  
access_control_demo.py  
insecure_deserialization_demo.py  
command_injection_demo.py  
README.txt (este arquivo)

Para rodar qualquer demo:

👉  python nome_do_arquivo.py

Exemplo:
👉  python sql_injection_demo.py

=======================================================
1️⃣ INJEÇÃO DE SQL
=======================================================

📌 CONCEITO  
Acontece quando o programa monta comandos SQL concatenando diretamente dados enviados pelo usuário.  
Um atacante pode inserir pedaços de SQL malicioso e alterar a lógica da consulta.

⚠️ RISCOS  
- Login sem senha (bypass de autenticação)  
- Exposição de dados sensíveis  
- Modificação ou destruição do banco  
- Perda total de integridade

-------------------------------------------------------
💀 CÓDIGO VULNERÁVEL (resumo)

query = f"SELECT * FROM usuarios WHERE username = '{username}' AND senha = '{senha}'"

O usuário controla parte da query → PERIGO.

-------------------------------------------------------
🔥 ATAQUE DEMONSTRADO

O payload:
    ' OR '1'='1

Gera uma query sempre verdadeira.  
No vídeo, a versão vulnerável aceita o login indevido.

-------------------------------------------------------
🛡️ CÓDIGO SEGURO (DEFESA)

query = "SELECT * FROM usuarios WHERE username = ? AND senha = ?"
cursor.execute(query, (username, senha))

Usando parâmetros, o banco trata tudo como DADO, não como código.

-------------------------------------------------------
🤖 CI/CD – DETECÇÃO  
- SAST: ✔️ detecta concatenação insegura  
- DAST: ✔️ testa payloads de injeção  
- SCA: ❌ pouco relevante  

Ferramenta principal: **SAST**

=======================================================
2️⃣ QUEBRA DE CONTROLE DE ACESSO
=======================================================

📌 CONCEITO  
Ocorre quando a aplicação deixa o usuário acessar informações que não pertencem a ele, sem verificar permissões corretamente.

⚠️ RISCOS  
- Usuários acessando dados de outros  
- Modificação de registros alheios  
- Violação de privacidade  
- Vazamento massivo de dados

-------------------------------------------------------
💀 CÓDIGO VULNERÁVEL

def get_pedido_vulneravel(pedido_id, usuario_logado_id):
    return pedido → sem validar o dono

-------------------------------------------------------
🔥 ATAQUE DEMONSTRADO

Usuário 1 acessando pedido do usuário 2 apenas mudando o ID.

Versão vulnerável: ✔️ retorna o pedido  
Versão segura: ❌ bloqueia

-------------------------------------------------------
🛡️ CÓDIGO SEGURO

if pedido["usuario_id"] == usuario_logado_id:
    return pedido
else:
    return None

-------------------------------------------------------
🤖 CI/CD – DETECÇÃO  
- SAST: ⚠️ consegue identificar lacuna de autorização  
- DAST: ✔️ excelente – detecta IDOR automaticamente  
- SCA: ❌ irrelevante  

Ferramenta principal: **DAST**, com apoio de SAST.

=======================================================
3️⃣ DESSERIALIZAÇÃO INSEGURA
=======================================================

📌 CONCEITO  
Desserializar dados externos usando mecanismos como `pickle` pode executar código arbitrário durante a reconstrução do objeto.

⚠️ RISCOS  
- Execução remota de comandos (RCE)  
- Comprometimento total do servidor  
- Malware sendo carregado como “objeto”  

-------------------------------------------------------
💀 CÓDIGO VULNERÁVEL

pickle.loads(dados_serializados)

O usuário controla o conteúdo → pode criar objetos maliciosos.

-------------------------------------------------------
🔥 ATAQUE DEMONSTRADO

Classe com "__reduce__" executa:

os.system("echo '>>> MALICIOSO <<<")

Quando desserializa → comando é executado automaticamente.

-------------------------------------------------------
🛡️ CÓDIGO SEGURO

Uso de JSON:

config = json.loads(json_string)

+ validação dos campos.

-------------------------------------------------------
🤖 CI/CD – DETECÇÃO  
- SAST: ✔️ detecta uso inseguro de pickle  
- SCA: ✔️ alerta dependências vulneráveis  
- DAST: ⚠️ possível, mas não ideal  

Ferramenta principal: **SAST**, complementado com SCA.

=======================================================
4️⃣ INJEÇÃO DE COMANDO
=======================================================

📌 CONCEITO  
Acontece quando a aplicação monta um comando para o SO usando entrada do usuário, permitindo injeção de operadores como `&&`, `|`, `;`.

⚠️ RISCOS  
- Execução arbitrária de comandos  
- Acesso ao sistema  
- Tomada total da máquina  

-------------------------------------------------------
💀 CÓDIGO VULNERÁVEL

os.system(f"echo Listando {alvo}")

Se alvo contém "&& rm -rf /" o shell executa.

-------------------------------------------------------
🔥 ATAQUE DEMONSTRADO

alvo_malicioso = "dir && echo 'COMANDO EXTRA'"

Versão vulnerável executa os DOIS comandos.

-------------------------------------------------------
🛡️ CÓDIGO SEGURO

subprocess.run(["echo", "Listando arquivos de", alvo])

Argumentos são separados → shell não interpreta operadores.

-------------------------------------------------------
🤖 CI/CD – DETECÇÃO  
- SAST: ✔️ detecta uso de system() com input  
- DAST: ✔️ detecta comando injetado  
- SCA: ❌ irrelevante  

Ferramenta principal: **SAST**

=======================================================
🏁 CONCLUSÃO
=======================================================

Este projeto demonstra, de forma prática:

✔️ Como surgem vulnerabilidades reais em Python  
✔️ Como explorá-las com ataques simples  
✔️ Como aplicar boas práticas de defesa  
✔️ Como ferramentas DevSecOps identificam essas falhas no pipeline CI/CD  

RM94618 - Enzo Vazquez Sartorelli
RM94524 - Eduardo de Oliveira Nistal

