from pprint import pprint
from time import sleep

from live_code_bench.leetcode.contest_ranking import ContestRanking, get_contest_ranking
from live_code_bench.leetcode.submission import Submission, Submissions, get_submission
from live_code_bench.utils.db import save, save_error
from live_code_bench.config import leetcode_contest_ids


def leetcode_get_contest_ranking_by_lang():
    RANKING_PAGE_START = 1
    RANKING_PAGE_END = 10

    LANGS = [
        "python3",
    ]

    ranking_pages = range(RANKING_PAGE_START, RANKING_PAGE_END + 1)

    for contest_id in leetcode_contest_ids:
        print(contest_id)
        result = ContestRanking(
            id=contest_id,
            is_past=True,
            submissions=[],
            questions=[],
            total_rank=[],
            user_num=0,
        )

        for ranking_page in ranking_pages:
            try:
                sleep(1)
                page_result = get_contest_ranking(
                    contest_id,
                    ranking_page,
                )
                result = ContestRanking(
                    id=page_result.id,
                    is_past=page_result.is_past,
                    submissions=result.submissions + page_result.submissions,
                    questions=page_result.questions,
                    total_rank=result.total_rank + page_result.total_rank,
                    user_num=page_result.user_num,
                )

            except Exception as e:
                pprint(e)
                save_error(
                    ContestRanking,
                    contest_id,
                    e,
                )

        save(result)

        all_submissions: dict[int, Submissions] = {}
        done = False
        for submission_dict in result.submissions:
            if done:
                break
            for question_id, submission in submission_dict.items():
                try:
                    if (
                        submission.lang is not None
                        and submission.lang not in LANGS  # ! filter by lang
                    ):
                        continue

                    sleep(1)
                    submission = get_submission(
                        submission.submission_id, submission.data_region, question_id
                    )

                    if submission.lang not in LANGS:  # ! filter by lang
                        # print(
                        #     f"Skipping {submission.lang} "
                        #     f"{submission.id} {question_id}"
                        # )
                        continue

                    # save(submission)

                    if question_id not in all_submissions:
                        all_submissions[question_id] = Submissions(
                            submissions=[submission],
                            contest_id=contest_id,
                            question_id=question_id,
                            id=question_id,
                        )
                    else:
                        all_submissions[question_id].add_submission(submission)

                    if submission.lang == "python3":
                        print(
                            f"Saving {submission.lang}@{submission.id} "
                            f"for {question_id} || "
                            f"len={len(all_submissions[question_id].submissions)}"
                        )

                    if len(all_submissions) == 4 and all(
                        [s.python3_length > 15 for s in all_submissions.values()]
                    ):
                        done = True
                        break

                    save(all_submissions[question_id])

                except Exception as e:
                    pprint(e)
                    import traceback

                    traceback.print_exc()
                    save_error(
                        Submission,
                        submission.id,
                        e,
                    )

        for submissions in all_submissions.values():
            save(submissions)

if __name__ == '__main__':
    leetcode_get_contest_ranking_by_lang()