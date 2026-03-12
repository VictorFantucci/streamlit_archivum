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
TIER_ORDER = [1, 2, 3, 4, 5]

TIER_COLORS = {
    1: "#374151",
    2: "#22C55E",
    3: "#3B82F6",
    4: "#A855F7",
    5: "#F97316",
}

TIER_CONFIG = {
    1: {"min_nh": 8, "divisor": 4},
    2: {"min_nh": 10, "divisor": 5},
    3: {"min_nh": 12, "divisor": 6},
    4: {"min_nh": 14, "divisor": 7},
    5: {"min_nh": 16, "divisor": 16},
}

TIER_NAME_SETS = {

    "qualidade": {
        1: "Comum",
        2: "Boa",
        3: "Superior",
        4: "Excelente",
        5: "Obra-Prima",
    },

    "raridade": {
        1: "Comum",
        2: "Incomum",
        3: "Raro",
        4: "Épico",
        5: "Lendário",
    },

    "habilidade": {
        1: "Aprendiz",
        2: "Experiente",
        3: "Veterano",
        4: "Especialista",
        5: "Mestre",
    }

}

def tier_name_to_level(name, tier_set):
    mapping = TIER_NAME_SETS[tier_set]
    for level, n in mapping.items():
        if n == name:
            return level
    return None

def tier_level_to_name(level, tier_set):
    return TIER_NAME_SETS[tier_set].get(level, str(level))

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
