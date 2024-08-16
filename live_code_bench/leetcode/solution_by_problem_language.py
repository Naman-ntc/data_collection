import os
import json
import requests
from tqdm import tqdm
from time import sleep
import dotenv

from live_code_bench.leetcode.selenium_leetCode import SeleniumLeetCode
from live_code_bench.leetcode.login_users import users


dotenv.load_dotenv()
leetcode_session = os.environ["LEETCODE_SESSION"]


def get_solution_by_problem_language(problem_id: int, language: str):
    sl = SeleniumLeetCode(
        username="kingh0730",
        password=users["kingh0730"],
        # geckodriver_location="/home/kingh0730/bin/geckodriver",
    )

    def submit_at_runtime(runtime):
        sleep(2)
        res_json = sl.submissions_by_problem_lang_runtime(problem_id, language, runtime)
        if "code" in res_json:
            return res_json["code"]
        elif (
            "error" in res_json
            and res_json["error"] == "No submission code for passed time/lang."
        ):
            return None
        else:
            print(
                res_json,
                f"Problem ID: {problem_id}, Language: {language}, Runtime: {runtime}",
            )
            return None

    RUNTIMES = []
    RUNTIMES += list(range(100, 1500, 100))
    RUNTIMES += list(range(150, 1500, 100))
    RUNTIMES += list(range(175, 2775, 200))
    RUNTIMES += list(range(275, 2775, 200))
    RUNTIMES += list(range(128, 4000, 160))
    RUNTIMES += list(range(168, 4000, 160))
    RUNTIMES += list(range(208, 4000, 160))
    RUNTIMES += list(range(248, 4000, 160))

    codes: dict[int, str] = {}
    for runtime in tqdm(RUNTIMES):
        output = submit_at_runtime(runtime)
        if output:
            codes[runtime] = output
            break

    print(f"Found {len(codes)} solutions")
    return codes


if __name__ == "__main__":
    with open("data/0.0.1/leetcode/questions.json") as f:
        questions = json.load(f)

    codes_by_problems = {}
    for question in tqdm(questions):
        question_id = question["question_id"]

        codes = get_solution_by_problem_language(question_id, "python3")
        if codes:
            codes_by_problems[question_id] = codes
        else:
            print(f"Did not find solution for {question_id}!!!!!!!!!!!!!!")

        with open("data/0.0.1/leetcode/solutions.json", "w") as f:
            json.dump(codes_by_problems, f)
