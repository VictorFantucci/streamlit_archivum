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
from app.utils import TIER_CONFIG, TIER_COLORS, TIER_ORDER
from app.src.data_loader import read_excel_data
from app.components.filters import search_box, diff_text_granular

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES

def get_row_by_tier(df: pd.DataFrame, tier: str):
    filtered = df[df["weapon_tier"].astype(str) == str(tier)]
    if filtered.empty:
        return None
    return filtered.iloc[0]

def calculate_hex(length):
    """ Função para converter comprimento em Hex """
    if length < 1:
        return 1
    return math.floor((length + 1) / 2) + 1

def render_melee_weapons(df_melee: pd.DataFrame):
    """
    Renderiza cada arma corpo-a-corpo em modo detalhado, com todos os campos e layout visual expandido.
    """

    df = df_melee.copy()
    df = df.fillna('')

    # Cria nova coluna de alcance em Hex
    df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)

    # normalização (boa prática)
    df["weapon_tier"] = df["weapon_tier"].astype(str).str.strip()

    df["weapon_tier"] = pd.Categorical(
        df["weapon_tier"],
        categories=TIER_ORDER,
        ordered=True
    )

    # ordenar por menor id da poção
    order = (
        df.groupby("weapon_name")["weapon_id"]
        .min()
        .sort_values()
        .index
    )

    for weapon_name in order:

        df_weapon = (
            df[df["weapon_name"] == weapon_name]
            .sort_values("weapon_tier")
            .reset_index(drop=True)
        )

        with st.expander(weapon_name):

            tiers_available = [
                t for t in TIER_ORDER
                if t in df_weapon["weapon_tier"].astype(str).values
            ]

            if not tiers_available:
                st.warning("Sem tiers disponíveis")
                continue

            default_tier = "Comum" if "Comum" in tiers_available else tiers_available[0]

            # botões
            try:
                selected_tier = st.segmented_control(
                    "Tier",
                    options=tiers_available,
                    default=default_tier,
                    key=f"tier_segment_{weapon_name}"
                )
            except Exception:
                selected_tier = st.radio(
                    "Tier",
                    options=tiers_available,
                    index=tiers_available.index(default_tier),
                    horizontal=True,
                    key=f"tier_radio_{weapon_name}"
                )

            row = get_row_by_tier(df_weapon, selected_tier)
            if row is None:
                continue

            prev_row = None
            idx = tiers_available.index(selected_tier)
            if idx > 0:
                prev_row = get_row_by_tier(df_weapon, tiers_available[idx - 1])

            tier_color = TIER_COLORS.get(str(row["weapon_tier"]), "#374151")

            def h(field):
                if prev_row is None:
                    return str(row[field])

                value = row[field]
                prev = prev_row[field]

                # textos longos → diff granular
                if isinstance(value, str):
                    return diff_text_granular(value, prev, tier_color)

                # valores simples → highlight normal
                if value != prev:
                    return f"<span style='color:{tier_color}; font-weight:600'>{value}</span>"

                return str(value)

            # ---------- HEADER ----------
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{row['weapon_tier']}</span>",
                    unsafe_allow_html=True
                )
            with col1:
                st.markdown(f"**Perícia:** {h('weapon_skill')}", unsafe_allow_html=True)


            # ---------- CAMPOS ----------
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Modificador BAL:** {h('weapon_bal_modifier')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Modificador GDP:** {h('weapon_gdp_modifier')}", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Peso:** {h('weapon_weight')} kg", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Comprimento:** {h('weapon_length')} m", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Preço:** {h('weapon_price')} moedas", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Alcance:** {h('weapon_range_hex')} Hex", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**ST Mínima:** {h('weapon_min_strength')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Tipos de Dano:** {h('weapon_damage_type')}", unsafe_allow_html=True)

            st.markdown(f"**Descrição:**\n\n{h('weapon_description')}", unsafe_allow_html=True)

