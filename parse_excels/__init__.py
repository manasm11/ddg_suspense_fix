"""Entry point to parse_excels."""
from .read_excel import TransactionsExcel


def generate_json_from_excels(inExcelDirectory: str, outJsonFile: str):
    """Convert excel row to a json file."""
    excelReader = TransactionsExcel(inExcelDirectory)
    for row in excelReader.rows():
        print(row)
