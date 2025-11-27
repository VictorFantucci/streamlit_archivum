
# ------------------------------------------------------------------------------------------------ #
# IMPORT

import logging
import pandas as pd
from r4ven_utils.log4me import r4venLogManager

# ------------------------------------------------------------------------------------------------ #
# CLASSE PARA LEITURA DE EXCEL

class ExcelReader:
    def __init__(self, log_dir: str, file_path: str):
        """
        Inicializa o ExcelReader com o caminho para o arquivo Excel.
        """
        self.file_path = file_path
        # Inicializa o gerenciador de log
        self.log_manager = r4venLogManager(log_dir)

    def get_logger(self):
        """ Retorna dinamicamente o logger para este arquivo. """
        return self.log_manager.function_logger(
            __file__,
            console_level=logging.WARNING
        )

    def get_sheet_names(self) -> list:
        """
        Retorna uma lista com os nomes de todas as abas do arquivo Excel.
        """
        log4me = self.get_logger()

        try:
            xls = pd.ExcelFile(self.file_path)
            sheet_names = xls.sheet_names
            log4me.info(f"Nomes de abas encontrados: {sheet_names}")
            return sheet_names
        except Exception as e:
            log4me.error(f"Erro ao ler os nomes das abas: {e}")
            return []

    def load_sheets(self, ignore_sheets: list = None) -> dict:
        """
        Carrega todas as abas do arquivo Excel para um dicionário de DataFrames.

        Parâmetros
        ----------
        ignore_sheets : list
            Lista com os nomes das abas que devem ser ignoradas. Padrão = None.

        Retorno
        -------
        dict
            Dicionário onde a chave é o nome da aba e o valor é o DataFrame correspondente.
        """
        log4me = self.get_logger()
        ignore_sheets = set(ignore_sheets or [])
        sheets_dict = {}

        try:
            xls = pd.ExcelFile(self.file_path)
        except Exception as e:
            log4me.error(f"Erro ao abrir o arquivo Excel '{self.file_path}': {e}")
            return sheets_dict

        for sheet in xls.sheet_names:
            if sheet in ignore_sheets:
                log4me.info(f"Aba ignorada: {sheet}")
                continue

            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet)
                sheets_dict[sheet] = df
                log4me.info(f"Aba carregada com sucesso: {sheet}")
            except Exception as e:
                log4me.error(f"Erro ao carregar a aba '{sheet}': {e}")

        return sheets_dict
