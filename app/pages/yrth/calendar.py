# ------------------------------------------------------------------------------------------------ #
# IMPORTS

import os
import streamlit as st
import pandas as pd
import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from app.src.data_loader import ExcelReader
from utils import get_project_folder

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES

logs_folder = get_project_folder('app')
data_folder = get_project_folder('data')

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES DE LEITURA DE DADOS

def read_ytarria_calendar() -> tuple[pd.DataFrame, pd.DataFrame]:

    # Caminho fixo dos arquivos
    file_path = os.path.join(data_folder, "calendar.xlsx")

    # Inicializa o leitor
    excel_reader = ExcelReader(log_dir=logs_folder, file_path=file_path)

    try:
        df_dict = excel_reader.load_sheets()
    except Exception as e:
        st.error("Falha ao carregar a aba selecionada.")
        return None, None

    # --- Meses ---
    df_months = (
        df_dict["months"]
        .loc[:, ["real_world_month_name", "ytarria_month_name"]]
        .rename(columns={
            "real_world_month_name": "Mês",
            "ytarria_month_name": "Mês em Yrth"
        })
    )

    # --- Dias da semana ---
    df_days = (
        df_dict["weekdays"]
        .loc[:, ["real_word_day_name", "ytarria_day_name"]]
        .rename(columns={
            "real_word_day_name": "Dia",
            "ytarria_day_name": "Dia em Yrth"
        })
    )

    return df_months, df_days

# ------------------------------------------------------------------------------------------------ #
#   #FUNÇÃO MAIN

def main():
    """
    Página principal do Streamlit responsável por:
    - Ler os arquivos de miscelânea usando a classe ExcelReader
    - Renderizar o conteúdo final
    """

    # Inicializa os dados a serem mostrados
    df_months, df_days = read_ytarria_calendar()

    st.header("📅 Calendário do Mundo de Yrth")

    st.markdown("### Meses do Ano")
    st.dataframe(
        df_months,
        hide_index=True,
        use_container_width=True
    )


# ------------------------------------------------------------------------------------------------ #
main()
