import os
from pprint import pprint

import dotenv
import requests
from bs4 import BeautifulSoup

from live_code_bench.atcoder.utils import problem_id

LANGUAGE = "Python"
STATUS = "AC"


# Load environment variables from .env file
dotenv.load_dotenv()
ATCODER_SESSION = os.environ["ATCODER_SESSION"]


def extract_submissions_for_problem(
    contest_id: int,
    problem_letter: str,  # * Should be lowercase
    page: int = 1,
):
    problem_id_str = problem_id(contest_id, problem_letter)

    # The URL of the problem status page
    url: str = (
        f"https://atcoder.jp/contests/{contest_id}/submissions?"
        f"f.Task={problem_id_str}&f.LanguageName={LANGUAGE}&f.Status={STATUS}&f.User="
        f"&page={page}"
    )

    # With head Cookie: _csrf_token=...
    headers = {
        "Cookie": f"REVEL_SESSION={ATCODER_SESSION}",
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res_text = res.text

    # Processing
    soup = BeautifulSoup(res_text, "html.parser")

    # Find all <a> with text href f"/contests/{contest_id}/submissions/\d+"
    submission_details = soup.find_all(
        "a",
        href=lambda href: href
        and href.startswith(f"/contests/{contest_id}/submissions/"),
    )

    # FIXME Do things with submission_details

    return submission_details


def main():
    result = extract_submissions_for_problem(
        contest_id="abc319",
        problem_letter="a",
        page=10,
    )
    pprint(result)


if __name__ == "__main__":
    main()
