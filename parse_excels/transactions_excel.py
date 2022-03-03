"""Handle transactions excel file."""
import os
from glob import glob

import jsonschema
import pandas as pd
from loguru import logger

from . import constants as c

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
        xlsx_files = glob(os.path.join(self._excelDirectory, "*.xlsx"))
        xls_files = glob(os.path.join(self._excelDirectory, "*.xls"))
        xl_files = xlsx_files + xls_files
        for file in xl_files:
            logger.info(f"Parsing {file}")
            df = pd.read_excel(file, skiprows=16, dtype=dtype, na_filter=False)
            for _, row in df.iterrows():
                if not row["Balance (INR)"]:
                    break
                yield self._rowToDict(row)

    def __to_float(self, numberString: str):
        if not numberString:
            return 0
        numberString = numberString.replace(",", "")
        return float(numberString)

    def _rowToDict(self, row):
        jsonschema.validate(row, c.EXCEL_SCHEMA)
        result = {
            "date": row["Value Date"],
            "chqno": row["Cheque. No./Ref. No."],
            "desc": row["Transaction Remarks"],
            "id": row["Tran. Id"],
            "withdraw": self.__to_float(row["Withdrawal Amt (INR)"]),
            "deposit": self.__to_float(row["Deposit Amt (INR)"]),
        }
        result.update(self.__desc_details(result))
        return result

    def __desc_details(self, d):
        jsonschema.validate(d, c.JSON_SCHEMA)
        if d["withdraw"]:
            # INF/NEFT/{REF_NO}/{IFSC}/{NAME}
            # CLG/{NAME}/{BANK}
            # MMT/IMPS/{REF_NO}/{ACC_NO}/{NAME}/{IFSC}
            # TRF/{NAME}/{BANK}
            # REJECT:{CHQ_NO}:{REASON}
            # GIB/{REF_NO}/{REMARK}/{REF_NO_2}
            return d
        elif d["deposit"]:
            # NEFT-{REF_NO}-{NAME}-{REMARK}-{ACC_NO}-{IFSC}
            # CLG/{NAME}/{CHQ_NO}/{BANK_NAME}/{DEPOSIT_DATE}
            # MMT/IMPS/{REF_NO}/{REMARK}/{NAME}/{BANK_NAME}
            # RTGS-{REF_NO}-{NAME}-{ACC_NO}-{IFSC}
            # BY CASH -KANPUR - BIRHANA ROAD
            # UPI/{REF_NO}/{REMARK}/{NAME}/{BANK}
            return d
        else:
            raise Exception("Neither withdraw nor deposit.")
