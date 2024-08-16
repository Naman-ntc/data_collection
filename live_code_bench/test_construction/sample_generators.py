import os
import json
import time

import openai
import numpy as np
from openai.types.chat import ChatCompletion

from run_models.multiprocess_utils import run_tasks_in_parallel_iter

EXAMPLE_QUESTION_SOLUTION = """###Problem
You have k bags. You are given a 0-indexed integer array weights where weights[i] is the weight of the ith marble. You are also given the integer k.

Divide the marbles into the k bags according to the following rules:

No bag is empty.
If the i^th marble and j^th marble are in a bag, then all marbles with an index between the i^th and j^th indices should also be in that same bag.
If a bag consists of all the marbles with an index from i to j inclusively, then the cost of the bag is weights[i] + weights[j].
The score after distributing the marbles is the sum of the costs of all the k bags.

Return the difference between the maximum and minimum scores among marble distributions.

Example 1:

Input: weights = [1,3,5,1], k = 2
Output: 4
Explanation: 
The distribution [1],[3,5,1] results in the minimal score of (1+1) + (3+1) = 6. 
The distribution [1,3],[5,1], results in the maximal score of (1+3) + (5+1) = 10. 
Thus, we return their difference 10 - 6 = 4.
Example 2:

Input: weights = [1, 3], k = 2
Output: 0
Explanation: The only distribution possible is [1],[3]. 
Since both the maximal and minimal score are the same, we return 0.
 

Constraints:

1 <= k <= weights.length <= 10^5
1 <= weights[i] <= 10^9

### Solution

```python
class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        pref = []
        for i in range(len(weights) - 1):
            pref.append(weights[i] + weights[i + 1])
        
        pref.sort()
        ans = 0
        
        for i in range(k - 1):
            ans += (pref[-(i + 1)] - pref[i])
        
        return ans
```
"""

RANDOM_GENERATOR = """
import numpy as np
def random_input_generator(weight_min, weight_max, size_min, size_max):
    weights_size = np.random.randint(size_min, size_max+1)
    weights = np.random.randint(weight_min, weight_max, size=weights_size).tolist()
    k = np.random.randint(1, len(weights)+1)
    return weights, k

def construct_inputs():
    inputs_list = []
    ## small inputs
    for i in range(15):
        inputs_list.append(random_input_generator(1, 10**3, 1, 10))
    ## medium inputs
    for i in range(15):
        inputs_list.append(random_input_generator(1, 10**6, 1, 10**3))
    ## large inputs
    for i in range(15):
        inputs_list.append(random_input_generator(1, 10**9, 1, 10**5))
    return inputs_list
"""


ADVERSARIAL_GENERATOR = """
import numpy as np
## case 1 - alternating large and small weights
def generate_adversarial_inputs_1(weight_size, max_weight, k):
    weights = [1 if i%2==0 else max_weight for i in range(weight_size)]
    return weights, k

## case 2 - equal_weights
def adversarial_input_generator_2(weight_size, max_weight, k):
    weights = [max_weight for _ in range(weight_size)]
    return weights, k

# Case 3 - Large weights at the ends
def adversarial_input_generator_3(weight_size, max_weight, k):
    weights = [1 for _ in range(weight_size)]
    weights[0] = max_weight
    weights[-1] = max_weight
    return weights, k

# Case 4 - Sparse large weights randomly
def adversarial_input_generator_4(weight_size, max_weight, k):
    weights = [1 for _ in range(weight_size)]
    for i in range(weight_size//10):
        weights[np.random.randint(0, weight_size)] = max_weight
    return weights, k

def construct_inputs():
    inputs_list = []

    weight_sizes = [10, 1000, 100000]
    max_weights = [10**3, 10**6, 10**9]

    for weight_size in weight_sizes:
        for max_weight in max_weights:
            ks = [1, 2, 5, weight_size//2, weight_size-1, weight_size]
            for k in ks:
                inputs_list.append(generate_adversarial_inputs_1(weight_size, max_weight, k))
                inputs_list.append(adversarial_input_generator_2(weight_size, max_weight, k))
                inputs_list.append(adversarial_input_generator_3(weight_size, max_weight, k))
                inputs_list.append(adversarial_input_generator_4(weight_size, max_weight, k))

    return inputs_list        
"""

client = openai.Client(api_key=os.environ["OPENAI_KEY"])


