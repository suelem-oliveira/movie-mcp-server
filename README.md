# 🎬 Movie MCP Server (Servidor MCP de Filmes)

Este projeto consiste em um servidor de cinema personalizado construído com o **Model Context Protocol (MCP)** utilizando o SDK oficial do Python (`FastMCP`). 

O objetivo deste servidor é fornecer a modelos de inteligência artificial (como o Claude) acesso a um banco de dados de filmes simulado em memória, permitindo que a IA leia sinopses, edite conteúdos em tempo de execução, acesse recursos padronizados e utilize prompts de análise otimizados.

---

## 🎯 Origem do Projeto e Aprendizado

Este projeto foi desenvolvido como aplicação prática dos conceitos do **Curso de Protocolo de Contexto de Modelo (MCP)**. 

> "Para demonstrar o domínio prático dos conceitos ensinados no curso (que utilizava originalmente um exemplo focado em gerenciamento de documentos de escritório), eu fiz uma **refatoração criativa** da arquitetura de código. Apliquei os mesmos pilares de Ferramentas, Recursos, Prompts e Depuração com o Inspector em um contexto totalmente novo de banco de dados de cinema."

---

## 🛠️ Funcionalidades Implementadas

O projeto foi estruturado seguindo rigorosamente os três blocos de construção essenciais do MCP:

### 1. Ferramentas (`@mcp.tool`)
As ferramentas permitem que o modelo de IA tome ações dinâmicas no servidor:
*   **`read_movie_contents`**: Retorna a sinopse do filme solicitado. Utiliza validação com `ValueError` caso o ID não exista.
*   **`edit_movie`**: Realiza uma operação de localizar e substituir strings dentro da sinopse do filme em tempo de execução.
*   *Nota técnica:* Utilizei dicas de tipo (type hints) do Python e a classe `Field` do Pydantic para gerar esquemas de entrada JSON automáticos. Isso permite que a IA compreenda as descrições dos parâmetros sem a necessidade de escrever esquemas complexos manualmente.

### 2. Recursos (`@mcp.resource`)
Os recursos expõem dados estáticos ou dinâmicos de forma eficiente diretamente ao contexto da IA:
*   **Recurso Estático (`movies://list`)**: Retorna a lista completa de IDs de filmes disponíveis formatada como `application/json`.
*   **Recurso com Modelo (`movies://movie/{movie_id}`)**: Permite que o cliente resgate o texto puro da sinopse do filme desejado utilizando o tipo MIME `text/plain`.

### 3. Prompts (`@mcp.prompt`)
*   **`/analyze_plot`**: Um prompt parametrizado de alta qualidade que guia o comportamento da IA. Ele instrui o modelo a assumir o papel de um crítico de cinema profissional, ler a sinopse através do servidor e sugerir uma continuação ou spin-off criativo para o filme de forma consistente.

---

## 🚀 Como Executar e Testar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o Python e o gerenciador de pacotes `uv` (ou o `pip`) instalados.

1.  **Instale o SDK do MCP** com os utilitários de linha de comando (CLI):
    ```bash
    pip install "mcp[cli]"
    ```

2.  **Inicie o ambiente de desenvolvimento e depuração** (MCP Inspector):
    ```bash
    uv run mcp dev movie_server.py
    ```
    *(Este comando iniciará o servidor e criará uma ponte de comunicação local).*

3.  **Abra o link do Inspetor no Navegador**:
    O terminal exibirá um link local com um token de segurança gerado pela CLI. Copie e cole esse endereço no navegador para acessar a interface visual de testes.

4.  **Testando a execução no Inspector**:
    *   Na aba **Tools**, selecione `read_movie_contents`, digite `As branquelas` no campo e clique em **Run tool**.
    *   O Inspetor manterá o estado do servidor, permitindo editar o filme com `edit_movie` e verificar a persistência de dados imediatamente realizando uma nova leitura.
