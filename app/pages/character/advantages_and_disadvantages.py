# ------------------------------------------------------------------------------------------------ #
# IMPORTS

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

def render_view_full(view: str ,df: pd.DataFrame):
    """
    Renderiza cada as vantagens e desvantagens em modo detalhado,
    com todos os campos e layout visual expandido.
    """
    df_sorted = df.sort_values(by=f"{view}_id")

    for _, row in df_sorted.iterrows():

        with st.expander(f"{row[f'{view}_box_name']}"):

            col1, col2 = st.columns(2)
            with col1: st.write(f"**ID:** {row[f'{view}_id']}")
            with col2: st.write(f"**Nome:** {row[f'{view}_name']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Custo:** {row[f'{view}_cost']}")
            with col2: st.write(f"**Tipo:** {row[f'{view}_type']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Fonte:** {row[f'{view}_source_book']}")
            with col2: st.write(f"**Página:** {row[f'{view}_source_page']}")

            st.markdown(f"**Descrição:**\n\n{row[f'{view}_description']}")

def render_view_list(view: str, df: pd.DataFrame):
    """
    Renderiza uma visão compacta dos feitiços.
    Mostra apenas informações essenciais em formato de tabela.
    """
    st.subheader("Lista Compacta")

    compact_df = df[
        [f'{view}_id', f'{view}_name', f'{view}_type', f'{view}_cost',
         f'{view}_source_book', f'{view}_source_page']
    ].sort_values(f'{view}_id')

    st.dataframe(compact_df, use_container_width=True)

# ------------------------------------------------------------------------------------------------ #
#   FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT

def advantages(df_dict: dict) -> None:
    """Vantagens"""

    df = df_dict["advantages"]
    df = df.fillna('')

    # Filtros
    with st.expander(f"🎯 Filtros de Vantages"):

        df = search_box(
            df=df,
            label=f"🔍 Busca de Vantages",
            column=f"advantage_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": f"advantage_type",
                "type": "multiselect",
                "default": []
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning(f"Nenhuma Vantagem encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # Sidebar
    st.sidebar.header("⚙️ Opções de Exibição")

    # Modo de visualização
    view_mode = st.sidebar.selectbox(
        "Modo de Visualização:",
        ["Ficha Completa", "Lista Compacta"]
    )

    # Renderização
    try:
        if view_mode == "Ficha Completa":
            render_view_full("advantage", df)
        else:
            render_view_list("advantage", df)

    except Exception as e:
        st.error(f"Falha ao renderizar Vantagens.")
        return

def disadvantages(df_dict: dict) -> None:
    """Desvantagens"""

    df = df_dict["disadvantages"]
    df = df.fillna('')

    # Filtros
    with st.expander(f"🎯 Filtros de Desvantagens"):

        df = search_box(
            df=df,
            label=f"🔍 Busca de Desvantagens",
            column=f"disadvantage_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": f"disadvantage_type",
                "type": "multiselect",
                "default": []
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning(f"Nenhuma Vantagem encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # Sidebar
    st.sidebar.header("⚙️ Opções de Exibição")

    # Modo de visualização
    view_mode = st.sidebar.selectbox(
        "Modo de Visualização:",
        ["Ficha Completa", "Lista Compacta"]
    )

    # Renderização
    try:
        if view_mode == "Ficha Completa":
            render_view_full("disadvantage", df)
        else:
            render_view_list("disadvantage", df)

    except Exception as e:
        st.error(f"Falha ao renderizar Desvantagens.")
        return

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    """
    Página principal que cria um menu lateral para seleção entre
    o grimório e a visão simples dos arquétipos.
    """

    df_dict = read_excel_data("advantages_and_disadvantages.xlsx")

    options = ["Vantagens", "Desvantagens"]


    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["1-square-fill", "2-square-fill"],
        default_index=0,
        orientation="horizontal"
    )

    # Roteamento das páginas
    if selection == options[0]:
        advantages(df_dict)
    elif selection == options[1]:
        disadvantages(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()