"""Handle transactions from marg excel files."""
import os
from glob import glob

import jsonschema
import pandas as pd
from loguru import logger

from . import constants as c

# from typing import List


"""Handle transactions from marg excel files."""


class TransactionsExcelMarg:
    """Handle transactions from marg excel files."""

    def __init__(self, excelDirectory: str):
        self._excelDirectory = excelDirectory
        self.__generate_hashes()

    def rows(self):
        """Iterate over all rows in all excel files."""
        dtype = {
            "DEBIT": object,
            "CREDIT": object,
        }
        xlsx_files = glob(os.path.join(self._excelDirectory, "*.xlsx"))
        xls_files = glob(os.path.join(self._excelDirectory, "*.xls"))
        xl_files = xlsx_files + xls_files
        for file in xl_files:
            logger.info(f"Parsing {file}")
            df = pd.read_excel(file, skiprows=8, dtype=dtype, na_filter=False)
            for _, row in df.iterrows():
                yield self._rowToDict(row)

    def row_by_item(self, item):
        """Return the row corresponding the item."""
        pass

    # def __to_float(self, numberString: str):
    #     if not numberString:
    #         return 0
    #     numberString = numberString.replace(",", "")
    #     return float(numberString)

    def __generate_hashes(self):
        for row in self.rows():
            jsonschema.validate(row, c.EXCEL_MARG_SCHEMA)

    def _rowToDict(self, row):
        result = {}
        return result
        # jsonschema.validate(dict(row), c.EXCEL_ICICI_SCHEMA)
        # result = {
        #     "date": row["Value Date"],
        #     "chqno": row["Cheque. No./Ref. No."],
        #     "desc": str(row["Transaction Remarks"]).upper(),
        #     "id": row["Tran. Id"],
        #     "withdraw": self.__to_float(row["Withdrawal Amt (INR)"]),
        #     "deposit": self.__to_float(row["Deposit Amt (INR)"]),
        # }
        # self.__desc_details(result)
        # return result
