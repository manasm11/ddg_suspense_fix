"""Handle transactions excel file."""
import os
from glob import glob

import pandas as pd
from loguru import logger

"""Handle transactions excel file."""


class TransactionsExcel:
    """Handle transactions excel file."""

    def __init__(self, excelDirectory: str):
        self._excelDirectory = excelDirectory

    def rows(self):
        """Iterate over all rows in all excel files."""
        dtype = {
            "Withdrawal Amt (INR)": object,
            "Deposit Amt (INR)": object,
        }
        for file in glob(os.path.join(self._excelDirectory, "*.xlsx")):
            logger.info(f"Parsing {file}")
            for _, row in pd.read_excel(file, skiprows=16, dtype=dtype).iterrows():
                if pd.isna(row["Balance (INR)"]):
                    break
                yield self._rowToDict(row)

    def __to_float(self, numberString):
        if pd.isna(numberString):
            return 0
        numberString = numberString.replace(",", "")
        return float(numberString)

    def _rowToDict(self, row):
        return {
            "sno": row["S.N."],
            "date": row["Value Date"],
            "chqno": row["Cheque. No./Ref. No."] or "",
            "desc": row["Transaction Remarks"],
            "id": row["Tran. Id"],
            "withdraw": self.__to_float(row["Withdrawal Amt (INR)"]),
            "deposit": self.__to_float(row["Deposit Amt (INR)"]),
        }
