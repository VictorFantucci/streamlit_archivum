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
from app.utils import TIER_CONFIG, TIER_COLORS, TIER_ORDER, TIER_NAME_SETS
DEFAULT_TIER_SET = "qualidade"

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

def render_melee_weapons(
    df_melee: pd.DataFrame,
    tier_set: str = DEFAULT_TIER_SET
):
    """
    Renderiza cada arma corpo-a-corpo em modo detalhado,
    com todos os campos e layout visual expandido.
    """

    df = df_melee.copy()
    df = df.fillna('')

    tier_map = TIER_NAME_SETS[tier_set]

    # -----------------------------
    # calcular alcance
    # -----------------------------
    df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)

    # -----------------------------
    # converter nome -> nível
    # -----------------------------
    name_to_level = {v: k for k, v in tier_map.items()}

    df["tier_level"] = (
        df["weapon_tier"]
        .astype(str)
        .str.strip()
        .map(name_to_level)
    )

    df["tier_level"] = pd.Categorical(
        df["tier_level"],
        categories=TIER_ORDER,
        ordered=True
    )

    # -----------------------------
    # ordenar armas
    # -----------------------------
    order = (
        df.groupby("weapon_name")["weapon_id"]
        .min()
        .sort_values()
        .index
    )

    for weapon_name in order:

        df_weapon = (
            df[df["weapon_name"] == weapon_name]
            .sort_values("tier_level")
            .reset_index(drop=True)
        )

        with st.expander(weapon_name):

            tiers_available = [
                int(t)
                for t in df_weapon["tier_level"]
                .dropna()
                .unique()
            ]

            tiers_available = sorted(tiers_available)

            if not tiers_available:
                st.warning("Sem tiers disponíveis")
                continue

            tier_labels = [tier_map[t] for t in tiers_available]

            default_level = 1 if 1 in tiers_available else tiers_available[0]
            default_label = tier_map[default_level]

            # -----------------------------
            # seleção de tier
            # -----------------------------
            try:
                selected_label = st.segmented_control(
                    "Tier",
                    options=tier_labels,
                    default=default_label,
                    key=f"tier_segment_{weapon_name}"
                )
            except Exception:
                selected_label = st.radio(
                    "Tier",
                    options=tier_labels,
                    index=tier_labels.index(default_label),
                    horizontal=True,
                    key=f"tier_radio_{weapon_name}"
                )

            selected_level = name_to_level[selected_label]

            # -----------------------------
            # linha atual
            # -----------------------------
            row = df_weapon[df_weapon["tier_level"] == selected_level]

            if row.empty:
                continue

            row = row.iloc[0]

            # -----------------------------
            # tier anterior
            # -----------------------------
            prev_row = None
            idx = tiers_available.index(selected_level)

            if idx > 0:
                prev_level = tiers_available[idx - 1]
                prev = df_weapon[df_weapon["tier_level"] == prev_level]

                if not prev.empty:
                    prev_row = prev.iloc[0]

            tier_color = TIER_COLORS.get(selected_level, "#374151")

            # -----------------------------
            # highlight helper
            # -----------------------------
            def h(field):

                if prev_row is None:
                    value = row[field]

                    if isinstance(value, (int, float)):
                        return f"{float(value):.1f}"

                    return str(value)

                value = row[field]
                prev = prev_row[field]

                # textos longos → diff granular
                if isinstance(value, str):
                    return diff_text_granular(value, prev, tier_color)

                # números → round + highlight
                if isinstance(value, (int, float)):
                    value_fmt = f"{float(value):.1f}"
                    prev_fmt = f"{float(prev):.1f}" if isinstance(prev, (int, float)) else prev

                    if value_fmt != prev_fmt:
                        return f"<span style='color:{tier_color}; font-weight:600'>{value_fmt}</span>"

                    return value_fmt

                # fallback
                if value != prev:
                    return f"<span style='color:{tier_color}; font-weight:600'>{value}</span>"

                return str(value)

            # -----------------------------
            # HEADER
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{tier_map[selected_level]}</span>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(f"**Perícia:** {h('weapon_skill')}", unsafe_allow_html=True)

            # -----------------------------
            # CAMPOS
            # -----------------------------
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

