# scrape data


from pprint import pprint
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pydantic.dataclasses import dataclass


@dataclass
class TestCaseDetails:
    case_name: str
    status: str
    exec_time: str
    memory: str


@dataclass
class SubmissionDetails:
    id: int
    contest_id: str
    problem_id: str

    # scraped

    source_code: str

    submission_time: str
    user: str
    language: str
    score: int
    code_size: str
    status: str
    exec_time: Optional[str]
    memory: Optional[str]

    test_cases: list[TestCaseDetails]

    compiler_error: Optional[str] = None


def get_submission_details(
    contest_id: str,
    submission_id: int,
):
    res = requests.get(
        f"https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}",
    )

    res.raise_for_status()
    res_text = res.text

    # Processing
    soup = BeautifulSoup(res_text, "html.parser")

    # Find <pre> with id "submission-code"
    source_code = soup.find("pre", {"id": "submission-code"})
    source_code = source_code.text.strip()

    # Find first table
    table = soup.find("table")

    # Find all <tr>
    trs = table.find_all("tr")

    submission_time = trs[0].find("td").text.strip()

    _, _, _contest_id, _, problem_id = [
        s.strip() for s in trs[1].find("a")["href"].split("/")
    ]
    assert _contest_id == contest_id

    user = trs[2].find("td").text.strip()
    language = trs[3].find("td").text.strip()
    score = trs[4].find("td").text.strip()
    code_size = trs[5].find("td").text.strip()
    status = trs[6].find("td").text.strip()
    exec_time = trs[7].find("td").text.strip() if len(trs) > 7 else None
    memory = trs[8].find("td").text.strip() if len(trs) > 8 else None

    # Find last table
    table = soup.find_all("table")[-1]

    # Find all <tr>
    trs = table.find_all("tr")

    test_cases = []
    if [th.text for th in trs[0].find_all("th")] == [
        "Case Name",
        "Status",
        "Exec Time",
        "Memory",
    ]:
        for tr in trs[1:]:
            tds = tr.find_all("td")
            test_cases.append(
                TestCaseDetails(
                    case_name=tds[0].text.strip(),
                    status=tds[1].text.strip(),
                    exec_time=tds[2].text.strip(),
                    memory=tds[3].text.strip(),
                ),
            )

    # Find <pre> with h4 above it having text "Compile Error"
    compiler_error = None
    h4s = soup.find_all("h4")
    for h4 in h4s:
        if h4.text == "Compile Error":
            compiler_error_pre = (
                h4.next_sibling
                if h4.next_sibling.name == "pre"
                else h4.next_sibling.next_sibling
            )
            compiler_error = compiler_error_pre.text.strip()
            break

    submission_details = SubmissionDetails(
        id=submission_id,
        contest_id=contest_id,
        problem_id=problem_id,
        source_code=source_code,
        submission_time=submission_time,
        user=user,
        language=language,
        score=score,
        code_size=code_size,
        status=status,
        exec_time=exec_time,
        memory=memory,
        test_cases=test_cases,
        compiler_error=compiler_error,
    )

    return submission_details


def main():
    result = get_submission_details(
        contest_id="abc319",
        submission_id=45460972,
    )
    pprint(result)


if __name__ == "__main__":
    main()
