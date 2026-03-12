# ------------------------------------------------------------------------------------------------ #
# IMPORTS

import os
import streamlit as st
from itertools import product
import math
import pandas as pd

import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from app.utils import TIER_CONFIG, TIER_COLORS, TIER_ORDER
from app.src.data_loader import read_excel_data
from app.components.filters import dynamic_filters, search_box, diff_text_granular

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES DAS ARMADURAS

def get_row_by_tier(df: pd.DataFrame, tier: str):
    filtered = df[df["armor_tier"].astype(str) == str(tier)]
    if filtered.empty:
        return None
    return filtered.iloc[0]

def render_armor_page(df_armors: pd.DataFrame, armor_type: str):

    df = df_armors.copy()
    df = df.fillna('')

    # normalização (boa prática)
    df["armor_tier"] = df["armor_tier"].astype(str).str.strip()

    df["armor_tier"] = pd.Categorical(
        df["armor_tier"],
        categories=TIER_ORDER,
        ordered=True
    )

    # ordenar por menor id da poção
    order = (
        df.groupby("armor_name")["armor_id"]
        .min()
        .sort_values()
        .index
    )

    for armor_name in order:

        df_armor = (
            df[df["armor_name"] == armor_name]
            .sort_values("armor_tier")
            .reset_index(drop=True)
        )

        with st.expander(armor_name):

            tiers_available = [
                t for t in TIER_ORDER
                if t in df_armor["armor_tier"].astype(str).values
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
                    key=f"tier_segment_{armor_name}"
                )
            except Exception:
                selected_tier = st.radio(
                    "Tier",
                    options=tiers_available,
                    index=tiers_available.index(default_tier),
                    horizontal=True,
                    key=f"tier_radio_{armor_name}"
                )

            row = get_row_by_tier(df_armor, selected_tier)
            if row is None:
                continue

            prev_row = None
            idx = tiers_available.index(selected_tier)
            if idx > 0:
                prev_row = get_row_by_tier(df_armor, tiers_available[idx - 1])

            tier_color = TIER_COLORS.get(str(row["armor_tier"]), "#374151")

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
                    f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{row['armor_tier']}</span>",
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(f"**Tipo:** {h('armor_type')}", unsafe_allow_html=True)


            # ---------- CAMPOS ----------
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Slot:** {h('armor_piece_location')}", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Resistência (DR):** {h('armor_damage_resistence')}", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Preço:** {h('armor_price')} moedas", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Peso:** {h('armor_weight')} kg", unsafe_allow_html=True)

            st.markdown(f"**Descrição:**\n\n{h('armor_description')}", unsafe_allow_html=True)

