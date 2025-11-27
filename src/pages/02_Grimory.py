# ------------------------------------------------------------------------------------------------ #
# IMPORTS

import os
import streamlit as st
import pandas as pd
import numpy as np
import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from src.data.data_loader import ExcelReader
from utils import get_project_folder, dynamic_filters, search_box

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES

logs_folder = get_project_folder('src')
data_folder = get_project_folder('data')

# Required columns for spell sheets
required_columns = [
    "spell_id", "spell_name", "spell_tier", "spell_type", "spell_difficulty",
    "spell_requirements", "spell_cost", "spell_cast_time", "spell_range",
    "spell_target_type", "spell_effect_area", "spell_duration",
    "spell_description", "spell_observation", "spell_school"
]

arcanum_dict = {
    "Arcanomancia": "Arcano",
    "Somatomancia": "Corpo",
    "Hemomancia": "Sangue",
    "Zoomancia": "Fauna",
    "Fitomancia": "Flora",
    "Melomancia": "Bardo",
    "Imbuomancia": "Encantamento",
    "Eidomancia": "Ilusão",
    "Restauromancia": "Restauração",
    "Hidromancia": "Água",
    "Aeromancia": "Ar",
    "Eletromancia": "Eletricidade",
    "Piromancia": "Fogo",
    "Geomancia": "Terra",
    "Hagiomancia": "Sagrado",
    "Necromancia": "Necro",
    "Umbromancia": "Sombra",
    "Espaciomancia": "Espaço",
    "Cronomancia": "Tempo",
    "Psiquemancia": "Mente",
    "Kinetomancia": "Movimento",
    "Sonoromancia": "Som"
}

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES

def filter_sheet_names(sheet_list: list, exclude_list: list) -> list:
    """
    Filtra da lista todas as sheet_names contidas na exclude_list.
    Retorna a lista limpa de abas que o usuário poderá selecionar.
    """
    return [s for s in sheet_list if s not in exclude_list]

