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
# FUNÇÕES AUXILIARES

def render_skills_full(df: pd.DataFrame):
    """
    Renderiza cada as vantagens e desvantagens em modo detalhado,
    com todos os campos e layout visual expandido.
    """
    df_sorted = df.sort_values(by="skill_id")

    for _, row in df_sorted.iterrows():

        with st.expander(f"{row['skill_box_name']}"):

            col1, col2 = st.columns(2)
            with col1: st.write(f"**ID:** {row['skill_id']}")
            with col2: st.write(f"**Nome:** {row['skill_name']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Categoria:** {row['skill_category']}")
            with col2:
                st.write(f"**Tipo:** {'Mental' if row['skill_type'] == 'M' else 'Física'}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Dificuldade:** {row['skill_difficulty']}")
            with col2: st.write(f"**Status Base:** {row['skill_base_status']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Nível Pré-definido:** {row['skill_pre_defined_level']}")
            with col2: st.write(f"**Pré-requisitos:** {row['skill_prerequisite']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Fonte:** {row['skill_source_book']}")
            with col2: st.write(f"**Página:** {row['skill_source_page']}")

            st.markdown(f"**Descrição:**\n\n{row['skill_description']}")

def render_skills_list(df: pd.DataFrame):
    """
    Renderiza uma visão compacta dos feitiços.
    Mostra apenas informações essenciais em formato de tabela.
    """
    st.subheader("Lista Compacta")

    compact_df = df[
        ['skill_id', 'skill_name', 'skill_type', 'skill_difficulty',
         'skill_base_status', 'skill_source_book', 'skill_source_page']
    ].sort_values('skill_id')

    st.dataframe(compact_df, use_container_width=True)

# ------------------------------------------------------------------------------------------------ #
#   FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT

def skills(df_dict: dict) -> None:
    """Perícias"""

    df = df_dict["skills"]
    df = df.fillna('').convert_dtypes()

    # Filtros
    skill_categories = df['skill_category'].unique().tolist()

    selected_category = st.selectbox(
        "Selecione uma categoria de perícias:",
        skill_categories,
        index=0
    )

    df_category = df[df['skill_category'] == selected_category]

    with st.expander(f"🎯 Filtros de Perícias"):

        df_category = search_box(
            df=df_category,
            label=f"🔍 Busca de Perícias",
            column="skill_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": "skill_type",
                "type": "multiselect",
                "default": []
            },

            "Filtrar por Dificuldade:": {
                "column": "skill_difficulty",
                "type": "multiselect",
                "default": [],
                "sort_order": ["F", "M", "D", "MD"]
            }
        }

        df_category, selected_filters = dynamic_filters(df_category, filter_config)

        if df_category.empty:
            st.warning(f"Nenhuma Perícia encontrada com os filtros aplicados.")
            return

    # Sidebar
    st.sidebar.header("⚙️ Opções de Exibição")

    # Modo de visualização
    view_mode = st.sidebar.selectbox(
        "Modo de Visualização:",
        ["Ficha Completa", "Lista Compacta"]
    )

    # Renderização
    st.header(f"{selected_category}", divider="grey")

    try:
        if view_mode == "Ficha Completa":
            render_skills_full(df_category)
        else:
            render_skills_list(df_category)

    except Exception as e:
        st.error(f"Falha ao renderizar perícias.")
        return

def skills_cost_in_points(df_dict: dict) -> None:
    """
    Função simples que exibe um as regras de custo em pontos e aperfeiçoamento de perícias.
    """

    skills_overview = "overview"
    skills_mental = "mental"
    skills_physical = "physical"

    st.subheader("Custo em Pontos", divider="grey")

    # ----------------------------------------------------------------------------------------- #
    # 1 - REGRAS E CUSTOS DOS NÍVEIS DE HABILIDADE QUANTO SUA CATEGORIA
    # ----------------------------------------------------------------------------------------- #

    with st.expander("Perícias Físicas"):

        df_physical = df_dict[skills_physical]
        df_physical = df_physical.fillna('').convert_dtypes()
        df_physical.rename(columns={"skill_final_level": "Nível de Habilidade"}, inplace=True)

        st.dataframe(df_physical, use_container_width=True, hide_index=True)

    # ----------------------------------------------------------------------------------------- #

    with st.expander("Perícias Mentais"):

        df_mental = df_dict[skills_mental]
        df_mental = df_mental.fillna('').convert_dtypes()
        df_mental.rename(columns={"skill_final_level": "Nível de Habilidade"}, inplace=True)

        st.dataframe(df_mental, use_container_width=True, hide_index=True)

    # ----------------------------------------------------------------------------------------- #
    # 1.1 SIGNIFICADO DO NÍVEL DE HABILIDADE COM AS PERÍCIAS
    # ----------------------------------------------------------------------------------------- #

    with st.expander("O que seu nível de perícia significa?"):

        df_overview = df_dict[skills_overview]
        df_overview = df_overview.fillna('').convert_dtypes()

        df_sorted = df_overview.sort_values(by="skill_level")

        # Cabeçalho (fora do loop)
        col1, col2, col3 = st.columns(3)
        col1.markdown("**Nível de Habilidade (NH)**")
        col2.markdown("**Nomenclatura do NH**")
        col3.markdown("**Descrição**")

        st.divider()

        # Linhas
        for _, row in df_sorted.iterrows():
            col1, col2, col3 = st.columns(3)
            col1.write(row["skill_level"])
            col2.write(row["skill_level_term"])
            col3.write(row["skill_level_description"])

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    """
    Página principal que cria um menu lateral para seleção entre
    o grimório e a visão simples dos arquétipos.
    """

    df_dict = read_excel_data('skills.xlsx')

    options = ["Aprendendo Perícias", "Perícias"]

    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["book", "list-ul"],
        default_index=0,
        orientation="horizontal"
    )

    # Roteamento das páginas
    if selection == options[0]:
        skills_cost_in_points(df_dict)
    elif selection == options[1]:
        skills(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()