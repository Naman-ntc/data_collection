import re
from pprint import pprint
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from pydantic.dataclasses import dataclass

from live_code_bench.atcoder.utils import problem_id
from live_code_bench.utils.streamlit import StreamlitMixin


@dataclass(repr=False)
class ProblemDetails(StreamlitMixin):
    id: str
    contest_id: str

    # scraped
    title: str
    time_limit: str
    memory_limit: str
    score: int
    question: str
    constraints: str
    input_spec: str
    output_spec: str
    sample_tests: List[Tuple[str, str]]
    sample_tests_explained: List[Tuple[str, str]] = None


def get_problem_details(
    contest_id: str,
    problem_letter: str,  # * Should be lowercase
):
    problem_id_str = problem_id(contest_id, problem_letter)

    res = requests.get(
        f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id_str}",
    )

    res.raise_for_status()
    res_text = res.text

    # Processing
    res_text = res_text.replace("</h3>", "\n\n</h3>")
    res_text = res_text.replace("<li>", "<li>- ")

    # Soup
    soup = BeautifulSoup(res_text, "html.parser")

    # Find span with class "h2"
    h2 = soup.find("span", {"class": "h2"})
    # Remove <a> inside
    h2.a.decompose()
    # Get text
    title = h2.text.split("-")[1].strip()

    # Find <p> with text "Time Limit: ..."
    time_limit_p = soup.find("p", string=re.compile(r"Time Limit:"))
    time_limit_p_text = time_limit_p.text.strip()
    time_limit = time_limit_p_text.split("/")[0].split(":")[1].strip()

    # Find <p> with text "Memory Limit: ..."
    memory_limit_p = soup.find("p", string=re.compile(r"Memory Limit:"))
    memory_limit_p_text = memory_limit_p.text.strip()
    memory_limit = memory_limit_p_text.split("/")[1].split(":")[1].strip()

    # Find <p> that is like <p>Score : <var>200</var> points</p>
    score_p = soup.find(
        lambda tag: tag.name == "p"
        and "Score" in tag.text
        and "points" in tag.text
        and tag.find("var")
    )
    score_p_text = score_p.text.strip()
    score = int(score_p_text.split(":")[1].split("points")[0].strip())

    # Find <h3> with text "Problem Statement"
    problem_statement_h3 = soup.find("h3", string=re.compile(r"Problem Statement"))
    problem_statement_h3_parent = problem_statement_h3.parent
    problem_statement = problem_statement_h3_parent.text.strip()

    # Find <h3> with text "Constraints"
    constraints_h3 = soup.find("h3", string=re.compile(r"Constraints"))
    constraints_h3_parent = constraints_h3.parent
    constraints = constraints_h3_parent.text.strip()

    # Find <h3> with text "Input"
    input_h3 = soup.find("h3", string=re.compile(r"Input"))
    input_h3_parent = input_h3.parent
    input_spec = input_h3_parent.text.strip()

    # Find <h3> with text "Output"
    output_h3 = soup.find("h3", string=re.compile(r"Output"))
    output_h3_parent = output_h3.parent
    output_spec = output_h3_parent.text.strip()

    # Find <h3> with text "Sample Input X" and <h3> with text "Sample Output X"
    sample_input_h3s = soup.find_all("h3", string=re.compile(r"Sample Input"))
    sample_output_h3s = soup.find_all("h3", string=re.compile(r"Sample Output"))

    sample_tests = []
    sample_tests_explained = []
    for sample_input_h3, sample_output_h3 in zip(sample_input_h3s, sample_output_h3s):
        sample_input_h3_parent = sample_input_h3.parent
        sample_input = sample_input_h3_parent.find("pre").text.strip()

        sample_output_h3_parent = sample_output_h3.parent
        sample_output = sample_output_h3_parent.find("pre").text.strip()

        sample_tests.append((sample_input, sample_output))
        sample_tests_explained.append(
            (
                sample_input_h3_parent.text.strip(),
                sample_output_h3_parent.text.strip(),
            )
        )

    return ProblemDetails(
        id=problem_id_str,
        contest_id=contest_id,
        title=title,
        time_limit=time_limit,
        memory_limit=memory_limit,
        score=score,
        question=problem_statement,
        constraints=constraints,
        input_spec=input_spec,
        output_spec=output_spec,
        sample_tests=sample_tests,
        sample_tests_explained=sample_tests_explained,
    )


def main():
    contest_id = "abc282"#abc312"
    problem_letter = "d"

    result = get_problem_details(contest_id, problem_letter)
    pprint(result.__dict__)


if __name__ == "__main__":
    main()
