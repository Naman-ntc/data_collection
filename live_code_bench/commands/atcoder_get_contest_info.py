import time
from pprint import pprint

from live_code_bench.atcoder.contests_archive import (
    ContestGeneral,
    get_contests_general,
)
from live_code_bench.utils.db import save, save_error


def atcoder_get_contest_info():
    most_recent_page = 1
    num_pages = 1  # 1 is enough for frequent updates

    for page in range(
        most_recent_page,
        most_recent_page + num_pages,
    ):
        time.sleep(1)

        try:
            results = get_contests_general(page)
        except Exception as e:
            print(f"Error for page={page}: {e}")
            save_error(ContestGeneral, f"page_{page}", e)
            continue

        for result in results:
            save(result)

if __name__ == '__main__':
    atcoder_get_contest_info()