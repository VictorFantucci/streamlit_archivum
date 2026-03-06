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
# FUNÇÕES AUXILIARES DAS REGRAS

# Helpers
def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))

def tier_limit_for_nh(nh: int, tier: str) -> int:
    cfg = TIER_CONFIG[tier]

    if nh < cfg["min_nh"]:
        return 0

    return round_half_up(nh / cfg["divisor"])

def limits_for_nh(nh: int) -> dict:
    return {t: tier_limit_for_nh(nh, t) for t in TIER_ORDER}

# Tabela
def tb_tier_limits(nh_min=None, nh_max=30):

    if nh_min is None:
        nh_min = min(cfg["min_nh"] for cfg in TIER_CONFIG.values())

    rows = []

    for nh in range(nh_min, nh_max + 1):

        row = {"NH": nh}
        row.update(limits_for_nh(nh))

        rows.append(row)

    return pd.DataFrame(rows)

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES DE VISUALIZAÇÃO DAS REGRAS

def render_tier_limits_panel():

    st.subheader("Fabricação por NH do Alquimista", divider="grey")

    # -------------------------------------------------
    # tabela completa

    df = tb_tier_limits()

    # -------------------------------------------------
    # NH selecionado

    nh_min = min(cfg["min_nh"] for cfg in TIER_CONFIG.values())

    nh = st.number_input(
        "NH do alquimista",
        min_value=nh_min,
        max_value=30,
        value=12,
        step=1
    )

    # limites calculados
    limits = limits_for_nh(nh)

    # ⭐ somente tiers permitidos
    allowed_tiers = [
        t for t in TIER_ORDER
        if nh >= TIER_CONFIG[t]["min_nh"]
    ]

    st.markdown("### **Limite para este NH**")

    st.dataframe(
        pd.DataFrame([{t: limits[t] for t in allowed_tiers}]),
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Tabela completa", expanded=False):
        st.dataframe(df, use_container_width=True, hide_index=True)

def render_fabrication_rules() -> None:
    """
    Renderiza as regras de fabricação de poções.
    """

    st.subheader("Resultados na Fabricação de Consumíveis Alquímicos", divider="grey")

    # ✅ SUCESSO
    with st.expander("✅ Sucesso", expanded=False):
        st.markdown("""
- O consumível é produzido exatamente na qualidade escolhida, conforme a **NH** do alquimista.
        """)

    # ✨ ACERTO CRÍTICO
    with st.expander("✨ Acerto Crítico", expanded=False):
        st.markdown("""

A produção é realizada com precisão excepcional, superando as capacidades normais do alquimista.

- **50% de chance** (3 números à escolha do Mestre e/ou jogador):
  ➝ O consumível é criado com qualidade **1 tier acima** da NH.

- **50% de chance** (3 números):
  ➝ São produzidas **maiores quantidades** do consumível (dobro, triplo etc.), conforme decisão do Mestre.

📌 **Caso o alquimista possua NH para qualidade Obra-Prima**

- Mestre e jogador podem decidir o resultado automaticamente, sem necessidade de rolagem.

- Se houver subida de tier a partir de **Obra-Prima**, o consumível se torna de qualidade **Única**, recebendo:
  - Seu efeito normal de Obra-Prima;
  - +1 efeito benéfico adicional coerente com sua categoria.

**Exemplo:**
Uma poção de vida não pode conceder invisibilidade, mas pode fornecer resistência a dano ou venenos.
A decisão final sobre o efeito bônus cabe ao Mestre.

        """)

    # ❌ FALHA
    with st.expander("❌ Falha", expanded=False):
        st.markdown("""

Caso o alquimista falhe no teste de criação do consumível, role **1d6** para determinar o resultado:

📌 **Resultado Padrão**

- **50% de chance** (3 números à escolha do Mestre e/ou jogador):
  ➝ O consumível falha e os ingredientes são perdidos.

- **50% de chance** (3 números):
  ➝ O consumível decai **1 tier** em qualidade.

📌 **Caso o alquimista só possa produzir qualidade **Comum****

A redução de tier **não se aplica**.

- **70% de chance** (4 números):
  ➝ O consumível falha e os ingredientes são perdidos.

- **30% de chance** (2 números):
  ➝ Ocorre uma consequência desastrosa (ver *Erro Crítico*).

        """)

    # 💥 ERRO CRÍTICO
    with st.expander("💥 Erro Crítico", expanded=False):
        st.markdown("""

O consumível se torna instável durante a fabricação, gerando um resultado geralmente desastroso.

- **70% de chance** (4 números à escolha do Mestre e/ou jogador):
  ➝ Consequência catastrófica (explosão, nuvem nociva com efeito negativo do consumível ou outro efeito decidido pelo Mestre).

- **30% de chance** (2 números):
  ➝ O consumível falha e os ingredientes são perdidos.

        """)

def alchemy_rules() -> None:

    render_tier_limits_panel()

    st.markdown("***")

    render_fabrication_rules()

def toxicity_rules() -> None:
    """
    Renderiza as regras de Toxicidade.
    """

    st.subheader("Regras de Toxicidade", divider="grey")

    # 📊 CONCEITO E CÁLCULO
    st.markdown(r"""

        A **Toxicidade** representa o limite fisiológico do personagem para consumir substâncias alquímicas sem sofrer efeitos adversos.

        Ela é calculada pela fórmula:

        $$
        \text{Toxicidade} = \frac{HT \times 4 + IQ \times 3 + ST \times 3}{3}
        $$

        Sendo:

        - $HT$ = Vitalidade
        - $IQ$ = Inteligência
        - $ST$ = Força

    """)

    with st.expander("Exemplo"):
        st.markdown(r"""
            Se um personagem possui:

            $$
            HT = 12
            $$

            $$
            IQ = 11
            $$

            $$
            ST = 10
            $$

            Então:

            $$
            \text{Toxicidade} = \frac{(12 \times 4) + (11 \times 3) + (10 \times 3)}{3}
            $$

            $$
            \text{Toxicidade} = \frac{48 + 33 + 30}{3}
            $$

            $$
            \text{Toxicidade} = \frac{90}{3} = 37
            $$
        """)

    # ♻️ RECUPERAÇÃO
    with st.expander("♻️ Recuperação de Toxicidade", expanded=False):
        st.markdown("""
- A recuperação natural é de **1 ponto a cada 30 minutos**.
- A toxicidade **só começa a decair após todos os efeitos de poções e elixires terminarem**.
- Existem consumíveis específicos capazes de **eliminar toxicidade** diretamente.
        """)

    # ⚠️ EFEITOS POR PERCENTUAL
    with st.expander("⚠️ Efeitos por Percentual de Toxicidade", expanded=False):
        st.markdown("""
Os efeitos negativos variam conforme o percentual atual de toxicidade em relação ao limite máximo do personagem:

- **0% a 50%**
  ➝ Nenhuma consequência.

- **51% a 75%**
  ➝ Perda de **1 ponto de vida por hora**, até que a toxicidade seja eliminada.

- **76% a 99%**
  ➝ Perda de **2 pontos de vida por hora**, até que a toxicidade seja eliminada.

- **100%**
  ➝ Quando todos os efeitos que causam toxicidade cessarem:
    - O personagem fica **inconsciente**;
    - Perde **4 pontos de vida a cada 2 horas**, até que a toxicidade seja eliminada.
        """)

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES AUXILIARES DOS CONSUMÍVEIS

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
            elif consumable_type in ("Venenos"):
                st.markdown(f"**Métodos de Aplicação:** {h('consumable_method')}", unsafe_allow_html=True)
            elif consumable_type in ("Bombas"):
                st.markdown(f"**Área de Efeito:** {h('consumable_effect_area')}", unsafe_allow_html=True)

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
# FUNÇÕES DE VISUALIZAÇÃO DOS CONSUMÍVEIS

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

def bombs(df_dict: dict) -> None:
    """Bombas"""

    df = df_dict["bombs"]

    # Filtros
    with st.expander(f"🎯 Filtros de Bombas"):


        df = search_box(
            df=df,
            label=f"🔍 Busca de Bombas",
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
    render_consumable_sub_page(df, "Bombas")

def alchemy_itens() -> None:
    """Itens de alquimia"""

    df_dict = read_excel_data('alchemy.xlsx')

    options = ["Poções", "Venenos", "Elixires", "Bombas"]

    selection = option_menu(
        menu_title=None,
        options=options,
        icons=["1-square-fill", "2-square-fill", "3-square-fill", "4-square-fill"],
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
    elif selection == options[3]:
        bombs(df_dict)

# ------------------------------------------------------------------------------------------------ #
#FUNÇÃO MAIN

def main():

    options = ["Regras", "Toxicidade", "Consumíveis"]

    with st.sidebar:
        st.markdown("### Navegação")
        selection = option_menu(
            menu_title=None,
            options=options,
            default_index=0,
        )

    # Roteamento das páginas
    if selection == options[0]:
        alchemy_rules()
    elif selection == options[1]:
        toxicity_rules()
    elif selection == options[2]:
        alchemy_itens()


# ------------------------------------------------------------------------------------------------ #
main()