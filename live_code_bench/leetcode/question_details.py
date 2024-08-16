import json
from pprint import pprint
from typing import Any, List, Optional

from bs4 import BeautifulSoup
from leetcode.models.graphql_query import GraphqlQuery
from leetcode.models.graphql_query_get_question_detail_variables import (
    GraphqlQueryGetQuestionDetailVariables,
)
from pydantic.dataclasses import dataclass

from live_code_bench.leetcode import api_instance
from live_code_bench.utils.streamlit import StreamlitMixin


@dataclass
class TopicTag:
    name: str
    slug: str
    translated_name: Optional[str]


@dataclass
class SimilarQuestion:
    title: str
    titleSlug: str
    difficulty: str
    translatedTitle: Optional[str]


@dataclass
class MetaDataParam:
    name: str
    type: str


@dataclass
class MetaData:
    name: str
    params: List[MetaDataParam]
    manual: Optional[bool]


@dataclass
class CodeSnippet:
    lang: str
    lang_slug: str
    code: str


@dataclass(repr=False)
class QuestionDetails(StreamlitMixin):
    id: int
    topic_tags: List[TopicTag]
    title_slug: str
    title: str
    status: Optional[str]
    similar_questions: List[SimilarQuestion]
    sample_test_case: str
    question_frontend_id: str
    mysql_schemas: List[Any]  # TODO What is Any?
    meta_data: MetaData
    judger_available: bool
    judge_type: str
    is_paid_only: bool
    hints: List[str]
    has_video_solution: bool
    has_solution: bool
    enable_test_mode: bool
    enable_run_code: bool
    difficulty: str
    contributors: List[Any]  # TODO What is Any?
    content: str
    code_snippets: List[CodeSnippet]
    category_title: Optional[str]
    bound_topic_id: Optional[int]
    ac_rate: float


def get_question_details(title_slug: str):
    graphql_request = GraphqlQuery(
        query="""
                query getQuestionDetail($titleSlug: String!) {
                  question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    boundTopicId
                    title
                    titleSlug
                    frequency
                    freqBar
                    content
                    translatedTitle
                    isPaidOnly
                    difficulty
                    likes
                    dislikes
                    isLiked
                    isFavor
                    similarQuestions
                    contributors {
                      username
                      profileUrl
                      avatarUrl
                      __typename
                    }
                    langToValidPlayground
                    topicTags {
                      name
                      slug
                      translatedName
                      __typename
                    }
                    companyTagStats
                    codeSnippets {
                      lang
                      langSlug
                      code
                      __typename
                    }
                    stats
                    acRate
                    codeDefinition
                    hints
                    solution {
                      id
                      canSeeDetail
                      __typename
                    }
                    hasSolution
                    hasVideoSolution
                    status
                    sampleTestCase
                    enableRunCode
                    metaData
                    translatedContent
                    judgerAvailable
                    judgeType
                    mysqlSchemas
                    enableTestMode
                    envInfo
                    __typename
                  }
                }
            """,
        variables=GraphqlQueryGetQuestionDetailVariables(
            title_slug=title_slug,
        ),
        operation_name="getQuestionDetail",
    )

    response = api_instance.graphql_post(body=graphql_request)

    data = response.data.question.to_dict()

    # This is for using ID as file name to save as JSON to DB
    data["id"] = data["question_id"]
    del data["question_id"]

    # This is to get rid of HTML tags and clean up the content
    content = data["content"]
    # content = BeautifulSoup(data["content"], "html.parser")
    # content = content.get_text()
    ret = QuestionDetails(
        **{
            **data,
            "content": content,
            "meta_data": {
                "manual": None,
                **json.loads(data["meta_data"]),
            },
            "similar_questions": json.loads(data["similar_questions"]),
        },
    )

    return ret


def get_formatted_question_details(slug="two-sum"):
    result = get_question_details(slug)
    return format_result(result)


import json
from bs4 import BeautifulSoup


def replace_sup_with_marker(soup, marker="^"):
    sup_tags = soup.find_all("sup")
    for sup in sup_tags:
        sup_text = sup.get_text()
        # Replace the <sup> tag with the marker followed by the superscript text
        sup.replace_with(marker + sup_text)
    return soup


def replace_sub_with_marker(soup, marker="_"):
    sub_tags = soup.find_all("sub")
    for sub in sub_tags:
        sub_text = sub.get_text()
        # Replace the <sup> tag with the marker followed by the superscript text
        sub.replace_with(marker + sub_text)
    return soup


def format_result(question):
    sample_code = question.code_snippets
    sample_code = [value.code for value in sample_code if value.lang_slug == "python3"][
        0
    ]
    content = question.content
    difficutly = question.difficulty
    content_soup = BeautifulSoup(content, "html.parser")
    content_soup = replace_sup_with_marker(content_soup)
    content_soup = replace_sub_with_marker(content_soup)
    has_image = content_soup.findAll("img")
    if has_image:
        has_image = all(
            [x.parent.attrs.get("class") == ["example-block"] for x in has_image]
        )
    else:
        has_image = False

    # if has_image:
    #     import pdb

    #     # pdb.set_trace()
    #     # print(has_image.parent.attrs.get("class"))
    #     if has_image:
    #         has_image = False
    soup_text = content_soup.get_text().replace("\u00a0", " ")
    return has_image, content, soup_text, sample_code, difficutly


if __name__ == "__main__":
    print(get_formatted_question_details("maximum-candies-allocated-to-k-children"))#shortest-distance-to-target-string-in-a-circular-array"))
