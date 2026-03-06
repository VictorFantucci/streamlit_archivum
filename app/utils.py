"""
Script que contém as utilidades do projeto.
"""

# ------------------------------------------------------------------------------------------------ #
# IMPORT

import os

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES

utils_directory = os.path.dirname(os.path.dirname(__file__)).rstrip('.')

# ------------------------------------------------------------------------------------------------ #
# CONSTANTES SOBRE TIERS
TIER_ORDER = ["Comum", "Boa", "Superior", "Excelente", "Obra-Prima"]

TIER_COLORS = {
    "Comum": "#374151",
    "Boa": "#22C55E",
    "Superior": "#3B82F6",
    "Excelente": "#A855F7",
    "Obra-Prima": "#F97316",
}

TIER_CONFIG = {
    "Comum": {"min_nh": 8, "divisor": 4},
    "Boa": {"min_nh": 10, "divisor": 5},
    "Superior": {"min_nh": 12, "divisor": 6},
    "Excelente": {"min_nh": 14, "divisor": 7},
    "Obra-Prima": {"min_nh": 16, "divisor": 16},
}


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
        "logs": os.path.join("app", "logs"),
        "data": os.path.join("app", "data"),
        "app": "app",
        "assets": os.path.join("app", "asseets"),
        "pages": os.path.join("app", "pages"),
        "components": os.path.join("app", "components"),
    }

    try:
        if folder_name not in folders:
            raise ValueError(f"Pasta desconhecida: {folder_name}")

        return os.path.join(utils_directory, folders[folder_name])

    except Exception as e:
        print(f"Erro ao obter pasta: {e}")
        raise
