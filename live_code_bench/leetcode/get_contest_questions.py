import tqdm
import json
import glob
import ast
from live_code_bench.leetcode.question_details import get_formatted_question_details

contest_paths1 = [
    f"data/0.0.1/leetcode/contest_info/weekly-contest-{d}.json" for d in range(400, 411)
]
contest_paths2 = [
    f"data/0.0.1/leetcode/contest_info/biweekly-contest-{d}.json"
    for d in range(132, 137)
]
contest_paths = contest_paths1 + contest_paths2

all_questions = []

with open("data/0.0.1/leetcode/questions_v1.json") as f:
    all_questions = json.load(f)


for contest_path in tqdm.tqdm(contest_paths):
    with open(contest_path) as f:
        contest = json.load(f)

    # print(contest_path)

    for question in contest["questions"]:
        # if question["question_id"] in BAD_QUESTION_IDS:
        #     continue
        slug = question["title_slug"]
        if slug.endswith("-ii"):
            print(f"Skipping {slug}")
            continue
        try:
            (
                has_img,
                content_html,
                content,
                sample_code,
                difficulty,
            ) = get_formatted_question_details(slug)
        except:
            print(f"Error for {slug}")
            continue

        credit = question["credit"]
        # if difficulty == "Medium" and credit > 5:
        #     print(f"Medium with credit {credit} || {slug}")
        #     continue
        # if difficulty == "Hard" and credit > 6:
        #     print(f"Hard with credit {credit} || {slug}")
        #     continue
        # if "\u2295" in content:
        #     continue
        # if len(content) > 2000 and difficulty != "Easy":
        #     continue

        sample_code_parsing = sample_code + "\n        pass"
        try:
            tree = ast.parse(sample_code_parsing)
        except:
            print(sample_code)
            continue

        if has_img:
            print(f"Skipping {slug} due to image")

        if not has_img:
            question_dict = {
                "contest_slug": contest["contest"]["title_slug"],
                "question_slug": slug,
                "id": question["id"],
                "question_id": question["question_id"],
                "content_html": content_html,
                "content": content,
                "sample_code": sample_code,
                "difficulty": difficulty,
                "credit": credit,
            }
            exists = any(
                [q["question_id"] == question["question_id"] for q in all_questions]
            )
            if not exists:
                all_questions.append(question_dict)

print(f"Collected {len(all_questions)} questions.")
with open("data/0.0.1/leetcode/questions_v1.json", "w") as f:
    json.dump(all_questions, f, indent=4)
