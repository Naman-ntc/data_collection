### LeetCode

WEEKLY_CONTEST_ID_START = 409
WEEKLY_CONTEST_ID_END = 410

_weekly_contest_ids = [
    f"weekly-contest-{i}"
    for i in range(WEEKLY_CONTEST_ID_START, WEEKLY_CONTEST_ID_END + 1)
]

leetcode_contest_ids = _weekly_contest_ids


# BIWEEKLY_CONTEST_ID_START = 132
# BIWEEKLY_CONTEST_ID_END = 136

# _biweekly_contest_ids = [
#     f"biweekly-contest-{i}"
#     for i in range(BIWEEKLY_CONTEST_ID_START, BIWEEKLY_CONTEST_ID_END + 1)
# ]

# leetcode_contest_ids = _weekly_contest_ids  + _biweekly_contest_ids



### AtCoder
ATCODER_ABC_START_ID = 364
ATCODER_ABC_END_ID = 365

abc_ids = range(ATCODER_ABC_START_ID, ATCODER_ABC_END_ID+1)
atcoder_contest_ids = [f"abc{id}" for id in abc_ids]