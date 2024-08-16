import time

from live_code_bench.leetcode.question_details import (
    QuestionDetails,
    get_question_details,
    format_result
)
from live_code_bench.utils.db import save, save_error


def transform_question(formatted_result):
    (has_img, content_html, content, sample_code, difficulty) = formatted_result
    sample_code_parsing = sample_code + "\n        pass"
    try:
        tree = ast.parse(sample_code_parsing)
    except:
        print(f"Skipping {slug} due to {sample_code}")
        return False
    
    if has_img:
        print(f"Skipping {slug} due to image")
        return False

    if slug.endswith("-ii"):
        print(f"Skipping {slug} since duplicate")
        return False

    bad_keywords = [
        "there are multiple",
        "there are two",
        "return any of them",
        "return any one",
        "return either of",
    ]

    ## used in v1
    bad_question_ids = [
        2836,
        3143,
        3165,
        2826,
        3241,
    ]

    if any([keyword in content.lower() for keyword in bad_keywords]):
        print(f"Skipping {slug} due to bad keywords")
        return False

    # Past Heuristics

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
    return question_dict

def leetcode_get_problem_details():
    all_questions_filtered = []
    for problem_slug in problem_slugs:
        time.sleep(5)
        try:
            result = get_question_details(problem_slug)
            formatted_result = format_result(result)

            question_dict_or_false = transform_question(formatted_result)
            if not question_dict_or_false:
                print(question_dict_or_false)
                continue
        except Exception as e:
            print(f"Error for {problem_slug=}: {e}")
            save_error(QuestionDetails, problem_slug, e)
            continue

        all_questions_filtered.append(question_dict_or_false)
        save(result)

    return all_questions_filtered

if __name__ == '__main__':
    import json
    import glob
    contests = glob.glob("data/0.0.1/leetcode/contest_info/*.json")
    problem_slugs = []
    for contest in contests:
        contest_info = json.load(open(contest))
        for question in contest_info["questions"]:
            problem_slugs.append(question["title_slug"])
    
    filtered_questions = leetcode_get_problem_details()

    difficulties = set([question["difficulty"] for question in filtered_questions])
    difficulty_counts = {difficulty: 0 for difficulty in difficulties}
    for question in filtered_questions:
        difficulty_counts[question["difficulty"]] += 1
    
    print(difficulty_counts)

    with open("data/0.0.1/leetcode/questions_v1_filtered.json", "w") as f:
        json.dump(filtered_questions, f)