def render_ranged_weapons(df_ranged: pd.DataFrame):
    """
    Renderiza cada arma de longa distância em modo detalhado, com todos os campos e layout visual expandido.
    """

    df = df_ranged.copy()
    df = df.fillna('')

    # Cria nova coluna de alcance em Hex
    df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)

    # normalização (boa prática)
    df["weapon_tier"] = df["weapon_tier"].astype(str).str.strip()

    df["weapon_tier"] = pd.Categorical(
        df["weapon_tier"],
        categories=TIER_ORDER,
        ordered=True
    )

    # ordenar por menor id da poção
    order = (
        df.groupby("weapon_name")["weapon_id"]
        .min()
        .sort_values()
        .index
    )

    for weapon_name in order:

        df_weapon = (
            df[df["weapon_name"] == weapon_name]
            .sort_values("weapon_tier")
            .reset_index(drop=True)
        )

        with st.expander(weapon_name):

            tiers_available = [
                t for t in TIER_ORDER
                if t in df_weapon["weapon_tier"].astype(str).values
            ]

            if not tiers_available:
                st.warning("Sem tiers disponíveis")
                continue

            default_tier = "Comum" if "Comum" in tiers_available else tiers_available[0]

            # botões
            try:
                selected_tier = st.segmented_control(
                    "Tier",
                    options=tiers_available,
                    default=default_tier,
                    key=f"tier_segment_{weapon_name}"
                )
            except Exception:
                selected_tier = st.radio(
                    "Tier",
                    options=tiers_available,
                    index=tiers_available.index(default_tier),
                    horizontal=True,
                    key=f"tier_radio_{weapon_name}"
                )

            row = get_row_by_tier(df_weapon, selected_tier)
            if row is None:
                continue

            prev_row = None
            idx = tiers_available.index(selected_tier)
            if idx > 0:
                prev_row = get_row_by_tier(df_weapon, tiers_available[idx - 1])

            tier_color = TIER_COLORS.get(str(row["weapon_tier"]), "#374151")

            def h(field):
                if prev_row is None:
                    return str(row[field])

                value = row[field]
                prev = prev_row[field]

                # textos longos → diff granular
                if isinstance(value, str):
                    return diff_text_granular(value, prev, tier_color)

                # valores simples → highlight normal
                if value != prev:
                    return f"<span style='color:{tier_color}; font-weight:600'>{value}</span>"

                return str(value)

            # ---------- HEADER ----------
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{row['weapon_tier']}</span>",
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(f"**Perícia:** {h('weapon_skill')}", unsafe_allow_html=True)


            # ---------- CAMPOS ----------
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Modificador GDP:** {h('weapon_gdp_modifier')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Tempo de Recarga:** {h('weapon_reload_speed')}", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**TR:** {h('weapon_tr')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Prec:** {h('weapon_prec')}", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Peso:** {h('weapon_weight')} kg", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Comprimento:** {h('weapon_length')} m", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Preço:** {h('weapon_price')} moedas", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Preço da Munição:** {h('weapon_ammo_price')} moedas", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**ST Mínima:** {h('weapon_min_strength')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Tipos de Dano:** {h('weapon_damage_type')}", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Distância ½:** {h('weapon_half_distance')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Distância Max:** {h('weapon_max_distance')}", unsafe_allow_html=True)

            st.markdown(f"**Descrição:**\n\n{h('weapon_description')}", unsafe_allow_html=True)

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

    st.subheader(selected_category, divider="grey")

    render_melee_weapons(df)

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

    st.subheader(selected_category, divider="grey")

    render_ranged_weapons(df)

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    df_dict = read_excel_data('weapons_with_tiers.xlsx')

    options = ["Armas Corpo-a-Corpo", "Armas de Longa Distância"]

    with st.sidebar:
        selection = option_menu(
            menu_title=None,
            options=options,
            icons=["shield-slash-fill", "arrow-through-heart-fill"],
            default_index=0,
        )

    # Roteamento das páginas
    if selection == options[0]:
        melee(df_dict)
    elif selection == options[1]:
        ranged(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()