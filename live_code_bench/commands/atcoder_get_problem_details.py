import os
import time
from pathlib import Path
from pprint import pprint

import tqdm

from live_code_bench.atcoder.contest_task import ProblemDetails, get_problem_details
from live_code_bench.atcoder.utils import problem_id
from live_code_bench.utils.db import save, save_error
from live_code_bench.config import atcoder_contest_ids


def atcoder_get_problem_details():
    for contest_id in tqdm.tqdm(atcoder_contest_ids):
        for problem_letter in [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
        ]:

            if os.path.exists(
                f"data/0.0.1/atcoder/problem_details/{contest_id}_{problem_letter}.json"
            ):

                print(f"Skipping {contest_id}_{problem_letter} as found")
                continue

            time.sleep(10)

            try:
                result = get_problem_details(contest_id, problem_letter)
            except Exception as e:
                id = problem_id(contest_id, problem_letter)
                print(f"Error for problem_id={id}: {e}")
                save_error(ProblemDetails, id, e)
                continue

            save(result)

if __name__ == '__main__':
    atcoder_get_problem_details()