# 📄 Invoice Intelligence Pipeline (ETL com LLM)

Pipeline de Engenharia de Dados para extração estruturada de informações de Notas Fiscais (PDFs e Imagens) utilizando Inteligência Artificial Generativa.

O projeto transforma documentos não estruturados em dados validados (JSON) e os persiste automaticamente em um banco de dados relacional (PostgreSQL).

---

## 🚀 Funcionalidades

*   **Ingestão Universal:** Aceita PDFs de qualquer layout (não usa templates fixos ou Regex).
*   **Visão Computacional:** Converte páginas em imagens de alta resolução para que a IA "veja" o documento como um humano.
*   **Extração Semântica:** Usa LLMs para entender e extrair campos específicos (Emissor, Destinatário, Itens, Totais).
*   **Validação Rigorosa:** Utiliza **Pydantic** para garantir que os dados de saída obedeçam a um contrato de dados estrito.
*   **Data Lake (Storage):** Salva os arquivos JSON originais (Raw Data) no **AWS S3** para auditoria e reprocessamento.
*   **Persistência SQL:** Salva os dados estruturados em um banco de dados PostgreSQL (via Supabase) usando **SQLAlchemy** (ORM).
*   **Processamento Incremental:** Mantém histórico de arquivos pra não reprocessar.

---

## ⚠️ Aviso Crítico: Privacidade de Dados e LGPD

Este projeto é um **Laboratório de Engenharia**. 

Para ambientes de **Produção** que lidam com dados reais de terceiros (CPF, CNPJ, Endereços), é **IMPERATIVO** adotar uma das seguintes estratégias de segurança:

1.  **Cloud Privada (Enterprise):** Utilizar instâncias privadas de modelos (Azure OpenAI Service, AWS Bedrock) com contratos de "Zero Data Retention" (os dados não são usados para treinar os modelos públicos).
2.  **Modelos Locais (On-Premise):** Executar modelos Open Source (como Llama 3, Phi-3 ou Mistral) dentro da sua própria infraestrutura, garantindo que os dados nunca saiam do seu servidor.

> **Nunca envie dados sensíveis (PII) para APIs públicas de LLMs sem anonimização prévia ou contratos enterprise adequados.**

---

## 🛠️ Stack Tecnológico

*   **Linguagem:** Python 3.11+
*   **Orquestração & LLM:** LangChain
*   **Validação de Dados:** Pydantic
*   **Processamento de PDF:** PyMuPDF (Fitz)
*   **Storage (Data Lake):** AWS S3 (via Boto3)
*   **Banco de Dados:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Gerenciador de Pacotes:** uv (mas compatível com pip/poetry)

---

## 📦 Estrutura do Projeto

```bash
/
├── main.py              # Ponto de entrada (Entrypoint)
├── data/                # Coloque seus PDFs aqui (Input)
├── database/            # Configuração de conexão DB
├── schemas/             # Contratos de Dados (Pydantic Models)
└── src/
    ├── extractor.py     # Orquestrador do Pipeline
    ├── llm/             # Cliente de IA
    ├── models/          # Tabelas do Banco (SQLAlchemy)
    └── services/        # Regras de Negócio (Salvar no Banco e S3)
```

---

## ▶️ Como Rodar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/jonhnatta/invoice-ia-pipeline.git
    cd invoice-ia-pipeline
    ```

2.  **Configure o Ambiente:**
    Crie um arquivo `.env` na raiz:
    ```ini
    OPENAI_API_KEY=sk-...
    DATABASE_URL=postgresql://user:pass@host:5432/postgres
    
    # AWS (Para S3)
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_REGION=us-east-1
    AWS_S3_BUCKET=nome-do-seu-bucket
    ```

3.  **Instale as dependências:**
    ```bash
    # Se usar uv:
    uv sync
    ```

4.  **Execute o Pipeline:**
    Coloque seus PDFs na pasta `data/` e rode:
    ```bash
    uv run main.py
    # ou
    python main.py
    ```

O sistema irá processar os arquivos novos, gerar os JSONs na pasta `output/` e inserir os registros no seu banco de dados automaticamente.

---
**Desenvolvido como case de estudo para Engenharia de Dados com IA.**
