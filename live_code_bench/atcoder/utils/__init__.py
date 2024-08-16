def problem_id(contest_id, problem_letter: str) -> str:
    problem_letter = problem_letter.lower()

    return f"{contest_id}_{problem_letter}"
