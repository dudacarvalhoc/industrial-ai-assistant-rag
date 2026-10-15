
import streamlit as st
from pathlib import Path

from rag import (
    criar_base,
    responder_pergunta,
    PASTA_DOCUMENTOS
)

# ==========================================
# CONFIGURACAO DA PAGINA
# ==========================================

st.set_page_config(
    page_title="Industrial AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DESIGN - TEMA CLARO
# ==========================================

st.markdown("""
<style>
    /* Fundo principal */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
    }

    /* Barra lateral */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background-color: #EAF2FF !important;
        color: #1E293B !important;
    }

    /* Textos e titulos */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp span {
        color: #1E293B;
    }

    /* Titulo principal */
    h1 {
        color: #2563EB !important;
        font-size: 2.3rem !important;
        font-weight: 750 !important;
    }

    h2, h3 {
        color: #1D4ED8 !important;
    }

    /* Cartoes do chat */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DBEAFE;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 12px;
    }

    /* Caixa de mensagens */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px;
    }

    [data-testid="stChatInput"] textarea {
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
        background-color: #FFFFFF !important;
    }

    /* Barra inferior do chat */
    [data-testid="stBottom"] > div {
        background-color: #F8FAFC !important;
    }

    /* Botoes */
    .stButton button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    .stButton button p {
        color: #FFFFFF !important;
    }

    /* Campos de upload */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #93C5FD !important;
        border-radius: 12px;
    }

    /* Informacoes */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Expandir fontes */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DBEAFE;
        border-radius: 10px;
    }

    /* Divisores */
    hr {
        border-color: #DBEAFE !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# CABECALHO
# ==========================================

st.title("🤖 Industrial AI Assistant")

st.markdown(
    "### Assistente Inteligente de Suporte Técnico Industrial"
)

st.write(
    "Consulte manuais técnicos, procedimentos de segurança "
    "e orientações de manutenção utilizando Inteligência Artificial."
)

st.caption(
    "Rocket Industrial Solutions | Sistema RAG Acadêmico"
)

st.divider()


# ==========================================
# BASE DE CONHECIMENTO
# ==========================================

PASTA_DOCUMENTOS.mkdir(parents=True, exist_ok=True)


def assinatura_documentos():
    arquivos = sorted(
        PASTA_DOCUMENTOS.glob("*.pdf")
    )

    return tuple(
        (
            arquivo.name,
            arquivo.stat().st_size,
            arquivo.stat().st_mtime_ns
        )
        for arquivo in arquivos
    )


@st.cache_resource(
    show_spinner="Preparando a base de conhecimento..."
)
def carregar_base_cache(assinatura):
    if not assinatura:
        return None

    return criar_base()


# ==========================================
# HISTORICO DE CONVERSAS
# ==========================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "assinatura_atual" not in st.session_state:
    st.session_state.assinatura_atual = None


# ==========================================
# MENU LATERAL
# ==========================================

with st.sidebar:

    st.header("📚 Base de Conhecimento")

    st.write(
        "Aqui ficam os documentos utilizados "
        "pela inteligência artificial."
    )

    st.divider()

    st.subheader("Adicionar documentos")

    arquivos_enviados = st.file_uploader(
        "Selecione novos manuais em PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    if arquivos_enviados:

        if st.button(
            "Adicionar à base",
            use_container_width=True
        ):

            for arquivo in arquivos_enviados:

                nome = Path(arquivo.name).name

                if not nome.lower().endswith(".pdf"):
                    continue

                destino = PASTA_DOCUMENTOS / nome

                destino.write_bytes(
                    arquivo.getbuffer()
                )

            st.cache_resource.clear()

            st.session_state.mensagens = []

            st.success(
                "Documentos adicionados com sucesso!"
            )

            st.rerun()

    st.divider()

    st.subheader("📄 Manuais disponíveis")

    documentos = sorted(
        PASTA_DOCUMENTOS.glob("*.pdf")
    )

    if documentos:

        for documento in documentos:
            st.write(f"📘 {documento.name}")

    else:
        st.warning(
            "Nenhum documento encontrado."
        )

    st.divider()

    st.metric(
        label="Total de documentos",
        value=len(documentos)
    )

    st.divider()

    if st.button(
        "🗑️ Limpar conversa",
        use_container_width=True
    ):
        st.session_state.mensagens = []
        st.rerun()

    st.caption(
        "Projeto acadêmico de Inteligência Artificial."
    )


# ==========================================
# INICIALIZAR SISTEMA RAG
# ==========================================

assinatura = assinatura_documentos()

if assinatura != st.session_state.assinatura_atual:
    st.session_state.mensagens = []
    st.session_state.assinatura_atual = assinatura

try:
    banco = carregar_base_cache(assinatura)

except Exception as erro:

    st.error(
        "Não foi possível carregar a base de conhecimento."
    )

    st.exception(erro)
    st.stop()


# ==========================================
# INTERFACE PRINCIPAL
# ==========================================

st.subheader("💬 Chat de Suporte Técnico")

st.info(
    "Faça perguntas sobre os equipamentos, "
    "manutenção ou segurança industrial."
)

if banco is None:

    st.warning(
        "Adicione documentos PDF para iniciar."
    )

    st.stop()


# ==========================================
# SUGESTOES DE PERGUNTAS
# ==========================================

st.markdown("**O que você gostaria de saber?**")

st.write(
    "Exemplos: Qual óleo utilizar no compressor? "
    "Quais procedimentos de segurança são necessários? "
    "Como consultar um código de erro?"
)

st.divider()


# ==========================================
# EXIBIR HISTORICO DO CHAT
# ==========================================

for mensagem in st.session_state.mensagens:

    with st.chat_message(
        mensagem["role"]
    ):

        st.markdown(
            mensagem["content"]
        )

        if mensagem.get("fontes"):

            with st.expander(
                "📖 Ver documentos consultados"
            ):

                for fonte in mensagem["fontes"]:

                    st.write(
                        f"📄 {fonte['documento']} "
                        f"— Página {fonte['pagina']}"
                    )


# ==========================================
# RECEBER PERGUNTAS
# ==========================================

pergunta = st.chat_input(
    "Digite sua pergunta sobre manutenção industrial..."
)

if pergunta:

    historico_anterior = list(
        st.session_state.mensagens
    )

    # Mensagem do usuario
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    # Resposta da inteligencia artificial
    with st.chat_message("assistant"):

        with st.spinner(
            "Consultando os documentos..."
        ):

            try:

                resultado = responder_pergunta(
                    pergunta,
                    banco,
                    historico_anterior
                )

                resposta = resultado["resposta"]
                fontes = resultado["fontes"]

            except Exception as erro:

                st.error(
                    "Ocorreu um erro ao consultar a IA."
                )

                st.exception(erro)
                st.stop()

        st.markdown(resposta)

        # Mostrar as referencias
        if fontes:

            with st.expander(
                "📖 Ver documentos consultados"
            ):

                for fonte in fontes:

                    st.write(
                        f"📄 {fonte['documento']} "
                        f"— Página {fonte['pagina']}"
                    )

    # Armazenar resposta no historico
    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta,
        "fontes": fontes
    })

