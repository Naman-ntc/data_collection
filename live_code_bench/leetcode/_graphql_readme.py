"""
! Not used

Only for demo purposes
"""


import os
from pprint import pprint

import dotenv
import leetcode
import leetcode.auth

from live_code_bench.leetcode import api_instance


def main():
    graphql_request = leetcode.GraphqlQuery(
        query="""
        {
            user {
            username
            isCurrentUserPremium
            }
        }
        """,
        variables=leetcode.GraphqlQueryVariables(),
    )

    print(api_instance.graphql_post(body=graphql_request))

    # --------------------------------------------------

    api_response = api_instance.api_problems_topic_get(topic="algorithms")

    slug_to_solved_status = {
        pair.stat.question__title_slug: True if pair.status == "ac" else False
        for pair in api_response.stat_status_pairs
    }

    import time
    from collections import Counter

    topic_to_accepted = Counter()
    topic_to_total = Counter()

    # Take only the first 10 for test purposes
    for slug in list(slug_to_solved_status.keys())[:10]:
        time.sleep(1)  # Leetcode has a rate limiter

        graphql_request = leetcode.GraphqlQuery(
            query="""
                query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    topicTags {
                    name
                    slug
                    }
                }
                }
            """,
            variables=leetcode.GraphqlQueryGetQuestionDetailVariables(
                title_slug=slug,
            ),
            operation_name="getQuestionDetail",
        )

        api_response = api_instance.graphql_post(body=graphql_request)

        for topic in (tag.slug for tag in api_response.data.question.topic_tags):
            topic_to_accepted[topic] += int(slug_to_solved_status[slug])
            topic_to_total[topic] += 1

    pprint(
        list(
            sorted(
                (
                    (topic, accepted / topic_to_total[topic])
                    for topic, accepted in topic_to_accepted.items()
                ),
                key=lambda x: x[1],
            )
        )
    )


if __name__ == "__main__":
    main()
