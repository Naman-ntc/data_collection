"""
! Not used

We prefer solutions here:
https://leetcode.com/contest/weekly-contest-357/ranking/1/
"""


# ruff: noqa: E501


from leetcode.models.graphql_query import GraphqlQuery

from live_code_bench.leetcode import api_instance

graphql_request = GraphqlQuery(
    query="""\
query communitySolutions($questionSlug: String!, $skip: Int!, $first: Int!, $query: String, $orderBy: TopicSortingOption, $languageTags: [String!], $topicTags: [String!]) {
  questionSolutions(
    filters: {questionSlug: $questionSlug, skip: $skip, first: $first, query: $query, orderBy: $orderBy, languageTags: $languageTags, topicTags: $topicTags}
  ) {
    hasDirectResults
    totalNum
    solutions {
      id
      title
      commentCount
      topLevelCommentCount
      viewCount
      pinned
      isFavorite
      solutionTags {
        name
        slug
      }
      post {
        id
        status
        voteStatus
        voteCount
        creationDate
        isHidden
        author {
          username
          isActive
          nameColor
          activeBadge {
            displayName
            icon
          }
          profile {
            userAvatar
            reputation
          }
        }
      }
      searchMeta {
        content
        contentType
        commentAuthor {
          username
        }
        replyAuthor {
          username
        }
        highlights
      }
    }
  }
}
""",
    variables={
        "first": 15,
        "languageTags": [],
        "orderBy": "hot",
        "query": "",
        "questionSlug": "two-sum",
        "skip": 0,
        "topicTags": [],
    },
    operation_name="communitySolutions",
)

response = api_instance.graphql_post(body=graphql_request)

print(response)
