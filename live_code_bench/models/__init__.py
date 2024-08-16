from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class LanguageModel:
    name: str
    repr: str
    release_date: datetime


models_dict = {
    "gpt-3.5-turbo-0301": LanguageModel(
        name="gpt35turbo",
        repr="GPT-3.5-Turbo-0301",
        release_date=datetime(2021, 10, 1),
    ),
    "gpt-4": LanguageModel(
        name="gpt4",
        repr="GPT-4",
        release_date=datetime(2021, 10, 1),
    ),
    "gpt-4-1106-preview": LanguageModel(
        name="gpt4turbo",
        repr="GPT-4-Turbo-1106",
        release_date=datetime(2023, 5, 1),
    ),
    # "gpt-4-1106-preview-nonverbose": LanguageModel(
    #     name="gpt4turbo_nonverbose",
    #     repr="gpt4turbo_nonverbose",
    #     release_date=datetime(2021, 3, 1),
    # ),
    "claude-2": LanguageModel(
        name="claude2",
        repr="Claude-2",
        release_date=datetime(2022, 12, 31),
    ),
    "claude-2.1": LanguageModel(
        name="claude21",
        repr="Claude-2.1",
        release_date=datetime(2022, 12, 31),
    ),
    "claude-instant-1": LanguageModel(
        name="claudeinstant1",
        repr="Claude-Instant-1",
        release_date=datetime(2022, 12, 31),
    ),
    # "command": LanguageModel(
    #     name="coherecommand",
    #     repr="coherecommand",
    #     release_date=datetime(2021, 3, 1),
    # ),
    "deepseek-ai/deepseek-coder-33b-instruct": LanguageModel(
        name="deepseek33instruct",
        repr="DeepSeek-33B-Instruct",
        release_date=datetime(2023, 8, 1),
    ),
    "deepseek-ai/deepseek-coder-6.7b-instruct": LanguageModel(
        name="deepseek7instruct",
        repr="DeepSeek-6.7B-Instruct",
        release_date=datetime(2023, 8, 1),
    ),
    "codellama/CodeLlama-34b-Instruct-hf": LanguageModel(
        name="cllama34instruct",
        repr="CodeLLaMa-34B-Instruct",
        release_date=datetime(2023, 1, 1),
    ),
    "codellama/CodeLlama-13b-Instruct-hf": LanguageModel(
        name="cllama13instruct",
        repr="CodeLLaMa-13B-Instruct",
        release_date=datetime(2023, 1, 1),
    ),
    "codellama/CodeLlama-7b-Instruct-hf": LanguageModel(
        name="cllama7instruct",
        repr="CodeLLaMa-7B-Instruct",
        release_date=datetime(2023, 1, 1),
    ),
    "WizardLM/WizardCoder-Python-34B-V1.0": LanguageModel(
        name="wizardcoder_34b",
        repr="WizardCoder-34B",
        release_date=datetime(2023, 1, 1),
    ),
}
