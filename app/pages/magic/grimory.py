# ------------------------------------------------------------------------------------------------ #
# IMPORTS
import os
import streamlit as st
import pandas as pd
import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from app.src.data_loader import read_excel_data
from app.components.filters import dynamic_filters, search_box

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES

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

def grimory(df_dict: dict):
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

    selected_sheet = st.selectbox(
        "Selecione um arquétipo do grimório:",
        list(df_dict.keys()),
        index=0
    )

    df = df_dict[selected_sheet]
    df = df.fillna('')

    # Filtros
    with st.expander("🎯 Filtros de Feitiços"):

        df = search_box(
            df=df,
            label="🔍 Busca de Feitiços",
            column="spell_name"
        )

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

    # Tipo de Visualização
    st.sidebar.header("⚙️ Opções de Exibição")

    # Modo de visualização
    view_mode = st.sidebar.selectbox(
        "Modo de Visualização:",
        ["Ficha Completa", "Lista Compacta"]
    )

    # Renderização
    st.header(f"{selected_sheet} ({arcanum_dict[selected_sheet]})", divider="grey")

    try:
        if view_mode == "Ficha Completa":
            render_spell_full(df)
        else:
            render_spell_list(df)

    except Exception as e:
        st.error("Falha ao renderizar os feitiços.")
        return

def archetype_overview():
    """
    Função simples que exibe um dicionário com nomes simplificados
    dos arquétipos mágicos em duas colunas balanceadas.
    """

    # Ordena alfabeticamente pelas chaves (arquétipos)
    items = sorted(arcanum_dict.items(), key=lambda x: x[0])

    # Divide em duas partes o mais igual possível
    mid = (len(items) + 1) // 2
    col1_items = items[:mid]
    col2_items = items[mid:]

    col1, col2 = st.columns(2)

    with col1:
        for k, v in col1_items:
            st.markdown(f"**{k}** → `{v}`")

    with col2:
        for k, v in col2_items:
            st.markdown(f"**{k}** → `{v}`")

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    """
    Página principal que cria um menu lateral para seleção entre
    o grimório e a visão simples dos arquétipos.
    """

    df_dict = read_excel_data('grimory.xlsx')

    options = ["Arquétipos", "Grimório"]


    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["book", "list-ul"],
        default_index=0,
        orientation="horizontal"
    )

    # Roteamento das páginas
    if selection == options[0]:
        archetype_overview()
    elif selection == options[1]:
        grimory(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()
