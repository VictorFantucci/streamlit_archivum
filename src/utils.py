"""
Script que contém as utilidades do projeto.
"""

# ------------------------------------------------------------------------------------------------ #
# IMPORT

import os
import unicodedata
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES

utils_directory = os.path.dirname(os.path.dirname(__file__)).rstrip('.')

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES

def get_project_folder(folder_name: str = None) -> str:
    """
    Retorna o caminho absoluto de uma pasta específica do projeto.

    Args:
        folder_name (str, opcional): Nome da pasta cuja rota deve ser retornada.
                                     Se None, retorna o diretório base do projeto.

    Returns:
        str: Caminho absoluto para a pasta solicitada.

    Raises:
        Exception: Caso ocorra erro ao montar o caminho.
    """

    # Mapeamento simples de nomes para caminhos relativos
    folders = {
        None: "",
        "tests": "tests",
        "logs": "logs",
        "data": "data",
        "src": "src",
        "img": os.path.join("src", "img"),
        "pages": os.path.join("src", "pages"),
        "components": os.path.join("src", "components"),
        "calculations": os.path.join("src", "calculations"),
        "src_date": os.path.join("src", "data"),
    }

    try:
        if folder_name not in folders:
            raise ValueError(f"Pasta desconhecida: {folder_name}")

        return os.path.join(utils_directory, folders[folder_name])

    except Exception as e:
        print(f"Erro ao obter pasta: {e}")
        raise

# ------------------------------------------------------------------------------------------------ #
#FUNÇÕES UTILITÁRIAS PARA O STREAMLIT

def dynamic_filters(df: pd.DataFrame, filter_config: dict):
    """
    Aplica filtros dinâmicos em um DataFrame usando componentes do Streamlit.
    Toda vez que um filtro é aplicado, os demais se ajustam de acordo com os
    valores restantes no subconjunto filtrado.

    Args:
        df : pd.DataFrame
            DataFrame original contendo os dados a serem filtrados.

        filter_config : dict
            Dicionário no formato:
            {
                "label_para_ui": {
                    "column": "nome_da_coluna",
                    "type": "multiselect" | "selectbox",
                    "default": []
                    "sort_order": []
                },
                ...
            }

    Return:
        filtered_df : pd.DataFrame
            DataFrame após aplicação de todos os filtros.

        filter_state : dict
            Dicionário contendo os valores selecionados para cada filtro.
    """

    filtered_df = df.copy()
    filter_state = {}

    # Itera sobre filtros na ordem definida
    for filter_label, cfg in filter_config.items():
        col_name = cfg["column"]
        filter_type = cfg.get("type", "multiselect")
        default = cfg.get("default", [])

        raw_values = list(filtered_df[col_name].dropna().unique())

        # Caso haja sort customizado
        custom_sort = cfg.get("sort_order")

        if custom_sort:
            # mantém apenas valores presentes — evita erro se algo não existir no DF
            valid_values = [v for v in custom_sort if v in raw_values]
        else:
            valid_values = sorted(raw_values)

        # Streamlit UI para o filtro
        if filter_type == "multiselect":
            selection = st.multiselect(
                filter_label,
                options=valid_values,
                default=[v for v in default if v in valid_values],
            )

            # aplica o filtro se tiver seleção
            if selection:
                filtered_df = filtered_df[filtered_df[col_name].isin(selection)]

        elif filter_type == "selectbox":
            selection = st.selectbox(
                filter_label,
                options=["(Todos)"] + valid_values,
                index=0
            )

            if selection != "(Todos)":
                filtered_df = filtered_df[filtered_df[col_name] == selection]

        else:
            raise ValueError(f"Unsupported filter type: {filter_type}")

        # Salva o estado do filtro
        filter_state[col_name] = selection

    return filtered_df, filter_state

def search_box(df, label="🔍 Buscar", column="nome"):
    """
    Search box com autocomplete estilo 'busca dinâmica'.
    Quando o usuário digita, as sugestões são filtradas dinamicamente.
    """

    # Entrada de texto
    termo = st.text_input(label)

    # Gerar sugestões com base no que foi digitado
    if termo:
        suggestions = (
            df[column]
            .dropna()
            .unique()
            .tolist()
        )

        suggestions = [
            s for s in suggestions if termo.lower() in s.lower()
        ]

        suggestions = sorted(suggestions, key=str.lower)

        if suggestions:
            st.caption("Sugestões:")
            st.write(", ".join(suggestions[:20]))  # limita a 20 sugestões
        else:
            st.caption("Nenhuma sugestão encontrada.")

        # Aplicar o filtro ao dataframe
        df = df[df[column].str.contains(termo, case=False, na=False)]

    return df

def sort_ui(df, default_col=None):
    """
    UI para ordenação dinâmica de um DataFrame.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame base a ser ordenado.
    default_col : str
        Coluna padrão para ordenação caso o usuário não selecione outra.

    Retorno
    -------
    pd.DataFrame
        DataFrame ordenado conforme seleção do usuário.
    """

    st.subheader("Ordenação")

    # Seleciona coluna
    sort_col = st.selectbox("Escolha a coluna para ordenar:", df.columns, index=df.columns.get_loc(default_col) if default_col else 0)

    # Crescente ou decrescente
    ascending = st.radio("Ordem:", ["Crescente", "Decrescente"]) == "Crescente"

    return df.sort_values(by=sort_col, ascending=ascending)

def tag_filter(df, filter_columns):
    """
    Filtro dinâmico baseado em múltiplas colunas do DataFrame.
    Conforme o usuário faz seleções, as demais opções são atualizadas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame base a ser filtrado.
    filter_columns : list
        Lista de colunas que serão usadas como filtros.

    Retorno
    -------
    pd.DataFrame
        DataFrame filtrado conforme as escolhas do usuário.
    dict
        Dicionário contendo os valores selecionados para cada filtro.
    """

    st.subheader("Filtros")

    # Armazena seleções do usuário
    selections = {}

    # DataFrame auxiliar que será filtrado a cada passo
    filtered_df = df.copy()

    for col in filter_columns:

        # Ajusta dinamicamente as opções disponíveis
        available_options = sorted(filtered_df[col].dropna().unique())

        # Caixa de seleção dinâmica
        selection = st.multiselect(
            f"Filtrar por {col}:",
            available_options,
            default=None
        )

        selections[col] = selection

        # Aplica filtragem parcial para atualizar opções das próximas colunas
        if selection:
            filtered_df = filtered_df[filtered_df[col].isin(selection)]

    return filtered_df, selections