def validate_columns(df: pd.DataFrame, log4me) -> bool:
    """
    Verifica se todas as colunas obrigatórias estão presentes.
    Se faltar alguma, retorna False e loga o erro.
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        log4me.error(f"Missing columns in sheet: {missing}")
        return False

    log4me.info("All required columns found.")
    return True

def render_spell_requirements(req_string: str):
    """
    Converte a string de requisitos em uma lista limpa.
    """
    if not isinstance(req_string, str) or req_string.strip() == "":
        return []

    return [item.strip() for item in req_string.split(",")]

def render_spell_list(df: pd.DataFrame):
    """
    Renderiza uma visão compacta dos feitiços.
    Mostra apenas informações essenciais em formato de tabela.
    """
    st.subheader("Lista Compacta")

    compact_df = df[
        ["spell_id", "spell_name", "spell_tier", "spell_type", "spell_difficulty",
         "spell_cost", "spell_cast_time", "spell_range", "spell_target_type",
         "spell_effect_area", "spell_duration", "spell_school"]
    ].sort_values("spell_id")

    st.dataframe(compact_df, use_container_width=True)

def render_spell_full(df: pd.DataFrame):
    """
    Renderiza cada feitiço em modo detalhado (ficha completa),
    com todos os campos e layout visual expandido.
    """
    df_sorted = df.sort_values(by="spell_id")

    st.subheader("Ficha Completa")

    for _, row in df_sorted.iterrows():

        col1, col2, col3 = st.columns(3)
        with col1: st.write(f"**ID:** {row['spell_id']}")
        with col2: st.write(f"**Nome:** {row['spell_name']}")
        with col3: st.write(f"**Duração:** {row['spell_duration']}")

        col1, col2, col3 = st.columns(3)
        with col1: st.write(f"**Tier:** {row['spell_tier']}")
        with col2: st.write(f"**Tipo:** {row['spell_type']}")
        with col3: st.write(f"**Dificuldade:** {row['spell_difficulty']}")

        col1, col2, col3 = st.columns(3)
        with col1: st.write(f"**Alcance:** {row['spell_range']}")
        with col2: st.write(f"**Alvo:** {row['spell_target_type']}")
        with col3: st.write(f"**Área:** {row['spell_effect_area']}")

        # Custo de Mana
        st.write(f"**Custo de Mana:** {row['spell_cost']}")

        # Descrição e Observações
        col1, col2 = st.columns(2)
        with col1: st.markdown(f"**Descrição:**\n\n{row['spell_description']}")
        with col2: st.markdown(f"**Observação:**\n\n{row['spell_observation']}")

        # --------------------------- Requirements ----------------------------- #
        st.markdown("**Requisitos:**")
        req_list = render_spell_requirements(row["spell_requirements"])
        if req_list:
            for r in req_list:
                st.write(f"- {r}")
        else:
            st.write("- Nenhum")


        st.markdown("---")

# ------------------------------------------------------------------------------------------------ #
#   FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT

def grimory():
    """
    Página principal do Streamlit responsável por:
    - Ler o arquivo grimory.xlsx usando a classe ExcelReader
    - Filtrar abas indesejadas
    - Permitir selecionar uma aba válida
    - Validar colunas obrigatórias
    - Aplicar filtros dinâmicos + campo de busca + ordenação
    - Permitir modo de visualização (Ficha Completa / Lista Compacta)
    - Renderizar o conteúdo final
    """

    st.title("Grimório de Ytarria")

    # Caminho fixo do arquivo
    file_path = os.path.join(data_folder, "grimory.xlsx")

    # Inicializa o leitor
    excel_reader = ExcelReader(log_dir=logs_folder, file_path=file_path)
    log4me = excel_reader.get_logger()

    # ----------------------------------------------------------------------------------------- #
    # LÊ OS NOMES DAS ABAS
    # ----------------------------------------------------------------------------------------- #
    try:
        sheet_names = excel_reader.get_sheet_names()
        sheet_names = sorted(sheet_names)
        invalid_sheet_names = [s for s in sheet_names if s and s[0].isdigit()]
    except Exception as e:
        log4me.error(f"Error reading sheet names: {e}")
        st.error("Falha ao ler os nomes das abas.")
        return

    if not sheet_names:
        st.error(f"Nenhuma aba encontrada no arquivo: {file_path}")
        return

    default_exclude = ["data_validation"]
    default_exclude.extend(invalid_sheet_names)
    cleaned_sheet_names = filter_sheet_names(sheet_names, default_exclude)

    if not cleaned_sheet_names:
        st.error("Nenhuma aba válida após a filtragem.")
        return

    # ----------------------------------------------------------------------------------------- #
    # SELECTBOX PARA ESCOLHER A ABA
    # ----------------------------------------------------------------------------------------- #
    selected_sheet = st.selectbox(
        "Selecione um arquétipo do grimório:",
        cleaned_sheet_names,
        index=0
    )

    # ----------------------------------------------------------------------------------------- #
    # CARREGA APENAS A ABA SELECIONADA
    # ----------------------------------------------------------------------------------------- #
    try:
        df_dict = excel_reader.load_sheets(
            ignore_sheets=[s for s in sheet_names if s != selected_sheet]
        )
    except Exception as e:
        log4me.error(f"Error loading sheet {selected_sheet}: {e}")
        st.error("Falha ao carregar a aba selecionada.")
        return

    if selected_sheet not in df_dict:
        st.error("A aba selecionada não pôde ser carregada.")
        return

    df = df_dict[selected_sheet]
    df = df.fillna('')

    # ----------------------------------------------------------------------------------------- #
    # VALIDA COLUNAS
    # ----------------------------------------------------------------------------------------- #
    if not validate_columns(df, log4me):
        st.error("Formato da aba inválido. Colunas obrigatórias ausentes.")
        return


    # ----------------------------------------------------------------------------------------- #
    # FILTROS DINÂMICOS
    # ----------------------------------------------------------------------------------------- #

    with st.expander("🎯 Filtros de Feitiços"):

    # ----------------------------------------------------------------------------------------- #
    # SEARCH BOX
    # ----------------------------------------------------------------------------------------- #

        df = search_box(
            df=df,
            label="🔍 Busca de Feitiços",
            column="spell_name"
        )

    # ----------------------------------------------------------------------------------------- #
    # FILTROS (TYPE, TIER, DIFFICULTY)
    # ----------------------------------------------------------------------------------------- #

        filter_config = {
            "Filtrar por Tipo:": {
                "column": "spell_type",
                "type": "multiselect",
                "default": []
            },
            "Filtrar por Círculo (Tier):": {
                "column": "spell_tier",
                "type": "multiselect",
                "default": [],
                "sort_order": ["Básico", "Comum", "Avançado", "Raro", "Lendário", "Proíbido"]
            },
            "Filtrar por Dificuldade:": {
                "column": "spell_difficulty",
                "type": "multiselect",
                "default": [],
                "sort_order": ["F", "M", "D", "MD"]
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning("Nenhum feitiço encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # ----------------------------------------------------------------------------------------- #
    # SIDEBAR: ORDENAÇÃO + MODO DE VISUALIZAÇÃO
    # ----------------------------------------------------------------------------------------- #

    st.sidebar.header("⚙️ Opções de Exibição")

    # Modo de visualização
    view_mode = st.sidebar.selectbox(
        "Modo de Visualização:",
        ["Ficha Completa", "Lista Compacta"]
    )

    # ----------------------------------------------------------------------------------------- #
    # RENDERIZAÇÃO FINAL
    # ----------------------------------------------------------------------------------------- #

    st.header(f"{selected_sheet} ({arcanum_dict[selected_sheet]})", divider="grey")

    try:
        if view_mode == "Ficha Completa":
            render_spell_full(df)
        else:
            render_spell_list(df)

    except Exception as e:
        log4me.error(f"Error rendering spells in mode {view_mode}: {e}")
        st.error("Falha ao renderizar os feitiços.")
        return

def archetype_overview():
    """
    Função simples que exibe um dicionário com nomes simplificados
    dos arquétipos mágicos em ordem alfabética.
    """
    st.title("📚 Arquétipos Mágicos – Visão Geral")

    st.write("Abaixo estão os arquétipos e seu nome simplificado:")

    # Ordena alfabeticamente pelas chaves (arquétipos)
    for k, v in sorted(arcanum_dict.items(), key=lambda x: x[0]):
        st.markdown(f"**{k}** → `{v}`")

    st.info("Este módulo é apenas uma visualização simples, ordenada alfabeticamente.")

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    """
    Página principal que cria um menu lateral para seleção entre
    o grimório e a visão simples dos arquétipos.
    """

    with st.sidebar:
        st.markdown("### 📁 Navegação")
        selection = option_menu(
            menu_title=None,
            options=["Arquétipos", "Grimório"],
            icons=["book", "list-ul"],
            default_index=0,
        )

    # Roteamento das páginas
    if selection == "Arquétipos":
        archetype_overview()
    elif selection == "Grimório":
        grimory()

# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    main()
