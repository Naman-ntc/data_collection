import os
import time
from pprint import pprint

from live_code_bench.leetcode.contest_info import ContestInfo, get_contest_info
from live_code_bench.utils.db import save, save_error
from live_code_bench.config import leetcode_contest_ids

def leetcode_get_contest_info():
    for contest_id in leetcode_contest_ids:
        time.sleep(5)
        if os.path.exists(f"data/0.0.1/leetcode/contest_info/{contest_id}.json"):
            continue
        try:
            result = get_contest_info(contest_id)
        except Exception as e:
            print(f"Error for contest_id={contest_id}: {e}")
            save_error(ContestInfo, contest_id, e)
            continue

        save(result)

if __name__ == '__main__':
    leetcode_get_contest_info()