"""Server to be used by frontend."""
import json
from collections import defaultdict

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

logger.add("logs/debug_{time}.log", level="DEBUG")
logger.add("logs/error_{time}.log", level="ERROR")

TRANSACTIONS_JSON_FILE = "../output_jsons/transactions.json"


class PartyMapping:
    """Handle logic to search for party by description."""

    def __init__(self, filepath: str):
        self._filepath: str = filepath
        self._all_transactions: list = self._get_all_transactions()
        self._mappings: dict = self._get_mappings()

    def _get_all_transactions(self):
        transactions = []
        with open(self._filepath) as f:
            transactions = json.load(f)
        return transactions

    def _get_mappings(self):
        mappings = defaultdict(set)
        unique_pairs = set()
        for transaction in self._all_transactions:
            transaction: dict
            if not transaction.get("party_key") or not transaction.get("party_name"):
                continue
            pair = transaction["party_key"] + transaction["party_name"]
            if pair in unique_pairs:
                continue
            unique_pairs.add(pair)
            mappings[transaction["party_key"]].add(transaction["party_name"])
        return mappings

    def search(self, query: str) -> list:
        """Search and return list of possible parties."""
        party_names = set()
        for party_key in self._mappings:
            is_substring = self._search_substring(query, party_key)
            if is_substring:
                party_names = party_names.union(self._mappings[party_key])
        return list(party_names)

    def _search_substring(self, query, party_key):
        j = 0
        for char in party_key:
            found, j = self.__find_char_after_j(query, j, char)
            if not found:
                return False
        return True

    def __find_char_after_j(self, query, j, char):
        found = False
        while j < len(query):
            if query[j] == char:
                found = True
                break
            j += 1
        return found, j


origins = [
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_header(func):
    """Check Header."""

    def _(must_header=Header(None), *args, **kwargs):
        if must_header == "JAI MATA DI":
            return func(*args, **kwargs)
        return []

    return _


party_map = PartyMapping(TRANSACTIONS_JSON_FILE)


@app.get("/")
async def root():
    """Root endpoint to test if server is running."""
    return {"message": "SERVER IS ON"}


@app.get("/possible-parties")
async def possible_parties(desc, must_header=Header(None)):
    """Get possible_parties with the given desc."""
    logger.info(f"Header {must_header}")
    logger.info(f"desc={desc}")
    search_result = party_map.search(desc)
    logger.debug(f"search_result={list(search_result)}")
    return search_result
