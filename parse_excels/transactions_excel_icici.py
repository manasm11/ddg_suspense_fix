"""Handle transactions from icici excel files."""
import os
from collections import defaultdict
from glob import glob
from typing import List

import jsonschema
import pandas as pd
from loguru import logger

from . import constants as c

identity_func = lambda a: a


"""Handle transactions from icici excel files."""


class TransactionsExcelIcici:
    """Handle transactions from icici excel files."""

    def __init__(self, excelDirectory: str):
        self._excelDirectory = excelDirectory

    def rows(self):
        """Iterate over all rows in all excel files."""
        dtype = {
            "Withdrawal Amt (INR)": object,
            "Deposit Amt (INR)": object,
        }
        xl_files = []
        xl_files += glob(os.path.join(self._excelDirectory, "*.xlsx"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.XLSX"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.xls"))
        xl_files += glob(os.path.join(self._excelDirectory, "*.XLS"))
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
        jsonschema.validate(dict(row), c.EXCEL_ICICI_SCHEMA)
        result = {
            "date": row["Value Date"],
            "chqno": row["Cheque. No./Ref. No."],
            "desc": str(row["Transaction Remarks"]).upper(),
            "id": row["Tran. Id"],
            "withdraw": self.__to_float(row["Withdrawal Amt (INR)"]),
            "deposit": self.__to_float(row["Deposit Amt (INR)"]),
        }
        self.__desc_details(result)
        return result

    def __desc_details(self, d):
        jsonschema.validate(d, c.JSON_SCHEMA)
        if d["withdraw"]:
            self.chq_descs = defaultdict(str)
            self.__handle_withdraw_desc(d)
        elif d["deposit"]:
            self.__handle_deposit_desc(d)
        else:
            raise Exception("Neither withdraw nor deposit.")

    def __handle_deposit_desc(self, d):
        # NEFT-{REF_NO}-{NAME}-{REMARK}-{ACC_NO}-{IFSC}
        # CLG/{NAME}/{CHQ_NO}/{BANK_NAME}/{DEPOSIT_DATE}
        # MMT/IMPS/{REF_NO}/{REMARK}/{NAME}/{BANK_NAME}
        # RTGS-{REF_NO}-{NAME}-{ACC_NO}-{IFSC}
        # BY CASH  - KANPUR - BIRHANA ROAD
        # UPI/{REF_NO}/{REMARK}/{NAME}/{BANK}/{REF_NO2}
        # INF/INFT/{REF_NO}/{REMARK}/{NAME}
        # TRF/{NAME}/{CHQ_NO}/{BANK}/{DATE}
        # CAM/{REF_NO}/CASH DEP/{DATE}
        # {FD_NO}: REV SWEEP FROM
        # {FD_NO}: CLOSURE PROCEEDS
        # BIL/INFT/{REF_NO}/{REMARK}/{NAME}
        # TRFR FROM:{NAME}
        # THIRD PARTY DEPOSIT
        # BIL/REV PMT ID {REF_NO}
        # INT ON FD/RD {FD_NO}  {REMARK}
        # BY CASH-SHIKOHABAD  FIROZABAD
        # {FD_NO} FD CLOS {REMARK}
        # REV CHQ RET -{REF_NO}/{CHQ_NO}
        # {REF_NO}/NTB
        # RTGS RETURN-ICICR52020022900539720-INTAS PHARMACEUTICALS LTD-INCORRECT ACCOUNT
        # 969420/NBL/SANTOSH AGENCY
        # 971698/SANOTSDH AGENCY
        # 260620_KANPUR_BRK_6022955761
        # 010720_PURANI D_BRK_6022955799
        # 020720_PURANID_BRK_6022955798
        # REV MOB ALRT CHG OCT19+GST
        # REV CHQ BOOK CHG11-20MAR20+GST
        # UPI 029015347931 DT 161020 UPIF361561180D64453B51C013C3F74B1A7
        # FT-BIL REV PMT ID 328535642

        desc: str = d["desc"]
        SANTOSH_AGENCY = "SANTOSH AGENCY"

        substring_funcs = {
            "NEFT-": lambda desc: self.__remove_substrings(desc, "-", [1, 3]),
            "CLG/": lambda desc: self.__remove_substrings(desc, "/", [2, 4]),
            "MMT/IMPS/": lambda desc: self.__remove_substrings(desc, "/", [2, 3])
            if desc.count("/") == 5
            else self.__remove_substrings(desc, "/", [2]),
            "RTGS-": lambda desc: self.__remove_substrings(desc, "-", [1]),
            "BY CASH": identity_func,
            "UPI/": lambda desc: self.__remove_substrings(desc, "/", [1, 2, 5]),
            "INF/INFT/": lambda desc: self.__remove_substrings(desc, "/", [2, 3]),
            "TRF/": lambda desc: self.__remove_substrings(desc, "/", [2, 4]),
            "CAM/": lambda desc: self.__remove_substrings(desc, "/", [1, 3]),
            ": REV SWEEP FROM": lambda desc: desc.split(":")[0],
            ": CLOSURE PROCEEDS": lambda desc: desc.split(":")[0],
            "BIL/INFT/": lambda desc: self.__remove_substrings(
                desc, "/", [2, 3]
            ),  # Doubt
            "TRFR FROM:": identity_func,
            "THIRD PARTY DEPOSIT": identity_func,
            "BIL/REV PMT ID": identity_func,
            "INT ON FD/RD ": lambda desc: desc.split(" ")[3],
            " FD CLOS ": lambda desc: desc.split(" ")[0],
            "REV CHQ RET": lambda desc: " ".join(desc.split(" ")[:3]),
            "/NTB": identity_func,
            "RTGS RETURN-": lambda desc: self.__remove_substrings(desc, "-", [1, 3]),
            "/NBL/": lambda desc: desc.split("/")[2],
            "/SANOTSDH AGENCY": lambda desc: SANTOSH_AGENCY,
            "_KANPUR_BRK_": lambda desc: self.__remove_substrings(desc, "_", [0, 3]),
            "_PURANI D_BRK_": lambda desc: self.__remove_substrings(desc, "_", [0, 3]),
            "_PURANID_BRK_": lambda desc: self.__remove_substrings(desc, "_", [0, 3]),
            "REV MOB ALRT CHG ": lambda desc: c.BANK_CHARGES,
            "REV CHQ BOOK ": lambda desc: c.BANK_CHARGES,
            "UPI 029015347931 DT 161020": identity_func,
            "FT-BIL REV PMT ID ": identity_func,
            "SELF DEPOSIT": identity_func,
            "UPI 136551282438 31 12 2021 YBL0E8F558680D44DDCA584A6FE43DD6993": identity_func,
            "GST ADJ TRAN FOR S21846176/24-03-2022": identity_func,
            "CHRG ADJ TRAN FOR S21846176/24-03-2022": identity_func,
        }
        for substring in substring_funcs:
            if substring in desc:
                self._sep = ""
                d["party_key"] = substring_funcs[substring](desc)
                d["sep"] = self._sep
                assert isinstance(
                    d["party_key"], str
                ), f"party_key for {d} is of type {type(d['party_key'])}"
                assert isinstance(
                    d["sep"], str
                ), f"sep for {d} is of type {type(d['sep'])}"
                break
        else:
            raise Exception(f"Unable to handle deposit description for {d}")

    def __handle_withdraw_desc(self, d):
        # INF/NEFT/{REF_NO}/{IFSC}/{NAME}
        # MMT/IMPS/{REF_NO}/{ACC_NO}/{NAME}/{IFSC}
        # MMT/IMPS/205312507380/KUMAR MEDI/CANARA BANK
        # INF/INFT/{REF_NO}/{NAME}
        # CLG/{NAME}/{BANK}
        # TRF/{NAME}/{BANK}
        # REJECT:{CHQ_NO}:{REASON}
        # GIB/{REF_NO}/{REMARK}/{REF_NO_2}
        # MOB ALRT CHG {REMARK}
        # RTN CHG-{CHQ_NO}/{REMARK}/{DATE}
        # CHQ BOOK CHG {REMARK}
        # BIL/ONL/{REF_NO}/{NAME}/{REMARK}
        # TRFR TO:{NAME}
        # TRF TO FD/RD {FD_NO} DURGA DAWA GHAR
        # {FD_NO}:INT.COLL:{REMARK}
        # MAOVET ANIMAL HEALTH CARE
        # BIL/{REF_NO}/BILL DESK (CORPORATE/QICO79431841
        # BIL/001791897887//BSNLPOST_QICI79
        # DBT CARD CHG AUG-19+GST
        # TRF TO FD NO. 192110001349
        # CHQ RTN {CHQ_NO}
        # SGST201912051476755019
        # CGST201912051476755023
        # NEFT:{REF_NO}/{IFSC}/{NAME}
        # RTGS:{REF_NO}/{IFSC}/{NAME}
        # RAUNAK SALES & MARKETING
        # INS NO:511
        # DSB SERV CHGS JUN'20 DURGA DAW
        # SGST202007091963970550
        # CGST202007091963970552
        # 140820_6022955768_BRK_KAN_S
        # CASH DEP CHG 22JUL21+GST
        # RTGS/ICICR42022020600500827/HDFC0000298/CRESCENTLIFESCIENCE/0298897000005420220

        desc: str = d["desc"]

        substring_funcs = {
            "INF/NEFT/": lambda desc: self.__remove_substrings(desc, "/", [2]),
            "MMT/IMPS/": lambda desc: self.__remove_substrings(desc, "/", [2]),
            "INF/INFT/": lambda desc: self.__remove_substrings(desc, "/", [2]),
            "CLG/": lambda desc: self.chq_descs.__setitem__(d["chqno"], desc) or desc,
            "TRF/": lambda desc: self.chq_descs.__setitem__(d["chqno"], desc) or desc,
            "REJECT:": lambda desc: self.chq_descs[desc.split(":")[1]],
            "GIB/": lambda desc: self.__remove_substrings(desc, "/", [1, 2, 3]),
            "MOB ALRT CHG": lambda desc: c.BANK_CHARGES,
            "RTN CHG-": lambda desc: c.BANK_CHARGES,
            "CHQ BOOK CHG": lambda desc: c.BANK_CHARGES,
            "BIL/ONL/": lambda desc: self.__remove_substrings(desc, "/", [2, 4]),
            "TRFR TO:": identity_func,
            "TRF TO FD/RD ": lambda desc: desc.split(" ")[3],
            ":INT.COLL:": lambda desc: desc.split(":")[0],
            "MAOVET ANIMAL HEALTH CARE": identity_func,
            "QICO79431841": lambda desc: self.__remove_substrings(desc, "/", [1]),
            "BSNLPOST_QICI79": lambda desc: self.__remove_substrings(desc, "/", [1]),
            "DBT CARD CHG": lambda desc: c.BANK_CHARGES,
            "TRF TO FD NO. ": lambda desc: desc.split(" ")[4],
            "CHQ RTN ": lambda desc: c.BANK_CHARGES,
            "SGST201912051476755019": lambda desc: c.GST,
            "CGST201912051476755023": lambda desc: c.GST,
            "NEFT:": lambda desc: self.__remove_substrings(desc, "/", [0]),
            "RTGS:": lambda desc: self.__remove_substrings(desc, "/", [0]),
            "RAUNAK SALES & MARKETING": identity_func,
            "INS NO:": identity_func,
            "DSB SERV CHGS ": lambda desc: c.BANK_CHARGES,
            "SGST202007091963970550": lambda desc: c.GST,
            "CGST202007091963970552": lambda desc: c.GST,
            "_BRK_KAN_": lambda desc: self.__remove_substrings(desc, "_", [0, 1]),
            "CASH DEP CHG ": lambda desc: c.BANK_CHARGES,
            "RTGS/": lambda desc: self.__remove_substrings(desc, "/", [1, 4]),
            "BIL/BPAY/IC3109943304/BBPS/KANPUR ELECTRICIT": identity_func,
        }
        for substring in substring_funcs:
            if substring in desc:
                self._sep = ""
                d["party_key"] = substring_funcs[substring](desc)
                d["sep"] = self._sep
                assert isinstance(
                    d["party_key"], str
                ), f"party_key for {d} is of type {type(d['party_key'])}"
                assert isinstance(
                    d["sep"], str
                ), f"sep for {d} is of type {type(d['sep'])}"
                break
        else:
            raise Exception(f"Unable to handle withdraw description for {d}")

    def __remove_substrings(self, string: str, seperator: str, indexes: List[int]):
        assert (
            seperator in string
        ), f"String '{string}' doesn't contains seperator '{seperator}'"
        self._sep = seperator
        return seperator.join(
            [ss for i, ss in enumerate(string.split(seperator)) if i not in indexes]
        )
