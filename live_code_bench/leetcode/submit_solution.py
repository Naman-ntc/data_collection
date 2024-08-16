import os
from pprint import pprint
from time import sleep
from typing import Optional

import leetcode
from pydantic.dataclasses import dataclass

from live_code_bench.leetcode import api_instance


def submit_solution(
    question_id: int,
    question_slug: str,
    solution: str,
    lang: str = "python3",
):
    res = api_instance.problems_problem_submit_post(
        problem=question_slug,
        body=leetcode.Submission(
            lang=lang,
            question_id=question_id,
            # question_slug=question_slug,
            typed_code=solution,
            test_mode=False,
            judge_type="large",
        ),
    )

    submission_id = res.submission_id

    # print("Submission has been queued. Result:")
    # print(submission_id)

    num_tries = 0
    while num_tries < 8:
        sleep(3)
        submission_result = api_instance.submissions_detail_id_check_get(
            id=submission_id,
        )
        if submission_result["state"] == "SUCCESS":
            break
        num_tries += 1

    # print("Got submission result:")
    try:
        submission_result["total_correct"]
    except KeyError:
        pprint(submission_result)
    del submission_result["task_name"]
    del submission_result["finished"]

    # pprint(leetcode.SubmissionResult(**submission_result))

    return submission_result  # TODO pydantic dataclass


def main():
    problem_slug = "find-the-safest-path-in-a-grid"

    solution_888_999 = """\
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        return [888, 999]
"""

    solution_one_pass_hash_table = """\
class Solution:
    num_test_cases = 0
    to_be_correct_test_cases = range(1,1030)

    @staticmethod
    def getValidNeighbours(x, y, n):
        neighbours = [(x+1, y), (x-1,y), (x,y+1), (x,y-1)]
        output = []
        for nx, ny in neighbours:
            if nx>=0 and ny>=0 and nx<n and ny<n:
                output.append((nx,ny))
        return output

    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        Solution.num_test_cases += 1
        if Solution.num_test_cases not in Solution.to_be_correct_test_cases:
            return None
        n = len(grid)
        distances = [[0 if val==1 else None for val in valrow] for valrow in grid]
        thief_locs_queue = [(x,y) for y in range(n) for x in range(n) if grid[x][y]]

        while thief_locs_queue:
            new_queue = []
            for tx, ty in thief_locs_queue:
                for ntx, nty in Solution.getValidNeighbours(tx,ty,n):
                    if distances[ntx][nty] is None:
                        distances[ntx][nty] = distances[tx][ty]+1
                        new_queue.append((ntx,nty))
            thief_locs_queue = new_queue

        best_scores = [[-1 for _ in range(n+1)] for _ in range(n+1)]

        from queue import PriorityQueue

        bfs_queue = PriorityQueue()
        bfs_queue.put((-distances[n-1][n-1], n-1,n-1))

        while True:
            dist, x, y = bfs_queue.get()
            if best_scores[x][y] != -1:
                continue
            dist = -dist
            new_dist = min(dist, distances[x][y])
            best_scores[x][y] = new_dist
            if x==0 and y==0:
                break
            for nx, ny in Solution.getValidNeighbours(x,y,n):
                bfs_queue.put((-new_dist, nx, ny))

        return best_scores[0][0]
"""

    result = submit_solution(2914, problem_slug, solution_one_pass_hash_table)
    print(result)
    sleep(10)
    # result = submit_solution(1, problem_slug, solution_one_pass_hash_table)
    # sleep(10)
    # result = submit_solution(1, problem_slug, solution_one_pass_hash_table)
    # sleep(10)
    # result = submit_solution(1, problem_slug, solution_one_pass_hash_table)
    # sleep(10)
    # result = submit_solution(1, problem_slug, solution_one_pass_hash_table)
    # sleep(10)
    # result = submit_solution(1, problem_slug, solution_one_pass_hash_table)
    # sleep(10)


if __name__ == "__main__":
    main()