def render_armor_selection(df_armors: pd.DataFrame):

    st.subheader("Seleção de Armaduras", divider="grey")

    slots = ["Cabeça", "Tronco", "Braços", "Mãos", "Pernas", "Pés"]
    type_order = ["Leve", "Média", "Pesada"]

    # -----------------------------
    # PRESETS
    # -----------------------------

    col1, col2, col3, col4 = st.columns([1,1,1,3])

    if col1.button("Leve"):
        st.session_state["preset_type"] = "Leve"

    if col2.button("Média"):
        st.session_state["preset_type"] = "Média"

    if col3.button("Pesada"):
        st.session_state["preset_type"] = "Pesada"

    preset = st.session_state.get("preset_type", None)

    selected_rows = []

    # -----------------------------
    # SLOTS
    # -----------------------------

    for i in range(0, len(slots), 2):

        col_left, col_right = st.columns(2)

        for col, slot in zip([col_left, col_right], slots[i:i+2]):

            with col:

                st.markdown(f"**{slot}**")

                df_slot = df_armors[df_armors["armor_piece_location"] == slot].copy()

                # ordenar tipos
                df_slot["armor_type"] = pd.Categorical(
                    df_slot["armor_type"],
                    categories=type_order,
                    ordered=True
                )

                df_slot = df_slot.sort_values(["armor_type", "armor_name"])

                armor_names = df_slot["armor_name"].unique().tolist()

                # -----------------------------
                # PRESET DEFAULT
                # -----------------------------

                default_armor = armor_names[0]

                if preset:
                    df_preset = df_slot[df_slot["armor_type"] == preset]
                    if not df_preset.empty:
                        default_armor = df_preset.iloc[0]["armor_name"]

                sub1, sub2 = st.columns(2)

                with sub1:
                    armor_choice = st.selectbox(
                        "Armadura",
                        armor_names,
                        index=armor_names.index(default_armor),
                        key=f"armor_select_{slot}"
                    )

                df_armor = df_slot[df_slot["armor_name"] == armor_choice]

                tiers = df_armor["armor_tier"].tolist()

                with sub2:
                    tier_choice = st.selectbox(
                        "Tier",
                        tiers,
                        index=tiers.index("Comum") if "Comum" in tiers else 0,
                        key=f"tier_select_{slot}"
                    )

                row = df_armor[df_armor["armor_tier"] == tier_choice].iloc[0]

                selected_rows.append(row)

                stat1, stat2 = st.columns(2)

                with stat1:
                    st.write(f"DR: **{row['armor_damage_resistence']}**")
                    st.write(f"Peso: **{row['armor_weight']} kg**")

                with stat2:
                    st.write(f"Preço: **{row['armor_price']}**")

        st.markdown("---")

    return pd.DataFrame(selected_rows)

def render_build_summary(df_build: pd.DataFrame):

    if df_build.empty:
        return

    st.subheader("Resumo do Conjunto", divider="grey")

    total_weight = df_build["armor_weight"].sum()
    total_price = df_build["armor_price"].sum()
    total_dr = df_build["armor_damage_resistence"].sum()

    col1, col2, col3 = st.columns(3)

    col1.write(f"**DR Total:** {total_dr}")
    col2.write(f"**Peso Total:** {round(total_weight,2)} kg")
    col3.write(f"**Preço Total:** {total_price} moedas")

    df_view = (
        df_build[
            [
                "armor_piece_location",
                "armor_name",
                "armor_tier",
                "armor_damage_resistence",
                "armor_weight",
                "armor_price"
            ]
        ]
        .rename(columns={
            "armor_piece_location": "Slot",
            "armor_name": "Armadura",
            "armor_tier": "Tier",
            "armor_damage_resistence": "DR",
            "armor_weight": "Peso (kg)",
            "armor_price": "Preço"
        })
    )

    st.dataframe(
        df_view,
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES DE VISUALIZAÇÃO DAS ARMADURAS

def armors(df_dict: dict) -> None:
    """Armaduras"""

    df_armors = df_dict["armors"]

    options = ["Cabeça", "Tronco", "Braços", "Mãos", "Pernas", "Pés"]

    st.header("Armaduras", divider="grey")

    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["1-square-fill", "2-square-fill", "3-square-fill",
               "4-square-fill", "5-square-fill", "6-square-fill"],
        default_index=0,
        orientation="horizontal"
    )

    df = df_armors[df_armors["armor_piece_location"] == selection]

    st.markdown("***")

    # Função de visualização
    render_armor_page(df, "Armaduras")

def armor_build(df_dict):

    st.header("Montar Conjunto de Armadura", divider="grey")

    df_armors = df_dict["armors"].copy()

    with st.expander("Seleção de armadura por slot e tier"):
        df_build = render_armor_selection(df_armors)

    render_build_summary(df_build)

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():

    df_dict = read_excel_data('armors.xlsx')

    options = ["Armaduras", "Montar Build"]

    with st.sidebar:
        st.markdown("### Navegação")
        selection = option_menu(
            menu_title=None,
            options=options,
            default_index=0,
        )

    if selection == options[0]:
        armors(df_dict)

    if selection == options[1]:
        armor_build(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()