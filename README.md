
# Industrial AI Assistant
## Assistente Inteligente de Suporte Técnico Industrial

**Instituição:** Centro Universitário UniMAX  
**Disciplina:** Projeto Prático Integrado — Inteligência Artificial e Aprendizagem de Máquina  
**Professor:** Rogério Morandi  
**Projeto:** Rocket Industrial Solutions — Simulação Acadêmica

---

## 1. Descrição do Projeto

O Industrial AI Assistant é um assistente inteligente de suporte técnico industrial desenvolvido em Python.

O sistema utiliza RAG (Retrieval-Augmented Generation) para consultar documentos técnicos em PDF e responder perguntas com base nas informações recuperadas.

O objetivo é demonstrar como a inteligência artificial pode auxiliar na consulta a manuais, procedimentos de segurança, orientações de manutenção e especificações de equipamentos.

## 2. Funcionalidades

- Leitura e processamento de documentos PDF.
- Divisão dos documentos em trechos (chunking).
- Criação de embeddings.
- Armazenamento e consulta vetorial com ChromaDB.
- Busca híbrida por similaridade e palavras-chave.
- Geração de respostas com o modelo Llama 3.2.
- Interface interativa desenvolvida com Streamlit.
- Upload de novos documentos PDF.
- Histórico de conversas durante a sessão.
- Identificação dos documentos e páginas consultados.
- Tratamento de perguntas sem informação suficiente.

## 3. Tecnologias Utilizadas

- Python 3.11
- Streamlit
- LangChain
- ChromaDB
- Ollama
- Llama 3.2 (3B)
- Nomic Embed Text
- PyPDF

## 4. Estrutura do Projeto

```text
Assistente_Inteligente_RAG/
├── app.py
├── rag.py
├── requirements.txt
├── README.md
└── knowledge/
    ├── 01_manual_cnc.pdf
    ├── 02_procedimento_seguranca.pdf
    ├── 03_manual_compressor.pdf
    ├── 04_politica_manutencao.pdf
    ├── 05_checklist_operacional.pdf
    └── 06_manual_bomba_hidraulica.pdf
```

## 5. Requisitos para Execução

É necessário ter:

- Python 3.11 instalado.
- Ollama instalado e em execução.
- Acesso à internet para instalar as dependências e baixar os modelos inicialmente.

## 6. Como Executar

### Passo 1 — Abrir o projeto

Abra a pasta do projeto no VS Code.

### Passo 2 — Criar o ambiente virtual

No terminal:

```bash
python3.11 -m venv .venv
```

No macOS ou Linux, ative com:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Passo 3 — Instalar as bibliotecas

```bash
python -m pip install -r requirements.txt
```

### Passo 4 — Preparar os modelos de IA

Instale e inicie o Ollama:

https://ollama.com/download

Execute:

```bash
ollama pull llama3.2:3b
```

```bash
ollama pull nomic-embed-text
```

### Passo 5 — Iniciar a aplicação

```bash
python -m streamlit run app.py
```

Acesse no navegador:

http://localhost:8501

## 7. Exemplos de Perguntas

**Pergunta:** Qual óleo deve ser utilizado no compressor CP50?

**Resposta esperada:** Lubrificante ISO VG 68, sujeito à validação técnica.

**Pergunta:** Qual é a pressão nominal da bomba hidráulica BH-700?

**Resposta esperada:** 120 bar.

**Pergunta:** Qual é a senha do Wi-Fi da fábrica?

**Resposta esperada:** Não encontrei essa informação na documentação disponível.

## 8. Níveis do Exercício

### Nível 1 — RAG Básico

Implementação da leitura de PDFs, divisão de textos, embeddings, busca vetorial e geração de respostas.

### Nível 2 — Sistema Profissional

Interface interativa com upload de PDFs, histórico de conversas e indicação das fontes consultadas.

### Nível 3 — Controle de Alucinações

Implementação de regras de resposta baseadas nas evidências recuperadas e retorno de mensagem padrão quando não houver informação suficiente.

O controle foi validado em cenários de teste, mas não representa garantia absoluta contra respostas incorretas.

## 9. Observações

Todos os documentos industriais incluídos na pasta `knowledge` são fictícios, desenvolvidos exclusivamente para demonstração acadêmica.

Nenhuma informação desses manuais deve ser utilizada para operação ou manutenção de equipamentos reais.

O sistema foi desenvolvido e testado localmente em um MacBook com Python 3.11 e Ollama.

A execução em outros computadores depende da instalação das ferramentas e modelos necessários.

## 10. Conclusão

O projeto demonstra a aplicação prática da arquitetura RAG em um cenário de suporte técnico industrial.

A integração entre recuperação de informações documentais, modelos de linguagem e uma interface interativa permite consultar uma base de conhecimento utilizando perguntas em linguagem natural.