def get_response(chat_messages, n):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=chat_messages,
            temperature=0.4,
            max_tokens=1024,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            n=n,
        )
    except (
        openai.APIError,
        openai.RateLimitError,
        openai.InternalServerError,
        openai.OpenAIError,
        openai.APIStatusError,
        openai.APITimeoutError,
        openai.InternalServerError,
        openai.APIConnectionError,
    ) as e:
        print("Exception: ", e, "Sleeping for 20 seconds...")
        time.sleep(20)
        return get_response(chat_messages)
    except Exception as e:
        print("Exception: ", e)
        return []
    return response


def extract_code_from_response(response: ChatCompletion):
    codes = []
    for output in response.choices:
        output = output.message.content
        outputlines = output.splitlines()
        backtick_line_indices = [i for i, x in enumerate(outputlines) if "```" in x]

        ## extract code from backtick pairs
        for i in range(len(backtick_line_indices) // 2):
            code = "\n".join(
                outputlines[
                    backtick_line_indices[2 * i] + 1 : backtick_line_indices[2 * i + 1]
                ]
            )
            code += "\n"
            codes.append(code)

    return codes


def get_generators_from_question(inp):
    question_solution = inp
    SYSTEM_MESSAGE = "You are an expert python competitive programmar and your goal is to construct input-generators for testing programming contest problems. You will write relevant generators and finally construct `construct_inputs` function that returns a list of diverse inputs sampled from the generator. Remember to strictly follow the instructions and constraints present in the problem statement."
    INSTRUCTION = f"Construct a random input generator. Use the format used in the above example by returning a single function that builds diverse inputs named `construct_inputs`."
    base_messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {
            "role": "user",
            "content": f"{EXAMPLE_QUESTION_SOLUTION}\n\nConstruct a random input generator.",
        },
        {
            "role": "assistant",
            "content": f"Following is an input generator function enclosed in backtics.\n\n```python\n{RANDOM_GENERATOR}\n```",
        },
        {
            "role": "user",
            "content": f"{question_solution}\n\n{INSTRUCTION}",
        },
    ]

    with open("random.json", "w") as f:
        json.dump(base_messages, f, indent=4)

    response = get_response(base_messages, 2)
    random_codes = extract_code_from_response(response)

    INSTRUCTION = f"Construct an adversarial input generator. Use the format used in the above example by returning a single function that builds diverse inputs named `construct_inputs`."
    base_messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE,
        },
        {
            "role": "user",
            "content": f"{EXAMPLE_QUESTION_SOLUTION}\n\nConstruct an adversarial input generator.",
        },
        {
            "role": "assistant",
            "content": f"Following is an input generator function enclosed in backtics.\n\n```python\n{ADVERSARIAL_GENERATOR}\n```",
        },
        {
            "role": "user",
            "content": f"{question_solution}\n\nC{INSTRUCTION}",
        },
    ]

    with open("adversarial.json", "w") as f:
        json.dump(base_messages, f, indent=4)

    response = get_response(base_messages, 4)
    adversarial_codes = extract_code_from_response(response)

    return {"random": random_codes, "adversarial": adversarial_codes}


def main():
    with open("data/0.0.1/leetcode/questions_v1.json", "r") as f:
        questions = json.load(f)

    question_solutions = []
    filtered_questions = []

    for question in questions:
        if os.path.exists(
            f'data/0.0.1/leetcode/generators/{question["question_id"]}.json'
        ):
            continue
        filtered_questions.append(question)
        with open(
            f"data/0.0.1/leetcode/submission_by_question/{question['question_id']}.json"
        ) as fp:
            submissions = json.load(fp)["submissions"]
            python_submissions = [s for s in submissions if s["lang"] == "python3"]

        question_solutions.append(
            f"###Problem\n{question['content']}\n\n### Solution\n\n```python\n{python_submissions[0]['code']}\n```"
        )

    print(len(question_solutions))
    outputs = run_tasks_in_parallel_iter(
        get_generators_from_question, question_solutions, 12, use_progress_bar=True
    )

    all_generators = {}
    for question, output in zip(filtered_questions, outputs):
        if output.is_exception():
            print(output.exception_tb)
            exit()

        with open(
            f"data/0.0.1/leetcode/generators/{question['question_id']}.json", "w"
        ) as f:
            json.dump(output.result, f, indent=4)


if __name__ == "__main__":
    main()
