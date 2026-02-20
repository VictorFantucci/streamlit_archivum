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
from app.components.filters import dynamic_filters, search_box, diff_text_granular

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES

TIER_ORDER = ["Comum", "Boa", "Superior", "Excelente", "Obra-Prima"]

TIER_COLORS = {
    "Comum": "#374151",       # cinza escuro
    "Boa": "#22C55E",         # verde
    "Superior": "#3B82F6",    # azul
    "Excelente": "#A855F7",   # roxo
    "Obra-Prima": "#F97316",  # laranja
}

def get_row_by_tier(df: pd.DataFrame, tier: str):
    filtered = df[df["consumable_tier"].astype(str) == str(tier)]
    if filtered.empty:
        return None
    return filtered.iloc[0]

def render_consumable_sub_page(df_consumables: pd.DataFrame, consumable_type: str):

    df = df_consumables.copy()
    df = df.fillna('')

    # normalização (boa prática)
    df["consumable_tier"] = df["consumable_tier"].astype(str).str.strip()

    df["consumable_tier"] = pd.Categorical(
        df["consumable_tier"],
        categories=TIER_ORDER,
        ordered=True
    )

    # ordenar por menor id da poção
    order = (
        df.groupby("consumable_name")["consumable_id"]
        .min()
        .sort_values()
        .index
    )

    for consumable_name in order:

        df_consumable = (
            df[df["consumable_name"] == consumable_name]
            .sort_values("consumable_tier")
            .reset_index(drop=True)
        )

        st.subheader(consumable_name)

        tiers_available = [
            t for t in TIER_ORDER
            if t in df_consumable["consumable_tier"].astype(str).values
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
                key=f"tier_segment_{consumable_name}"
            )
        except Exception:
            selected_tier = st.radio(
                "Tier",
                options=tiers_available,
                index=tiers_available.index(default_tier),
                horizontal=True,
                key=f"tier_radio_{consumable_name}"
            )

        row = get_row_by_tier(df_consumable, selected_tier)
        if row is None:
            continue

        prev_row = None
        idx = tiers_available.index(selected_tier)
        if idx > 0:
            prev_row = get_row_by_tier(df_consumable, tiers_available[idx - 1])

        tier_color = TIER_COLORS.get(str(row["consumable_tier"]), "#374151")

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
            st.write(f"**Nome:** {row['consumable_name']}")
        with col2:
            st.markdown(
                f"**Tier:** <span style='color:{tier_color}; font-weight:700'>{row['consumable_tier']}</span>",
                unsafe_allow_html=True
            )

        # ---------- CAMPOS ----------
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Categoria:** {h('consumable_category')}", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Duração:** {h('consumable_duration')}", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Efeito:** {h('consumable_effect')}", unsafe_allow_html=True)
        with col2:
            if consumable_type in ("Poções", "Elixires"):
                st.markdown(f"**Toxicidade:** {h('consumable_toxicity')}", unsafe_allow_html=True)
            elif consumable_type == "Venenos":
                st.markdown(f"**Métodos de Aplicação:** {h('consumable_method')}", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Preço:** {h('consumable_price')} moedas", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Peso:** {h('consumable_weight')} kg", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Descrição:**\n\n{h('consumable_description')}", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Observação:**\n\n{h('consumable_observation')}", unsafe_allow_html=True)

        st.markdown("---")

# ------------------------------------------------------------------------------------------------ #
#   FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT
def potions(df_dict: dict) -> None:
    """Poções"""

    df = df_dict["potions"]

    # Filtros
    with st.expander(f"🎯 Filtros de Poções"):


        df = search_box(
            df=df,
            label=f"🔍 Busca de Poções",
            column="consumable_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": "consumable_category",
                "type": "multiselect",
                "default": []
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning(f"Nenhuma poção encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # Função de visualização
    render_consumable_sub_page(df, "Poções")

def poisons(df_dict: dict) -> None:
    """Venenos"""

    df = df_dict["poisons"]

    # Filtros
    with st.expander(f"🎯 Filtros de Venenos"):


        df = search_box(
            df=df,
            label=f"🔍 Busca de Venenos",
            column="consumable_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": "consumable_category",
                "type": "multiselect",
                "default": []
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning(f"Nenhuma poção encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # Função de visualização
    render_consumable_sub_page(df, "Venenos")

def elixirs(df_dict: dict) -> None:
    """Elixires"""

    df = df_dict["elixirs"]

    # Filtros
    with st.expander(f"🎯 Filtros de Elixires"):


        df = search_box(
            df=df,
            label=f"🔍 Busca de Elixires",
            column="consumable_name"
        )

        filter_config = {
            "Filtrar por Tipo:": {
                "column": "consumable_category",
                "type": "multiselect",
                "default": []
            }
        }

        df, selected_filters = dynamic_filters(df, filter_config)

        if df.empty:
            st.warning(f"Nenhuma poção encontrado com os filtros aplicados.")
            return

    st.markdown("***")

    # Função de visualização
    render_consumable_sub_page(df, "Elixires")


# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():
    """
    Página principal que cria um menu lateral para seleção entre
    o grimório e a visão simples dos arquétipos.
    """

    df_dict = read_excel_data('alchemy.xlsx')

    options = ["Poções", "Venenos", "Elixires"]

    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["1-square-fill", "2-square-fill", "3-square-fill"],
        default_index=0,
        orientation="horizontal"
    )

    # Roteamento das páginas
    if selection == options[0]:
        potions(df_dict)
    elif selection == options[1]:
        poisons(df_dict)
    elif selection == options[2]:
        elixirs(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()