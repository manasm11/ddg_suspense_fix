"""Handle transactions from marg excel files."""
import os
from collections import defaultdict
from datetime import datetime, timedelta
from glob import glob

import jsonschema
import pandas as pd
from loguru import logger
from thefuzz import fuzz
from xlrd import open_workbook

from . import constants as c

# from typing import List


"""Handle transactions from marg excel files."""


class TransactionsExcelMarg:
    """Handle transactions from marg excel files."""

    def __init__(self, excelDirectory: str):
        self._excelDirectory = excelDirectory
        logger.debug("Generating valid dates")
        self.__generate_valid_dates()
        logger.debug("Generating hashes")
        self.__generate_hashes()

    def is_date_in_range(self, date: str) -> bool:
        """Check if date is in the current finanial year or not."""
        financial_year_start = datetime(self._start_year, 4, 1)
        financial_year_end = datetime(self._end_year, 3, 31)
        date = datetime.strptime(date, c.DATE_FORMAT)
        return financial_year_start <= date <= financial_year_end

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
        amount = item["deposit"] - item["withdraw"]
        rows = self._get_rows(item, amount)
        unique_particulars = {row["PARTICULARS"] for row in rows}
        if len(unique_particulars) == 1:
            return rows[0]
        item["sep"] = " " if not item["sep"] else item["sep"]
        particulars = ""
        for row in rows:
            keys = item["party_key"].split(item["sep"])
            match = fuzz.partial_token_set_ratio(row["PARTICULARS"], item["desc"])
            if all([key in row["PARTICULARS"] for key in keys]) or match == 100:
                return row
            particulars = (
                particulars + "    or    " + row["PARTICULARS"]
                if particulars
                else row["PARTICULARS"]
            )
        return {"PARTICULARS": particulars} if particulars else None

    def _get_rows(self, item, amount):
        for i in range(3):
            date = self._date_plus_day(item["date"], i)
            item_date_amount = f"{date}_{amount}"
            i and logger.debug(f"Checking one day after {item_date_amount}")
            if item_date_amount in self._date_amount:
                break
            logger.debug(f"date_amount {item_date_amount} not found")
        rows = self._date_amount[item_date_amount]
        return rows

    def _date_plus_day(self, date: str, days: int):
        item_date = datetime.strptime(date, c.DATE_FORMAT)
        item_date_plus_one = item_date + timedelta(days=days)
        date_plus_one_day = item_date_plus_one.strftime(c.DATE_FORMAT)
        return date_plus_one_day

    def _is_row(self, index):
        date = self._df.loc[index, "DATE"].strip()
        if date not in self.__valid_dates:
            return False
        nextParticular = self._df.loc[index + 1, "PARTICULARS"].strip()
        if nextParticular == c.ICICI_ACC:
            return True
        if (
            nextParticular == "TOTAL"
            and self._df.loc[index + 9, "PARTICULARS"].strip() == c.ICICI_ACC
        ):
            return True
        return False

    def __generate_hashes(self):
        self._date_amount = defaultdict(list)
        for row in self._rows():
            jsonschema.validate(row, c.EXCEL_MARG_SCHEMA)
            # DEBIT means withdraw and CREDIT means deposit
            date_amount = f"{row['DATE']}_{row['CREDIT'] - row['DEBIT']}"
            self._date_amount[date_amount].append(row)
        logger.debug(f"date_amounts found: {list(self._date_amount.keys())}")

    def _rowToDict(self, index) -> dict:
        result = dict(self._df.loc[index])
        result["DEBIT"] = float(result["DEBIT"]) if result["DEBIT"] else 0
        result["CREDIT"] = float(result["CREDIT"]) if result["CREDIT"] else 0
        date_split = result["DATE"].split()
        day = date_split[1] if len(date_split[1]) == 2 else f"0{date_split[1]}"
        mon = date_split[0]
        year = self._end_year if mon in ["Jan", "Feb", "Mar"] else self._start_year
        result["DATE"] = f"{day}/{mon}/{year}"
        return result

    def __generate_valid_dates(self):
        self.__valid_dates = []
        for month in c.MONTHS:
            for date in range(1, 10):
                self.__valid_dates.append(f"{month}  {date}")
            for date in range(10, 32):
                self.__valid_dates.append(f"{month} {date}")
