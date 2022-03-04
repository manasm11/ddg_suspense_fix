"""Constants to be used by modules."""

BANK_CHARGES = "BANK CHARGES"
GST = "GST"

JSON_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://example.com/object1646141331.json",
    "title": "Root",
    "type": "object",
    "required": ["date", "chqno", "desc", "id", "withdraw", "deposit"],
    "properties": {
        "date": {
            "$id": "#root/date",
            "title": "Date",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "chqno": {
            "$id": "#root/chqno",
            "title": "Chqno",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "desc": {
            "$id": "#root/desc",
            "title": "Desc",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "id": {
            "$id": "#root/id",
            "title": "Id",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "withdraw": {
            "$id": "#root/withdraw",
            "title": "Withdraw",
            "type": "number",
            "default": 0.0,
        },
        "deposit": {
            "$id": "#root/deposit",
            "title": "Deposit",
            "type": "number",
            "default": 0.0,
        },
    },
}

EXCEL_ICICI_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://example.com/object1646212592.json",
    "title": "Root",
    "type": "object",
    "required": [
        "S.N.",
        "Tran. Id",
        "Value Date",
        "Transaction Date",
        "Transaction Posted Date",
        "Cheque. No./Ref. No.",
        "Transaction Remarks",
        "Withdrawal Amt (INR)",
        "Deposit Amt (INR)",
        "Balance (INR)",
    ],
    "properties": {
        "S.N.": {
            "$id": "#root/S.N.",
            "title": "S.n.",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Tran. Id": {
            "$id": "#root/Tran. Id",
            "title": "Tran. id",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Value Date": {
            "$id": "#root/Value Date",
            "title": "Value date",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Transaction Date": {
            "$id": "#root/Transaction Date",
            "title": "Transaction date",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Transaction Posted Date": {
            "$id": "#root/Transaction Posted Date",
            "title": "Transaction posted date",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Cheque. No./Ref. No.": {
            "$id": "#root/Cheque. No./Ref. No.",
            "title": "Cheque. no./ref. no.",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Transaction Remarks": {
            "$id": "#root/Transaction Remarks",
            "title": "Transaction remarks",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Withdrawal Amt (INR)": {
            "$id": "#root/Withdrawal Amt (INR)",
            "title": "Withdrawal amt (inr)",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Deposit Amt (INR)": {
            "$id": "#root/Deposit Amt (INR)",
            "title": "Deposit amt (inr)",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
        "Balance (INR)": {
            "$id": "#root/Balance (INR)",
            "title": "Balance (inr)",
            "type": "string",
            "default": "",
            "pattern": "^.*$",
        },
    },
}
