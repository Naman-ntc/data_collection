import datetime
import json
from importlib.metadata import version
from pathlib import Path

from pydantic import RootModel

import live_code_bench.atcoder.contest_task
import live_code_bench.atcoder.contests_archive
# import live_code_bench.codeforces.contest
# import live_code_bench.codeforces.contest_submission
# import live_code_bench.codeforces.contests
# import live_code_bench.codeforces.problem_submissions
# import live_code_bench.codeforces.problemset_problem
# import live_code_bench.codeforces.problemset_status_submission
import live_code_bench.leetcode.contest_info
import live_code_bench.leetcode.contest_ranking
import live_code_bench.leetcode.question_details
import live_code_bench.leetcode.submission
from live_code_bench import __package__

__version__ = version(__package__)


SAVE_BASE_DIR = Path("data")
SAVE_VERSION_DIR = SAVE_BASE_DIR / __version__


LOG_BASE_DIR = Path("logs")
LOG_VERSION_DIR = LOG_BASE_DIR / __version__


def pydantic_dataclass_to_path(type_obj: type):
    """
    TODO : use __module__ and __name__ instead of hard coding
    """

    mapping = {
        # live_code_bench.codeforces.contests.ContestGeneral: (
        #     "codeforces/contest_general"
        # ),
        # live_code_bench.codeforces.contest.ContestDetails: (
        #     "codeforces/contest_details"
        # ),
        # live_code_bench.codeforces.problemset_problem.ProblemDetails: (
        #     "codeforces/problem_details"
        # ),
        # live_code_bench.codeforces.contest_submission.SubmissionGeneral: (
        #     "codeforces/submission_general"
        # ),
        # live_code_bench.codeforces.problemset_status_submission.SubmissionDetails: (
        #     "codeforces/submission_details"
        # ),
        # live_code_bench.codeforces.problem_submissions.ProblemSubmissions: (
        #     "codeforces/problem_submissions"
        # ),
        # live_code_bench.codeforces.problemset_status_submission.ProblemIdToTestCases: (
        #     "codeforces/problem_id_to_test_cases"
        # ),
        live_code_bench.atcoder.contests_archive.ContestGeneral: (
            "atcoder/contest_general"
        ),
        live_code_bench.atcoder.contest_task.ProblemDetails: (
            "atcoder/problem_details"
        ),
        live_code_bench.leetcode.contest_info.ContestInfo: ("leetcode/contest_info"),
        live_code_bench.leetcode.question_details.QuestionDetails: (
            "leetcode/question_details"
        ),
        live_code_bench.leetcode.contest_ranking.ContestRanking: (
            "leetcode/contest_ranking"
        ),
        live_code_bench.leetcode.submission.Submission: ("leetcode/submission"),
        live_code_bench.leetcode.submission.Submissions: (
            "leetcode/submission_by_question"
        ),
    }

    return mapping[type_obj]


def get_save_dir(type_obj):
    return SAVE_VERSION_DIR / pydantic_dataclass_to_path(type_obj)


def get_save_error_dir(type_obj):
    return LOG_VERSION_DIR / pydantic_dataclass_to_path(type_obj)


def save(obj):
    _save_dir = get_save_dir(type(obj))
    id = obj.id

    _save_dir.mkdir(parents=True, exist_ok=True)
    save_path = _save_dir / f"{id}.json"

    save_path.write_text(
        RootModel[type(obj)](obj).model_dump_json(indent=2) + "\n",
    )


def save_error(type_obj, id, error):
    _log_dir = get_save_error_dir(type_obj)

    _log_dir.mkdir(parents=True, exist_ok=True)
    log_path = _log_dir / f"{id}.log"

    with log_path.open("a") as f:
        f.write(
            datetime.datetime.now().isoformat()
            + "\t"
            + "ERROR"
            + "\t"
            + str(error)
            + "\n",
        )


def read_as_json(type_obj, id):
    _save_dir = get_save_dir(type_obj)
    save_path = _save_dir / f"{id}.json"
    return json.loads(save_path.read_text())


def read_as_dataclass(type_obj, id):
    _json = read_as_json(type_obj, id)
    return type_obj(**_json)


def get_largest_id(type_obj):
    save_dir = SAVE_VERSION_DIR / pydantic_dataclass_to_path(type_obj)
    return max(int(path.stem) for path in save_dir.glob("*.json"))