def render_ranged_weapons(
    df_ranged: pd.DataFrame,
    tier_set: str = DEFAULT_TIER_SET
):
    """
    Renderiza cada arma de longa distância em modo detalhado,
    com todos os campos e layout visual expandido.
    """

    df = df_ranged.copy()
    df = df.fillna('')

    tier_map = TIER_NAME_SETS[tier_set]

    # -----------------------------
    # calcular alcance em hex
    # -----------------------------
    df["weapon_range_hex"] = df["weapon_length"].apply(calculate_hex)

    # -----------------------------
    # converter nome -> nível
    # -----------------------------
    name_to_level = {v: k for k, v in tier_map.items()}

    df["tier_level"] = (
        df["weapon_tier"]
        .astype(str)
        .str.strip()
        .map(name_to_level)
    )

    df["tier_level"] = pd.Categorical(
        df["tier_level"],
        categories=TIER_ORDER,
        ordered=True
    )

    # -----------------------------
    # ordenar armas
    # -----------------------------
    order = (
        df.groupby("weapon_name")["weapon_id"]
        .min()
        .sort_values()
        .index
    )

    for weapon_name in order:

        df_weapon = (
            df[df["weapon_name"] == weapon_name]
            .sort_values("tier_level")
            .reset_index(drop=True)
        )

        with st.expander(weapon_name):

            tiers_available = [
                int(t)
                for t in df_weapon["tier_level"]
                .dropna()
                .unique()
            ]

            tiers_available = sorted(tiers_available)

            if not tiers_available:
                st.warning("Sem tiers disponíveis")
                continue

            tier_labels = [tier_map[t] for t in tiers_available]

            default_level = 1 if 1 in tiers_available else tiers_available[0]
            default_label = tier_map[default_level]

            # -----------------------------
            # seleção de tier
            # -----------------------------
            try:
                selected_label = st.segmented_control(
                    "Tier",
                    options=tier_labels,
                    default=default_label,
                    key=f"tier_segment_{weapon_name}"
                )
            except Exception:
                selected_label = st.radio(
                    "Tier",
                    options=tier_labels,
                    index=tier_labels.index(default_label),
                    horizontal=True,
                    key=f"tier_radio_{weapon_name}"
                )

            selected_level = name_to_level[selected_label]

            # -----------------------------
            # linha atual
            # -----------------------------
            row = df_weapon[df_weapon["tier_level"] == selected_level]

            if row.empty:
                continue

            row = row.iloc[0]

            # -----------------------------
            # tier anterior
            # -----------------------------
            prev_row = None
            idx = tiers_available.index(selected_level)

            if idx > 0:
                prev_level = tiers_available[idx - 1]
                prev = df_weapon[df_weapon["tier_level"] == prev_level]

                if not prev.empty:
                    prev_row = prev.iloc[0]

            tier_color = TIER_COLORS.get(selected_level, "#374151")

            # -----------------------------
            # highlight helper
            # -----------------------------
            def h(field):

                if prev_row is None:
                    value = row[field]

                    if isinstance(value, (int, float)):
                        return f"{float(value):.1f}"

                    return str(value)

                value = row[field]
                prev = prev_row[field]

                # textos longos → diff granular
                if isinstance(value, str):
                    return diff_text_granular(value, prev, tier_color)

                # números → round + highlight
                if isinstance(value, (int, float)):
                    value_fmt = f"{float(value):.1f}"
                    prev_fmt = f"{float(prev):.1f}" if isinstance(prev, (int, float)) else prev

                    if value_fmt != prev_fmt:
                        return f"<span style='color:{tier_color}; font-weight:600'>{value_fmt}</span>"

                    return value_fmt

                # fallback
                if value != prev:
                    return f"<span style='color:{tier_color}; font-weight:600'>{value}</span>"

                return str(value)

            # -----------------------------
            # HEADER
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{tier_map[selected_level]}</span>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(f"**Perícia:** {h('weapon_skill')}", unsafe_allow_html=True)

            # -----------------------------
            # CAMPOS
            # -----------------------------
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