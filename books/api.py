import re
import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class BookDetails:
    title: str
    description: Optional[str]
    olid: str


OPEN_LIBRARY_INFO_URL = re.compile(r"https://openlibrary.org/books/(OL[\w\d]+)/.+")


def olid_from_info_url(info_url: str) -> str:
    return OPEN_LIBRARY_INFO_URL.search(info_url).group(1)


def fetch_book_details(isbn: str) -> BookDetails:
    resp = requests.get(
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=details",
    )
    resp.raise_for_status()
    data = resp.json()
    book = data[f"ISBN:{isbn}"]
    details = book["details"]
    description = details.get("description", {}).get("value")
    return BookDetails(
        title=details["title"],
        description=description,
        olid=olid_from_info_url(book["info_url"]),
    )

