import io
import re
import os
import base64
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Biblioteca SESI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CORES SESI
# ============================================================

AZUL_SESI = "#005A9C"
AZUL_ESCURO = "#003B66"
CINZA = "#666666"
CINZA_CLARO = "#F4F6F8"
BRANCO = "#FFFFFF"


# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = os.path.dirname(
    os.path.abspath(__file__)
)

PASTA_DADOS = os.path.join(
    PASTA_PROJETO,
    "dados"
)

ARQUIVO_ACERVO = os.path.join(
    PASTA_DADOS,
    "acervo.csv"
)

ARQUIVO_INFO_ACERVO = os.path.join(
    PASTA_DADOS,
    "acervo_info.txt"
)

IMAGEM_ACERVO = os.path.join(
    PASTA_PROJETO,
    "acervo.png"
)

IMAGEM_LOGIN = os.path.join(
    PASTA_PROJETO,
    "login.png"
)

LOGO_SESI = os.path.join(
    PASTA_PROJETO,
    "logoSesi.jpg"
)

os.makedirs(
    PASTA_DADOS,
    exist_ok=True
)


# ============================================================
# CREDENCIAIS
# ============================================================

def carregar_credenciais():

    try:

        usuario = st.secrets["USUARIO_ADMIN"]
        senha = st.secrets["SENHA_ADMIN"]

        return (
            str(usuario),
            str(senha),
            True
        )

    except Exception:

        return (
            "",
            "",
            False
        )


