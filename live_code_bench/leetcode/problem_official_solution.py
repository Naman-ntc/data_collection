from pprint import pprint

from leetcode.models.graphql_query import GraphqlQuery
from leetcode.models.graphql_query_get_question_detail_variables import (
    GraphqlQueryGetQuestionDetailVariables,
)

from live_code_bench.leetcode import api_instance

query = """\
query officialSolution($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    solution {
      id
      title
      content
      contentTypeId
      paidOnly
      hasVideoSolution
      paidOnlyVideo
      canSeeDetail
      rating {
        count
        average
        userRating {
          score
        }
      }
      topic {
        id
        commentCount
        topLevelCommentCount
        viewCount
        subscribed
        solutionTags {
          name
          slug
        }
        post {
          id
          status
          creationDate
          author {
            username
            isActive
            profile {
              userAvatar
              reputation
            }
          }
        }
      }
    }
  }
}
"""


def get_official_solution(title_slug: str):
    graphql_request = GraphqlQuery(
        query=query,
        variables=GraphqlQueryGetQuestionDetailVariables(
            title_slug=title_slug,
        ),
        operation_name="officialSolution",
    )

    response = api_instance.graphql_post(body=graphql_request)
    return response  # TODO pydantic dataclass


def main():
    response = get_official_solution(title_slug="two-sum")
    pprint(response)


if __name__ == "__main__":
    main()
