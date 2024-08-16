"""
! Not used

We prefer to get question details by GraphQL
"""


import re
from pprint import pprint
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from pydantic.dataclasses import dataclass


@dataclass
class ProblemDetails:
    id: int
    id_kebab: str
    contest_id: str

    # scraped
    title: str
    question: str
    constraints: str

    user_accepted: int
    user_tried: int
    total_accepted: int
    total_submissions: int
    difficulty: str

    sample_tests: List[Tuple[str, str]]  # Compatible with other platforms
    sample_tests_explanation: List[str]  # Unique to LeetCode

    starter_code: str


def get_problem_details(
    contest_id: str,
    problem_id_kebab: int,
):
    res = requests.get(
        f"https://leetcode.com/contest/{contest_id}/problems/{problem_id_kebab}",
    )

    res.raise_for_status()
    res_text = res.text

    # ! Need to login to access this page


def main():
    contest_id = "weekly-contest-261"
    problem_id_kebab = "minimum-moves-to-convert-string"

    result = get_problem_details(contest_id, problem_id_kebab)

    pprint(result)


if __name__ == "__main__":
    main()
