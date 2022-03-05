"""Handle transactions from marg excel files."""
import os
from collections import defaultdict
from glob import glob

import jsonschema
import pandas as pd
from loguru import logger
from xlrd import open_workbook

from . import constants as c

# from typing import List


"""Handle transactions from marg excel files."""


class TransactionsExcelMarg:
    """Handle transactions from marg excel files."""

    def __init__(self, excelDirectory: str):
        self._excelDirectory = excelDirectory
        self.__generate_valid_dates()
        self.__generate_hashes()

    def _rows(self):
        """Iterate over all rows in all excel files."""
        dtype = {
            "DEBIT": object,
            "CREDIT": object,
        }
        xl_files = []
        xl_files += glob(os.path.join(self._excelDirectory, "*.xlsx"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.XLSX"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.xls"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.XLS"))
        for file in xl_files:
            logger.info(f"Parsing {file}")
            date_range = (
                open_workbook(file)
                .sheet_by_name("MARG ERP 9+ Excel Report")
                .cell(7, 0)
                .value.strip()
            )
            self._start_year = int(date_range.split("-")[2])
            self._end_year = int(date_range.split("-")[5])
            self._df = pd.read_excel(file, skiprows=8, dtype=dtype, na_filter=False)
            logger.info(f"Read file {file} with {len(self._df)} rows")
            for i in range(len(self._df)):
                if self._is_row(i):
                    yield self._rowToDict(i)

    def row_by_item(self, item):
        """Return the row corresponding the item."""
        jsonschema.validate(item, c.JSON_SCHEMA)
        item_date_amount = f"{item['date']}_{item['deposit'] - item['withdraw']}"
        if item_date_amount not in self._date_amount:
            return None
        rows = self._date_amount[item_date_amount]
        if len(rows) == 1:
            return rows[0]
        else:
            print(f"For item={item}")
            print(f"Rows = {rows}")
            raise NotImplementedError("Unable to handle same amount on same days.")

    def _is_row(self, index):
        date = self._df.loc[index, "DATE"].strip()
        return (
            date in self.__valid_dates
            and self._df.loc[index + 1, "PARTICULARS"].strip()
            == "ICICI BANK A/C NO.192105001218"
        )

    def __generate_hashes(self):
        self._date_amount = defaultdict(list)
        for row in self._rows():
            jsonschema.validate(row, c.EXCEL_MARG_SCHEMA)
            date_amount = f"{row['DATE']}_{row['CREDIT'] - row['DEBIT']}"
            self._date_amount[date_amount].append(row)

    def _rowToDict(self, index):
        result = dict(self._df.loc[index])
        # DEBIT : withdraw
        result["DEBIT"] = float(result["DEBIT"]) if result["DEBIT"] else 0
        # CREDIT : deposit
        result["CREDIT"] = float(result["CREDIT"]) if result["CREDIT"] else 0
        date_split = result["DATE"].split()
        day = date_split[1] if len(date_split[1]) == 2 else f"0{date_split[1]}"
        mon = date_split[0]
        year = self._end_year if mon in ["Jan", "Feb", "Mar"] else self._start_year
        result["DATE"] = f"{day}/{mon}/{year}"
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

    def __generate_valid_dates(self):
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        self.__valid_dates = []
        for month in months:
            for date in range(1, 10):
                self.__valid_dates.append(f"{month}  {date}")
            for date in range(10, 32):
                self.__valid_dates.append(f"{month} {date}")
