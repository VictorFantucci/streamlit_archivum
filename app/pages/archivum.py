"""
Script que contém o projeto streamlit, temporário, do Archivum.
"""

# ------------------------------------------------------------------------------------------------ #
# IMPORTS
import os
import sys
import streamlit as st

# ------------------------------------------------------------------------------------------------ #
# IMPORTS RELATIVOS
from utils import get_project_folder

# ------------------------------------------------------------------------------------------------ #
# PATH SETUP
app_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(app_directory)

# ------------------------------------------------------------------------------------------------ #
# STREAMLIT MAIN PAGE

def main() -> None:
    st.header("Archivum")

    st.markdown("***")

    st.markdown(
        """
        <p style='text-align: center;'>
        “Toda lenda precisa de um guardião. O Archivum preserva as histórias,
        os segredos e a alma do meu universo — porque conhecimento é poder.
        Arquive-o.”
        </p>
        """,
        unsafe_allow_html=True
    )


main()