USUARIO_ADMIN, SENHA_ADMIN, SECRETS_CONFIGURADO = (
    carregar_credenciais()
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ========================================================
       PÁGINA
       ======================================================== */

    .stApp {{
        background-color: {BRANCO};
    }}


    /* ========================================================
       MENU PADRÃO STREAMLIT
       ======================================================== */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}


    /* ========================================================
       LOGO
       ======================================================== */

    .logo-sesi {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }}

    .logo-sesi img {{
        width: 150px;
        max-width: 100%;
        height: auto;
    }}


    /* ========================================================
       TÍTULO PRINCIPAL
       ======================================================== */

    .titulo-principal {{
        color: {AZUL_SESI};
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 8px;
    }}


    /* ========================================================
       SUBTÍTULO
       ======================================================== */

    .subtitulo {{
        color: {CINZA};
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }}


    /* ========================================================
       TÍTULO DE SEÇÃO
       ======================================================== */

    .titulo-secao {{
        background-color: {AZUL_SESI};
        color: {BRANCO};
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 20px;
        text-align: center;
    }}


    /* ========================================================
       SUBTÍTULO DE SEÇÃO
       ======================================================== */

    .subtitulo-secao {{
        color: {AZUL_ESCURO};
        font-size: 18px;
        font-weight: bold;
        margin-top: 18px;
        margin-bottom: 12px;
    }}


    /* ========================================================
       CARDS DA PÁGINA INICIAL
       ======================================================== */

    .card-home {{
        width: 240px;
        height: 240px;
        margin: 0 auto;
    }}


    /* ========================================================
       BOTÕES
       ======================================================== */

    div.stButton > button {{
        border-radius: 8px;
        font-weight: bold;
        min-height: 45px;
    }}


    /* ========================================================
       RADIO
       ======================================================== */

    div[data-testid="stRadio"] > label {{
        font-weight: bold;
        color: {AZUL_ESCURO};
    }}

    div[data-testid="stRadio"] div[role="radiogroup"] {{
        gap: 8px;
    }}


    /* ========================================================
       TABELAS
       ======================================================== */

    div[data-testid="stDataFrame"] {{
        border-radius: 8px;
    }}


    /* ========================================================
       RODAPÉ
       IMPORTANTE:
       NÃO POSSUI DIVISÓRIA, BORDA OU LINHA
       ======================================================== */

    .rodape-final {{
        text-align: center;
        margin-top: 60px;
        padding: 20px 10px;
        color: {CINZA};
        font-size: 12px;
        line-height: 1.8;
        border: none !important;
        border-top: none !important;
        border-bottom: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}

    .rodape-final-principal {{
        color: {AZUL_ESCURO};
        font-size: 13px;
        font-weight: bold;
    }}

    .rodape-final-secundario {{
        color: {CINZA};
        font-size: 11px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RODAPÉ
# ============================================================

def mostrar_rodape():

    st.markdown(
        """
        <div class="rodape-final">

            <div class="rodape-final-principal">
                BIBLIOTECA SESI SÃO GONÇALO DO AMARANTE
            </div>

            <div class="rodape-final-secundario">
                Devs Jéssica Martins - Cientista da Informação
            </div>

            <div class="rodape-final-secundario">
                © 2026 • SESI Escola SGA/RN
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOGO
# ============================================================

def mostrar_logo():

    if os.path.exists(LOGO_SESI):

        st.markdown(
            '<div class="logo-sesi">',
            unsafe_allow_html=True
        )

        st.image(
            LOGO_SESI,
            width=150
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# IMAGEM BASE64
# ============================================================

def imagem_base64(caminho):

    try:

        with open(
            caminho,
            "rb"
        ) as arquivo:

            return base64.b64encode(
                arquivo.read()
            ).decode("utf-8")

    except Exception:

        return None


# ============================================================
# IMAGEM CLICÁVEL
# ============================================================

def imagem_clicavel(
    caminho,
    pagina
):

    imagem = imagem_base64(
        caminho
    )

    if not imagem:
        return False

    extensao = os.path.splitext(
        caminho
    )[1].lower()

    if extensao in [
        ".jpg",
        ".jpeg"
    ]:

        mime = "image/jpeg"

    elif extensao == ".webp":

        mime = "image/webp"

    else:

        mime = "image/png"

    html = f"""
    <a
        href="?pagina={pagina}"
        style="
            display: block;
            width: 240px;
            height: 240px;
            margin: auto;
            cursor: pointer;
            text-decoration: none;
        "
    >

        <img
            src="data:{mime};base64,{imagem}"
            alt=""
            style="
                width: 240px;
                height: 240px;
                object-fit: cover;
                display: block;
                border-radius: 18px;
                cursor: pointer;
                transition:
                    transform 0.2s ease,
                    box-shadow 0.2s ease;
            "
        >

    </a>

    <style>

        a:hover img {{
            transform: scale(1.04);
            box-shadow:
                0 8px 24px
                rgba(0, 0, 0, 0.20);
        }}

    </style>
    """

    st.html(html)

    return True


# ============================================================
# NORMALIZAR COLUNA
# ============================================================

def normalizar_coluna(nome):

    nome = str(
        nome
    ).strip().lower()

    substituicoes = {

        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "ä": "a",

        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",

        "í": "i",
        "ì": "i",
        "î": "i",
        "ï": "i",

        "ó": "o",
        "ò": "o",
        "õ": "o",
        "ô": "o",
        "ö": "o",

        "ú": "u",
        "ù": "u",
        "û": "u",
        "ü": "u",

        "ç": "c"
    }

    for antigo, novo in substituicoes.items():

        nome = nome.replace(
            antigo,
            novo
        )

    nome = re.sub(
        r"[^a-z0-9]+",
        "_",
        nome
    )

    return nome.strip("_")


# ============================================================
# LER CSV
# ============================================================

def ler_csv(arquivo):

    if arquivo is None:
        return None

    if hasattr(
        arquivo,
        "seek"
    ):

        arquivo.seek(0)

    tentativas = [

        ("utf-8-sig", ";"),
        ("utf-8", ";"),
        ("cp1252", ";"),
        ("latin1", ";"),

        ("utf-8-sig", ","),
        ("utf-8", ","),
        ("cp1252", ","),
        ("latin1", ",")
    ]

    for encoding, separador in tentativas:

        try:

            if hasattr(
                arquivo,
                "seek"
            ):

                arquivo.seek(0)

            df = pd.read_csv(
                arquivo,
                sep=separador,
                encoding=encoding,
                dtype=str
            )

            if len(df.columns) > 1:

                df.columns = [
                    str(col).strip()
                    for col in df.columns
                ]

                return df

        except Exception:

            continue

    return None


# ============================================================
# LER ACERVO SALVO
# ============================================================

def ler_acervo_salvo():

    if not os.path.exists(
        ARQUIVO_ACERVO
    ):

        return None

    tentativas = [

        ("utf-8-sig", ";"),
        ("utf-8", ";"),
        ("cp1252", ";"),
        ("latin1", ";"),

        ("utf-8-sig", ","),
        ("utf-8", ","),
        ("cp1252", ","),
        ("latin1", ",")
    ]

    for encoding, separador in tentativas:

        try:

            df = pd.read_csv(
                ARQUIVO_ACERVO,
                sep=separador,
                encoding=encoding,
                dtype=str
            )

            if len(df.columns) > 1:

                df.columns = [
                    str(col).strip()
                    for col in df.columns
                ]

                return df

        except Exception:

            continue

    return None


# ============================================================
# SALVAR ACERVO
# ============================================================

def salvar_acervo(df):

    df.to_csv(
        ARQUIVO_ACERVO,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    data_atual = datetime.now().strftime(
        "%d/%m/%Y às %H:%M"
    )

    with open(
        ARQUIVO_INFO_ACERVO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            data_atual
        )


# ============================================================
# DATA DO ACERVO
# ============================================================

def obter_data_acervo():

    if not os.path.exists(
        ARQUIVO_INFO_ACERVO
    ):

        return "Não informado"

    try:

        with open(
            ARQUIVO_INFO_ACERVO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return arquivo.read().strip()

    except Exception:

        return "Não informado"


# ============================================================
# NORMALIZAR DATAFRAME
# ============================================================

def normalizar_dataframe(df):

    if df is None:
        return None

    resultado = df.copy()

    resultado.columns = [
        str(col).strip()
        for col in resultado.columns
    ]

    for coluna in resultado.columns:

        resultado[coluna] = (
            resultado[coluna]
            .astype(str)
            .replace(
                "nan",
                "",
                regex=False
            )
            .str.strip()
        )

    return resultado


# ============================================================
# BUSCAR COLUNA
# ============================================================

def buscar_coluna(
    df,
    possibilidades
):

    if df is None:
        return None

    mapa = {
        normalizar_coluna(col): col
        for col in df.columns
    }

    for possibilidade in possibilidades:

        chave = normalizar_coluna(
            possibilidade
        )

        if chave in mapa:

            return mapa[chave]

    for coluna in df.columns:

        coluna_normalizada = (
            normalizar_coluna(coluna)
        )

        for possibilidade in possibilidades:

            possibilidade_normalizada = (
                normalizar_coluna(
                    possibilidade
                )
            )

            if (
                possibilidade_normalizada
                in coluna_normalizada
            ):

                return coluna

    return None


# ============================================================
# PESQUISAR DATAFRAME
# ============================================================

def pesquisar_dataframe(
    df,
    termo
):

    if df is None or not termo:
        return df

    termo = str(
        termo
    ).strip()

    if not termo:
        return df

    mascara = pd.Series(
        False,
        index=df.index
    )

    for coluna in df.columns:

        mascara = (
            mascara
            |
            df[coluna]
            .astype(str)
            .str.contains(
                termo,
                case=False,
                na=False,
                regex=False
            )
        )

    return df[mascara]


# ============================================================
# DOWNLOAD CSV
# ============================================================

def csv_download(df):

    buffer = io.StringIO()

    df.to_csv(
        buffer,
        index=False,
        sep=";"
    )

    return buffer.getvalue().encode(
        "utf-8-sig"
    )


# ============================================================
# CONVERTER DATA
# ============================================================

def converter_data(serie):

    return pd.to_datetime(
        serie,
        errors="coerce",
        dayfirst=True
    )


# ============================================================
# IDENTIFICAR HORÁRIO
# ============================================================

def identificar_horario(valor):

    try:

        if pd.isna(valor):
            return "Não informado"

        texto = str(
            valor
        ).strip()

        hora = pd.to_datetime(
            texto,
            errors="coerce"
        )

        if pd.isna(hora):
            return "Não informado"

        hora_decimal = (
            hora.hour
            +
            hora.minute / 60
        )

        if 7 <= hora_decimal <= 12:
            return "Manhã"

        if 12 < hora_decimal <= 13.25:
            return "Troca de turno"

        if 13.25 < hora_decimal <= 18:
            return "Tarde"

        return "Fora do horário"

    except Exception:

        return "Não informado"


# ============================================================
# LOCALIZAR DATA DA MOVIMENTAÇÃO
# ============================================================

def localizar_coluna_data_movimentacao(df):

    return buscar_coluna(
        df,
        [
            "Data",
            "Data do empréstimo",
            "Data do emprestimo",
            "Data empréstimo",
            "Data emprestimo",
            "Data da movimentação",
            "Data movimentação"
        ]
    )


# ============================================================
# LOCALIZAR DEVOLUÇÃO
# ============================================================

def localizar_coluna_devolucao(df):

    return buscar_coluna(
        df,
        [
            "Data de devolução",
            "Data de devolucao",
            "Data devolução",
            "Data devolucao",
            "Devolução",
            "Devolucao"
        ]
    )


# ============================================================
# LOCALIZAR DATA PREVISTA
# ============================================================

def localizar_coluna_prevista(df):

    return buscar_coluna(
        df,
        [
            "Data prevista",
            "Data prevista de devolução",
            "Data prevista de devolucao",
            "Previsão de devolução",
            "Previsao de devolucao",
            "Data de retorno"
        ]
    )


# ============================================================
# CALCULAR DIAS DE ATRASO
# ============================================================

def calcular_dias_atraso(df):

    coluna_prevista = (
        localizar_coluna_prevista(df)
    )

    coluna_devolucao = (
        localizar_coluna_devolucao(df)
    )

    if coluna_prevista is None:

        return pd.Series(
            0,
            index=df.index
        )

    prevista = converter_data(
        df[coluna_prevista]
    )

    if coluna_devolucao:

        devolucao = converter_data(
            df[coluna_devolucao]
        )

        data_final = devolucao.fillna(
            pd.Timestamp.today()
        )

    else:

        data_final = pd.Series(
            pd.Timestamp.today(),
            index=df.index
        )

    atraso = (
        data_final - prevista
    ).dt.days

    return (
        atraso
        .fillna(0)
        .clip(lower=0)
        .astype(int)
    )


# ============================================================
# PREPARAR MOVIMENTAÇÃO MENSAL
# ============================================================

def preparar_movimentacao_mensal(
    df,
    mes
):

    if df is None:
        return None

    resultado = normalizar_dataframe(
        df
    )

    coluna_data = (
        localizar_coluna_data_movimentacao(
            resultado
        )
    )

    if coluna_data is None:

        resultado["Data_Analise"] = pd.NaT

    else:

        resultado["Data_Analise"] = (
            converter_data(
                resultado[coluna_data]
            )
        )

    resultado["Mês"] = mes

    resultado["Mês_Numero"] = (
        resultado["Data_Analise"]
        .dt.month
    )

    resultado["Ano"] = (
        resultado["Data_Analise"]
        .dt.year
    )

    resultado["Bimestre"] = (
        resultado["Mês_Numero"]
        .apply(
            lambda x:
            (
                "1º Bimestre"
                if x in [1, 2]

                else

                "2º Bimestre"
                if x in [3, 4]

                else

                "3º Bimestre"
                if x in [5, 6]

                else

                "4º Bimestre"
                if x in [7, 8]

                else

                "Fora do período"
            )
        )
    )

    resultado["Semestre"] = (
        resultado["Mês_Numero"]
        .apply(
            lambda x:
            (
                "1º Semestre"
                if x and x <= 6

                else

                "2º Semestre"
                if x

                else

                "Não informado"
            )
        )
    )

    if coluna_data:

        resultado["Horário"] = (
            resultado[coluna_data]
            .apply(
                identificar_horario
            )
        )

    else:

        resultado["Horário"] = (
            "Não informado"
        )

    resultado["Dias de atraso"] = (
        calcular_dias_atraso(
            resultado
        )
    )

    return resultado


# ============================================================
# NAVEGAÇÃO
# ============================================================

def ir_para(pagina):

    st.query_params["pagina"] = pagina

    st.rerun()


# ============================================================
# LOGIN
# ============================================================

def fazer_login():

    mostrar_logo()

    st.markdown(
        """
        <div class="titulo-principal">
            🔐 LOGIN: ADMINISTRADOR
        </div>

        <div class="subtitulo">
            Acesso à área administrativa da Biblioteca SESI
        </div>
        """,
        unsafe_allow_html=True
    )

    col_esq, col_centro, col_dir = st.columns(
        [1, 2, 1]
    )

    with col_centro:

        if os.path.exists(IMAGEM_LOGIN):

            st.image(
                IMAGEM_LOGIN,
                width=250
            )

        with st.form("form_login"):

            usuario = st.text_input(
                "👤 Usuário",
                key="login_usuario"
            )

            senha = st.text_input(
                "🔑 Senha",
                type="password",
                key="login_senha"
            )

            entrar = st.form_submit_button(
                "🔐 ENTRAR",
                use_container_width=True
            )

            if entrar:

                if not SECRETS_CONFIGURADO:

                    st.error(
                        "⚠️ As credenciais do administrador "
                        "ainda não foram configuradas."
                    )

                    st.info(
                        "Configure USUARIO_ADMIN e "
                        "SENHA_ADMIN no arquivo "
                        ".streamlit/secrets.toml."
                    )

                elif (
                    usuario == USUARIO_ADMIN
                    and
                    senha == SENHA_ADMIN
                ):

                    st.session_state.autenticado = True

                    st.query_params["pagina"] = (
                        "administracao"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Usuário ou senha incorretos."
                    )

        if st.button(
            "← VOLTAR PARA INÍCIO",
            key="voltar_login",
            use_container_width=True
        ):

            ir_para("inicio")


# ============================================================
# SAIR
# ============================================================

def sair():

    st.session_state.autenticado = False

    if "login_usuario" in st.session_state:

        del st.session_state[
            "login_usuario"
        ]

    if "login_senha" in st.session_state:

        del st.session_state[
            "login_senha"
        ]

    st.query_params["pagina"] = "inicio"

    st.rerun()


# ============================================================
# PÁGINA INICIAL
# ============================================================

def mostrar_pagina_inicial():

    mostrar_logo()

    st.markdown(
        '<div class="titulo-principal">'
        'SISTEMA DE GESTÃO E ANÁLISE: BIBLIOTECA SESI SGA'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">'
        'Sistema de consulta, gestão e análise da biblioteca'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(
        [1, 2, 2, 1],
        gap="medium"
    )

    with col2:

        imagem_clicavel(
            IMAGEM_ACERVO,
            "acervo"
        )

    with col3:

        imagem_clicavel(
            IMAGEM_LOGIN,
            "login"
        )


# ============================================================
# ACERVO PÚBLICO
# ============================================================

def mostrar_acervo_publico():

    mostrar_logo()

    st.markdown(
        """
        <div class="titulo-principal">
            📚 ACERVO: CONSULTA DO CATÁLOGO
        </div>
        """,
        unsafe_allow_html=True
    )

    df_acervo = ler_acervo_salvo()

    if df_acervo is None or df_acervo.empty:

        st.warning(
            "📚 O acervo ainda não foi publicado."
        )

        if st.button(
            "← VOLTAR PARA INÍCIO",
            key="voltar_acervo_vazio",
            use_container_width=True
        ):

            ir_para("inicio")

        return

    df_acervo = normalizar_dataframe(
        df_acervo
    )

    campos_busca = [
        "Código",
        "Título",
        "Subtítulo",
        "Editora",
        "Localidade",
        "Ano"
    ]

    colunas_busca = {}

    for campo in campos_busca:

        coluna = buscar_coluna(
            df_acervo,
            [campo]
        )

        if coluna is not None:

            colunas_busca[campo] = coluna

    st.markdown(
        """
        <div class="titulo-secao">
            🔎 BUSCA: CONSULTE O ACERVO
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Escolha onde deseja realizar a busca:"
    )

    campos_disponiveis = [
        campo
        for campo in campos_busca
        if campo in colunas_busca
    ]

    if not campos_disponiveis:

        st.error(
            "❌ Não foram encontradas no acervo "
            "as colunas necessárias para a busca."
        )

        return

    campo_busca = st.radio(
        "Campo de busca",
        options=campos_disponiveis,
        horizontal=True,
        key="campo_busca_acervo",
        label_visibility="collapsed"
    )

    termo = st.text_input(
        "Digite sua busca",
        placeholder=(
            "Digite o código, título, subtítulo, "
            "editora, localidade ou ano..."
        ),
        key="busca_acervo"
    )

    df_exibicao = df_acervo.copy()

    if termo:

        coluna_real = colunas_busca[
            campo_busca
        ]

        df_exibicao = df_acervo[
            df_acervo[
                coluna_real
            ]
            .astype(str)
            .str.contains(
                termo,
                case=False,
                na=False,
                regex=False
            )
        ]

    colunas_exibicao = [
        "Código",
        "Título",
        "Subtítulo",
        "Editora",
        "Ano",
        "Localidade",
        "Tipo"
    ]

    colunas_resultado = {}

    for campo in colunas_exibicao:

        coluna = buscar_coluna(
            df_acervo,
            [campo]
        )

        if coluna is not None:

            colunas_resultado[
                campo
            ] = coluna

    resultado = pd.DataFrame(
        index=df_exibicao.index
    )

    for campo in colunas_exibicao:

        coluna_real = colunas_resultado.get(
            campo
        )

        if coluna_real is not None:

            resultado[campo] = (
                df_exibicao[
                    coluna_real
                ]
            )

        else:

            resultado[campo] = ""

    resultado = resultado.reset_index(
        drop=True
    )

    st.markdown(
        """
        <div class="subtitulo-secao">
            📚 RESULTADO: ACERVO ENCONTRADO
        </div>
        """,
        unsafe_allow_html=True
    )

    if termo:

        st.caption(
            f"{len(resultado)} registro(s) encontrado(s)."
        )

    st.dataframe(
        resultado,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    if st.button(
        "← VOLTAR PARA INÍCIO",
        key="voltar_acervo",
        use_container_width=True
    ):

        ir_para("inicio")


# ============================================================
# DADOS ATUAIS
# ============================================================

def mostrar_dados_atuais():

    st.markdown(
        """
        <div class="titulo-secao">
            DADOS ATUAIS: ANÁLISE DOS DADOS
        </div>
        """,
        unsafe_allow_html=True
    )

    arquivo_publicacoes = st.file_uploader(
        "📚 Relatório de publicações",
        type=["csv"],
        key="arquivo_publicacoes"
    )

    arquivo_movimentacao = st.file_uploader(
        "🔄 Relatório de movimentação",
        type=["csv"],
        key="arquivo_movimentacao"
    )

    arquivo_emprestimos = st.file_uploader(
        "📖 Relatório de empréstimos atuais",
        type=["csv"],
        key="arquivo_emprestimos"
    )

    df_publicacoes = None
    df_movimentacao = None
    df_emprestimos = None

    if arquivo_publicacoes:

        df_publicacoes = normalizar_dataframe(
            ler_csv(
                arquivo_publicacoes
            )
        )

    if arquivo_movimentacao:

        df_movimentacao = normalizar_dataframe(
            ler_csv(
                arquivo_movimentacao
            )
        )

    if arquivo_emprestimos:

        df_emprestimos = normalizar_dataframe(
            ler_csv(
                arquivo_emprestimos
            )
        )

    if (
        df_publicacoes is None
        and
        df_movimentacao is None
        and
        df_emprestimos is None
    ):

        st.info(
            "Envie os relatórios para visualizar "
            "a análise dos dados."
        )

        return

    # ========================================================
    # MÉTRICAS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        total_publicacoes = (
            len(df_publicacoes)
            if df_publicacoes is not None
            else 0
        )

        st.metric(
            "📚 Publicações",
            f"{total_publicacoes:,}".replace(
                ",",
                "."
            )
        )

    with col2:

        total_movimentacoes = (
            len(df_movimentacao)
            if df_movimentacao is not None
            else 0
        )

        st.metric(
            "🔄 Movimentações",
            f"{total_movimentacoes:,}".replace(
                ",",
                "."
            )
        )

    with col3:

        total_emprestimos = (
            len(df_emprestimos)
            if df_emprestimos is not None
            else 0
        )

        st.metric(
            "📖 Empréstimos atuais",
            f"{total_emprestimos:,}".replace(
                ",",
                "."
            )
        )

    # ========================================================
    # ABAS INTERNAS
    # ========================================================

    abas = st.tabs(
        [
            "📈 VISÃO GERAL",
            "📚 DADOS DO ACERVO",
            "🏆 RANKING",
            "🔄 MOVIMENTAÇÃO",
            "📖 EMPRÉSTIMOS ATUAIS",
            "📤 EXPORTAÇÃO"
        ]
    )

    # ========================================================
    # ABA 1 — VISÃO GERAL
    # ========================================================

    with abas[0]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                📈 VISÃO GERAL: DADOS CARREGADOS
            </div>
            """,
            unsafe_allow_html=True
        )

        if df_publicacoes is not None:

            st.write(
                "📚 Publicações:",
                len(df_publicacoes)
            )

        if df_movimentacao is not None:

            st.write(
                "🔄 Movimentações:",
                len(df_movimentacao)
            )

        if df_emprestimos is not None:

            st.write(
                "📖 Empréstimos atuais:",
                len(df_emprestimos)
            )

    # ========================================================
    # ABA 2 — DADOS DO ACERVO
    # ========================================================

    with abas[1]:

        if df_publicacoes is None:

            st.info(
                "Nenhum relatório de publicações enviado."
            )

        else:

            st.markdown(
                """
                <div class="subtitulo-secao">
                    📚 DADOS DO ACERVO: PUBLICAÇÕES
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="subtitulo-secao">
                    🔎 BUSCA: CONSULTE O ACERVO
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                "Escolha onde deseja realizar a busca:"
            )

            campos_busca = [
                "Código",
                "Título",
                "Subtítulo",
                "Editora",
                "Localidade",
                "Ano"
            ]

            colunas_busca = {}

            for campo in campos_busca:

                coluna = buscar_coluna(
                    df_publicacoes,
                    [campo]
                )

                if coluna is not None:

                    colunas_busca[campo] = coluna

            campos_disponiveis = [
                campo
                for campo in campos_busca
                if campo in colunas_busca
            ]

            if not campos_disponiveis:

                st.error(
                    "❌ Não foram encontradas no relatório "
                    "as colunas necessárias para a busca."
                )

            else:

                campo_busca = st.radio(
                    "Campo de busca",
                    options=campos_disponiveis,
                    horizontal=True,
                    key="campo_busca_publicacoes_admin",
                    label_visibility="collapsed"
                )

                termo = st.text_input(
                    "Digite sua busca",
                    placeholder=(
                        "Digite o código, título, subtítulo, "
                        "editora, localidade ou ano..."
                    ),
                    key="termo_publicacoes_admin"
                )

                df_exibicao = df_publicacoes.copy()

                if termo:

                    coluna_real = colunas_busca[
                        campo_busca
                    ]

                    df_exibicao = df_publicacoes[
                        df_publicacoes[
                            coluna_real
                        ]
                        .astype(str)
                        .str.contains(
                            termo,
                            case=False,
                            na=False,
                            regex=False
                        )
                    ]

                colunas_exibicao = [
                    "Código",
                    "Título",
                    "Subtítulo",
                    "Editora",
                    "Ano",
                    "Localidade",
                    "Tipo"
                ]

                colunas_resultado = {}

                for campo in colunas_exibicao:

                    coluna = buscar_coluna(
                        df_publicacoes,
                        [campo]
                    )

                    if coluna is not None:

                        colunas_resultado[
                            campo
                        ] = coluna

                resultado = pd.DataFrame(
                    index=df_exibicao.index
                )

                for campo in colunas_exibicao:

                    coluna_real = (
                        colunas_resultado.get(
                            campo
                        )
                    )

                    if coluna_real is not None:

                        resultado[campo] = (
                            df_exibicao[
                                coluna_real
                            ]
                        )

                    else:

                        resultado[campo] = ""

                resultado = resultado.reset_index(
                    drop=True
                )

                st.markdown(
                    """
                    <div class="subtitulo-secao">
                        📚 RESULTADO: ACERVO ENCONTRADO
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if termo:

                    st.caption(
                        f"{len(resultado)} "
                        f"registro(s) encontrado(s)."
                    )

                st.dataframe(
                    resultado,
                    use_container_width=True,
                    hide_index=True
                )

    # ========================================================
    # ABA 3 — RANKING
    # ========================================================

    with abas[2]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                🏆 RANKING: ALUNOS E LIVROS COM MAIS MOVIMENTAÇÕES
            </div>
            """,
            unsafe_allow_html=True
        )

        if df_movimentacao is None:

            st.info(
                "Envie o relatório de movimentação."
            )

        else:

            coluna_aluno = next(
                (
                    col
                    for col in df_movimentacao.columns
                    if normalizar_coluna(col) == "usuario"
                ),
                None
            )

            coluna_titulo = next(
                (
                    col
                    for col in df_movimentacao.columns
                    if normalizar_coluna(col) == "titulo"
                ),
                None
            )

            col_alunos, col_livros = st.columns(2)

            with col_alunos:

                st.markdown(
                    """
                    <div class="subtitulo-secao">
                        🏆 ALUNOS COM MAIS MOVIMENTAÇÕES
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if coluna_aluno is not None:

                    ranking_alunos = (
                        df_movimentacao[
                            coluna_aluno
                        ]
                        .astype(str)
                        .str.strip()
                        .replace(
                            "",
                            pd.NA
                        )
                        .dropna()
                        .value_counts()
                        .head(5)
                        .reset_index()
                    )

                    ranking_alunos.columns = [
                        "Aluno",
                        "Quantidade de movimentações"
                    ]

                    ranking_alunos.insert(
                        0,
                        "Posição",
                        range(
                            1,
                            len(ranking_alunos) + 1
                        )
                    )

                    st.dataframe(
                        ranking_alunos,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.error(
                        "❌ Não foi possível identificar "
                        "a coluna 'Usuário'."
                    )

            with col_livros:

                st.markdown(
                    """
                    <div class="subtitulo-secao">
                        📚 LIVROS MAIS EMPRESTADOS
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if coluna_titulo is not None:

                    ranking_livros = (
                        df_movimentacao[
                            coluna_titulo
                        ]
                        .astype(str)
                        .str.strip()
                        .replace(
                            "",
                            pd.NA
                        )
                        .dropna()
                        .value_counts()
                        .head(5)
                        .reset_index()
                    )

                    ranking_livros.columns = [
                        "Livro",
                        "Quantidade de empréstimos"
                    ]

                    ranking_livros.insert(
                        0,
                        "Posição",
                        range(
                            1,
                            len(ranking_livros) + 1
                        )
                    )

                    st.dataframe(
                        ranking_livros,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.error(
                        "❌ Não foi possível identificar "
                        "a coluna 'Título'."
                    )

    # ========================================================
    # ABA 4 — MOVIMENTAÇÃO
    # ========================================================

    with abas[3]:

        if df_movimentacao is None:

            st.info(
                "Nenhum relatório de movimentação enviado."
            )

        else:

            st.markdown(
                """
                <div class="subtitulo-secao">
                    🔄 MOVIMENTAÇÃO: REGISTROS
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                df_movimentacao,
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # ABA 5 — EMPRÉSTIMOS ATUAIS
    # ========================================================

    with abas[4]:

        if df_emprestimos is None:

            st.info(
                "Nenhum relatório de empréstimos enviado."
            )

        else:

            st.markdown(
                """
                <div class="subtitulo-secao">
                    📖 EMPRÉSTIMOS ATUAIS: REGISTROS
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                df_emprestimos,
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # ABA 6 — EXPORTAÇÃO
    # ========================================================

    with abas[5]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                📤 EXPORTAÇÃO: DOWNLOAD DOS DADOS
            </div>
            """,
            unsafe_allow_html=True
        )

        if df_publicacoes is not None:

            st.download_button(
                "📥 Baixar publicações",
                data=csv_download(
                    df_publicacoes
                ),
                file_name="publicacoes.csv",
                mime="text/csv"
            )

        if df_movimentacao is not None:

            st.download_button(
                "📥 Baixar movimentação",
                data=csv_download(
                    df_movimentacao
                ),
                file_name="movimentacao.csv",
                mime="text/csv"
            )

        if df_emprestimos is not None:

            st.download_button(
                "📥 Baixar empréstimos",
                data=csv_download(
                    df_emprestimos
                ),
                file_name="emprestimos.csv",
                mime="text/csv"
            )


# ============================================================
# MOVIMENTAÇÃO MENSAL
# ============================================================

def mostrar_movimentacao_mensal():

    st.markdown(
        """
        <div class="titulo-secao">
            📅 MOVIMENTAÇÃO MENSAL: ANÁLISE POR PERÍODO
        </div>
        """,
        unsafe_allow_html=True
    )

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    arquivos = {}

    for mes in meses:

        arquivos[mes] = st.file_uploader(
            f"📅 {mes}",
            type=["csv"],
            key=f"mov_{mes}"
        )

    dados = []

    for mes in meses:

        arquivo = arquivos[mes]

        if arquivo is not None:

            df = ler_csv(
                arquivo
            )

            if df is not None:

                df = preparar_movimentacao_mensal(
                    df,
                    mes
                )

                dados.append(df)

    if not dados:

        st.info(
            "Envie os relatórios mensais para "
            "realizar a análise."
        )

        return

    consolidado = pd.concat(
        dados,
        ignore_index=True
    )

    # ========================================================
    # MÉTRICAS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Movimentações",
            f"{len(consolidado):,}".replace(
                ",",
                "."
            )
        )

    with col2:

        st.metric(
            "📅 Meses carregados",
            len(dados)
        )

    with col3:

        total_atrasos = (
            consolidado[
                "Dias de atraso"
            ]
            .gt(0)
            .sum()
        )

        st.metric(
            "⚠️ Atrasos",
            f"{total_atrasos:,}".replace(
                ",",
                "."
            )
        )

    with col4:

        dias_atraso = consolidado[
            "Dias de atraso"
        ].sum()

        st.metric(
            "⏱️ Dias de atraso",
            f"{dias_atraso:,}".replace(
                ",",
                "."
            )
        )

    # ========================================================
    # ABAS
    # ========================================================

    abas = st.tabs(
        [
            "📊 RESUMO",
            "📅 POR MÊS",
            "📚 LIVROS",
            "👤 ALUNOS",
            "⚠️ ATRASOS",
            "🕐 HORÁRIOS",
            "📋 DADOS CONSOLIDADOS"
        ]
    )

    # ========================================================
    # RESUMO
    # ========================================================

    with abas[0]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                📊 RESUMO: VISÃO CONSOLIDADA
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            consolidado.describe(
                include="all"
            ).transpose(),
            use_container_width=True
        )

    # ========================================================
    # POR MÊS
    # ========================================================

    with abas[1]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                📅 POR MÊS: MOVIMENTAÇÕES MENSAIS
            </div>
            """,
            unsafe_allow_html=True
        )

        movimentacoes_mes = (
            consolidado[
                "Mês"
            ]
            .value_counts()
            .reindex(
                meses,
                fill_value=0
            )
            .reset_index()
        )

        movimentacoes_mes.columns = [
            "Mês",
            "Quantidade de movimentações"
        ]

        st.dataframe(
            movimentacoes_mes,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # LIVROS
    # ========================================================

    with abas[2]:

        coluna_livro = buscar_coluna(
            consolidado,
            [
                "Livro",
                "Título",
                "Titulo",
                "Obra"
            ]
        )

        if coluna_livro:

            livros = (
                consolidado[
                    coluna_livro
                ]
                .value_counts()
                .head(20)
                .reset_index()
            )

            livros.columns = [
                "Livro",
                "Quantidade"
            ]

            st.markdown(
                """
                <div class="subtitulo-secao">
                    📚 LIVROS: OBRAS MAIS MOVIMENTADAS
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                livros,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Não foi possível identificar "
                "a coluna de livro."
            )

    # ========================================================
    # ALUNOS
    # ========================================================

    with abas[3]:

        coluna_aluno = next(
            (
                col
                for col in consolidado.columns
                if normalizar_coluna(col) == "usuario"
            ),
            None
        )

        if coluna_aluno:

            alunos = (
                consolidado[
                    coluna_aluno
                ]
                .value_counts()
                .head(20)
                .reset_index()
            )

            alunos.columns = [
                "Aluno",
                "Quantidade"
            ]

            st.markdown(
                """
                <div class="subtitulo-secao">
                    👤 ALUNOS: MAIORES MOVIMENTAÇÕES
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                alunos,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Não foi possível identificar "
                "a coluna 'Usuário'."
            )

    # ========================================================
    # ATRASOS
    # ========================================================

    with abas[4]:

        atrasos = consolidado[
            consolidado[
                "Dias de atraso"
            ] > 0
        ]

        st.markdown(
            """
            <div class="subtitulo-secao">
                ⚠️ ATRASOS: DEVOLUÇÕES EM ATRASO
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            atrasos,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # HORÁRIOS
    # ========================================================

    with abas[5]:

        horarios = (
            consolidado[
                "Horário"
            ]
            .value_counts()
            .reset_index()
        )

        horarios.columns = [
            "Horário",
            "Quantidade"
        ]

        st.markdown(
            """
            <div class="subtitulo-secao">
                🕐 HORÁRIOS: DISTRIBUIÇÃO DAS MOVIMENTAÇÕES
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            horarios,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # DADOS CONSOLIDADOS
    # ========================================================

    with abas[6]:

        st.markdown(
            """
            <div class="subtitulo-secao">
                📋 DADOS CONSOLIDADOS: REGISTROS
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            consolidado,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PUBLICAR ACERVO
# ============================================================

def mostrar_publicacao_acervo():

    st.markdown(
        """
        <div class="titulo-secao">
            📤 PUBLICAR ACERVO: ATUALIZAÇÃO DO CATÁLOGO
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Envie o arquivo CSV do acervo para "
        "substituir o acervo atualmente publicado."
    )

    arquivo = st.file_uploader(
        "📚 Selecionar arquivo do acervo",
        type=["csv"],
        key="arquivo_acervo_admin"
    )

    if arquivo is not None:

        df = ler_csv(
            arquivo
        )

        if df is None:

            st.error(
                "❌ Não foi possível ler o arquivo."
            )

            return

        df = normalizar_dataframe(
            df
        )

        st.success(
            f"Arquivo carregado com "
            f"{len(df):,} registros.".replace(
                ",",
                "."
            )
        )

        st.markdown(
            """
            <div class="subtitulo-secao">
                👁️ PRÉ-VISUALIZAÇÃO: ACERVO
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            df.head(100),
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "🚀 PUBLICAR ACERVO",
            key="publicar_acervo",
            use_container_width=True
        ):

            try:

                salvar_acervo(
                    df
                )

                st.success(
                    "✅ Acervo publicado com sucesso!"
                )

                st.info(
                    f"Atualizado em: "
                    f"{obter_data_acervo()}"
                )

            except Exception as erro:

                st.error(
                    f"❌ Erro ao publicar o acervo: "
                    f"{erro}"
                )

    else:

        df_atual = ler_acervo_salvo()

        if df_atual is not None:

            st.markdown(
                """
                <div class="subtitulo-secao">
                    📚 ACERVO ATUALMENTE PUBLICADO: INFORMAÇÕES
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Registros",
                    f"{len(df_atual):,}".replace(
                        ",",
                        "."
                    )
                )

            with col2:

                st.metric(
                    "Última atualização",
                    obter_data_acervo()
                )


# ============================================================
# ADMINISTRAÇÃO
# ============================================================

def mostrar_administracao():

    mostrar_logo()

    st.markdown(
        """
        <div class="titulo-principal">
            BIBLIOTECA: SISTEMA DE GESTÃO E ANÁLISE
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [5, 1]
    )

    with col2:

        if st.button(
            "🚪 SAIR",
            key="btn_sair",
            use_container_width=True
        ):

            sair()

    abas_principais = st.tabs(
        [
            "📊 DADOS ATUAIS",
            "📅 MOVIMENTAÇÃO MENSAL",
            "📤 PUBLICAR ACERVO"
        ]
    )

    with abas_principais[0]:

        mostrar_dados_atuais()

    with abas_principais[1]:

        mostrar_movimentacao_mensal()

    with abas_principais[2]:

        mostrar_publicacao_acervo()


# ============================================================
# CONTROLE DE SESSÃO
# ============================================================

if "autenticado" not in st.session_state:

    st.session_state.autenticado = False


# ============================================================
# PÁGINAS VÁLIDAS
# ============================================================

paginas_validas = [
    "inicio",
    "acervo",
    "login",
    "administracao"
]


# ============================================================
# RECUPERAR PÁGINA
# ============================================================

pagina_url = st.query_params.get(
    "pagina"
)

if pagina_url in paginas_validas:

    pagina_atual = pagina_url

else:

    pagina_atual = "inicio"


# ============================================================
# ROTEAMENTO
# ============================================================

if pagina_atual == "inicio":

    mostrar_pagina_inicial()

elif pagina_atual == "acervo":

    mostrar_acervo_publico()

elif pagina_atual == "login":

    fazer_login()

elif pagina_atual == "administracao":

    if st.session_state.autenticado:

        mostrar_administracao()

    else:

        st.query_params["pagina"] = "login"

        st.rerun()


# ============================================================
# RODAPÉ
# ============================================================

mostrar_rodape()