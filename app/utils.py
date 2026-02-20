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
