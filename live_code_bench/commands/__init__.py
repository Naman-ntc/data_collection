from ._register import register_command
from .atcoder_get_contest_info import atcoder_get_contest_info
from .atcoder_get_problem_details import atcoder_get_problem_details
from .leetcode_get_contest_info import leetcode_get_contest_info
# from .leetcode_get_contest_ranking import leetcode_get_contest_ranking
from .leetcode_get_contest_ranking_by_lang import leetcode_get_contest_ranking_by_lang
# from .leetcode_get_problem_details import leetcode_get_problem_details
# from .codeforces_get_problem_submissions import codeforces_get_problem_details

for _name, _func in locals().copy().items():
    if callable(_func) and _func not in [
        register_command,
    ]:
        register_command(_func)
