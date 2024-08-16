# scrape data

from pprint import pprint

import requests
from bs4 import BeautifulSoup
from pydantic.dataclasses import dataclass


@dataclass
class ContestDetails:
    id: int

    # scraped
    name: str
    # FIXME questions
