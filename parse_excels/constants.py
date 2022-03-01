"""Constants to be used by modules."""
ROW_SCHEMA = {
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
