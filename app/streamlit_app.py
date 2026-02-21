"""
Entrypoint / Router do Archivum.
"""

# ------------------------------------------------------------------------------------------------ #
# IMPORTS
import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Archivum",
    page_icon="🗂️",
    layout="wide")

# ------------------------------------------------------------------------------------------------ #
# IMPORTS RELATIVOS
from utils import get_project_folder

# ------------------------------------------------------------------------------------------------ #
# PATH SETUP
app_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(app_directory)

pages_folder = get_project_folder("pages")

# ------------------------------------------------------------------------------------------------ #
# PAGES

home = st.Page(os.path.join(pages_folder, "archivum.py"), title="Home", icon="🏛️")

# Páginas sobre a ficha do personagem
attributes = st.Page(os.path.join(pages_folder, "character", "attributes.py"),
                     title="Atributos",
                     icon="📝")

adv_dis = st.Page(os.path.join(pages_folder, "character", "advantages_and_disadvantages.py"),
                     title="Vantagens e Desvantagens",
                     icon="🔰")

skills = st.Page(os.path.join(pages_folder, "character", "skills.py"),
                     title="Perícias",
                     icon="🛠️")

# Páginas sobre itens
weapons = st.Page(os.path.join(pages_folder, "itens", "weapons.py"),
                     title="Armas",
                     icon="⚔️")

# Páginas sobre alquimia
alchemy = st.Page(os.path.join(pages_folder, "alchemy", "alchemy.py"),
                     title="Consumíveis",
                     icon="⚗️")

# Páginas sobre magia
grimory = st.Page(os.path.join(pages_folder, "magic", "grimory.py"),
                     title="Grimório",
                     icon="🔮")

# Páginas sobre o mundo de Yrth
calendar = st.Page(os.path.join(pages_folder, "yrth", "calendar.py"),
                     title="Calendário de Ytarria",
                     icon="📅")


# ------------------------------------------------------------------------------------------------ #
# NAVIGATION

pg = st.navigation(
    pages =
    {
        "Archivum": [home],
        "Personagem": [attributes, adv_dis, skills],
        "Itens": [weapons],
        "Alquimia": [alchemy],
        "Magia": [grimory],
        "Yrth": [calendar]
    },
    expanded=False
)

pg.run()