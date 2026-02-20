# ------------------------------------------------------------------------------------------------ #
# IMPORTS

import os
import math
import streamlit as st
import pandas as pd
import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from app.src.data_loader import read_excel_data
from app.components.filters import search_box

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES

def calculate_hex(length):
    """ Função para converter comprimento em Hex """
    if length < 1:
        return 1
    return math.floor((length + 1) / 2) + 1

def render_weapons_full(view: str ,df: pd.DataFrame):
    """
    Renderiza cada arma em modo detalhado, com todos os campos e layout visual expandido.
    """
    if view == "Armas Corpo-a-Corpo":
        # Cria nova coluna de alcance em Hex
        df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)
        df_sorted = df.sort_values(by=f"weapon_id")

        for _, row in df_sorted.iterrows():

            st.subheader(f"{row['weapon_name']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Nome:** {row['weapon_name']}")
            with col2: st.write(f"**Perícia:** {row['weapon_skill']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Modificador BAL:** {row['weapon_bal_modifier']}")
            with col2: st.write(f"**Modificador GDP:** {row['weapon_gdp_modifier']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Peso:** {row['weapon_weight']} kg")
            with col2: st.write(f"**Comprimento:** {row['weapon_length']} m")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Preço Médio:** {row['weapon_price']} moedas")
            with col2: st.write(f"**Alcance:** {row['weapon_range_hex']} Hex")


            col1, col2 = st.columns(2)
            with col1: st.write(f"**ST Mínima:** {row['weapon_min_strength']}")
            with col2: st.write(f"**Tipos de Dano:** {row['weapon_damage_type']}")

            st.markdown(f"**Descrição:**\n\n{row['weapon_description']}")

            st.markdown("***")

    elif view == "Armas de Longa Distância":

        df_sorted = df.sort_values(by=f"weapon_id")

        for _, row in df_sorted.iterrows():

            st.subheader(f"{row['weapon_name']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Nome:** {row['weapon_name']}")
            with col2: st.write(f"**Perícia:** {row['weapon_skill']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Modificador GDP:** {row['weapon_gdp_modifier']}")
            with col2: st.write(f"**Tempo de Recarga:** {row['weapon_reload_speed']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**TR:** {row['weapon_tr']}")
            with col2: st.write(f"**Prec:** {row['weapon_prec']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Peso:** {row['weapon_weight']} kg")
            with col2: st.write(f"**Comprimento:** {row['weapon_length']} m")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Preço Médio:** {row['weapon_price']} Moedas")
            with col2: st.write(f"**Preço Médio Munição:** {row['weapon_munition_price']} Moedas")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**ST Mínima:** {row['weapon_min_strength']}")
            with col2: st.write(f"**Tipos de Dano:** {row['weapon_damage_type']}")

            col1, col2 = st.columns(2)
            with col1: st.write(f"**Distância ½:** {row['weapon_half_distance']}")
            with col2: st.write(f"**Distância Max:** {row['weapon_max_distance']}")

            st.markdown(f"**Descrição:**\n\n{row['weapon_description']}")

            st.markdown("***")

def render_weapons_list(view: str, df: pd.DataFrame):
    """
    Renderiza uma visão compacta das armas.
    Mostra apenas informações essenciais em formato de tabela.
    """
    st.subheader("Lista Compacta")

    if view == "Armas Corpo-a-Corpo":

        # Cria nova coluna de alcance em Hex
        df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)

        compact_df = df[[
                "weapon_id",
                "weapon_type",
                "weapon_name",
                "weapon_skill",
                "weapon_bal_modifier",
                "weapon_gdp_modifier",
                "weapon_weight",
                "weapon_price",
                "weapon_length",
                "weapon_range_hex",
                "weapon_min_strength",
                "weapon_damage_type"]
        ].sort_values('weapon_id')

        st.dataframe(compact_df, use_container_width=True)

    elif view == "Armas de Longa Distância":

        compact_df = df[[
            "weapon_id",
            "weapon_type",
            "weapon_name",
            "weapon_skill",
            "weapon_gdp_modifier",
            "weapon_weight",
            "weapon_price",
            "weapon_munition_price",
            "weapon_length",
            "weapon_min_strength",
            "weapon_damage_type",
            "weapon_tr",
            "weapon_prec",
            "weapon_half_distance",
            "weapon_max_distance",
            "weapon_reload_speed"]
        ].sort_values('weapon_id')

        st.dataframe(compact_df, use_container_width=True)

# ------------------------------------------------------------------------------------------------ #
#   FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT

def melee(df_dict: dict) -> None:
    """Armas Corpo-a-Corpo"""

    df = df_dict["melee"]
    df = df.fillna('')

    # Filtros
    skill_categories = df['weapon_type'].unique().tolist()

    selected_category = st.selectbox(
        "Selecione uma categoria de perícias:",
        skill_categories,
        index=0
    )

    df = df[df['weapon_type'] == selected_category]

    with st.expander(f"🎯 Filtros de Armas Corpo-a-Corpo"):

        df = search_box(
            df=df,
            label=f"🔍 Busca de Armas Corpo-a-Corpo",
            column=f"weapon_name"
        )

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
            render_weapons_full("Armas Corpo-a-Corpo", df)
        else:
            render_weapons_list("Armas Corpo-a-Corpo", df)

    except Exception as e:
        st.error(f"Falha ao renderizar Armas Corpo-a-Corpo.")
        return

def ranged(df_dict: dict) -> None:
    """Armas de Longa Distância"""

    df = df_dict["ranged"]
    df = df.fillna('')

    # Filtros
    skill_categories = df['weapon_type'].unique().tolist()

    selected_category = st.selectbox(
        "Selecione uma categoria de perícias:",
        skill_categories,
        index=0
    )

    df = df[df['weapon_type'] == selected_category]

    with st.expander(f"🎯 Filtros de Armas de Longa Distância"):

        df = search_box(
            df=df,
            label=f"🔍 Busca de Armas de Longa Distância",
            column=f"weapon_name"
        )

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
            render_weapons_full("Armas de Longa Distância", df)
        else:
            render_weapons_list("Armas de Longa Distância", df)

    except Exception as e:
        st.error(f"Falha ao renderizar Armas de Longa Distância.")
        return

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    df_dict = read_excel_data('weapons.xlsx')

    options = ["Armas Corpo-a-Corpo", "Armas de Longa Distância"]

    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["shield-slash-fill", "arrow-through-heart-fill"],
        default_index=0,
        orientation="horizontal"
    )

    # Roteamento das páginas
    if selection == options[0]:
        melee(df_dict)
    elif selection == options[1]:
        ranged(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()