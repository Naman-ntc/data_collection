import json
import subprocess
from time import sleep
from pprint import pprint
from typing import Dict, List, Optional

import requests
from pydantic.dataclasses import dataclass

from live_code_bench.leetcode.utils import contest_ranking_id

ContestRankingQuestionId = int


@dataclass
class ContestRankingSubmission:
    id: int
    date: int
    question_id: int
    submission_id: int
    status: int
    contest_id: int
    data_region: str
    fail_count: int
    lang: Optional[str]


@dataclass
class ContestRankingQuestion:
    id: int
    question_id: int
    credit: int
    title: str
    title_slug: str


@dataclass
class ContestRankingUserBadge:
    icon: str
    display_name: str


@dataclass
class ContestRankingUser:
    contest_id: int
    username: str
    username_color: Optional[str]
    user_badge: Optional[ContestRankingUserBadge]
    user_slug: str
    country_code: str
    country_name: Optional[str]
    rank: int
    score: int
    finish_time: int
    global_ranking: int
    data_region: str


@dataclass
class ContestRanking:
    id: str
    is_past: bool
    submissions: List[Dict[ContestRankingQuestionId, ContestRankingSubmission]]
    questions: List[ContestRankingQuestion]
    total_rank: List[ContestRankingUser]
    user_num: int


def subprocess_curl(contest_id, ranking_page):
    cmd = f"""curl 'https://leetcode.com/contest/api/ranking/{contest_id}/?pagination={ranking_page}' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: gr_user_id=32499272-87cd-499d-8267-d8be1522c7d7; 87b5a3c3f1a55520_gr_last_sent_cs1=naman1205jain; __stripe_mid=32c88075-ddd5-456f-82c0-d3ed11b7ea50afb849; __gpi=UID=00000a4051697fb9:T=1699249197:RT=1699249197:S=ALNI_MaZbbctApfY6GoaiQ-CgXdqiF5IHA; cf_clearance=.rVmOBJdtd1iM52JDXayS07UMSM4eYA7cV1XZyU8pao-1711989583-1.0.1.1-qtGcpUYbSv9RC9fnEaOwuy1bs4nElI3eEDFr.DBJ7_We_0MljkcTbt4ogr5VEOewHX2MndrP0qeC24i0XWt5RA; csrftoken=uDCJbpfYBluUPuAYjvTAmGnAETBasKij7gKIun0bx7CdAnNfLnBGwfz4pxqc56pQ; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWK-Ql5ibmGRoZmGYlZubpKcXq4DIiMr9UISOxLBWmPb-0BJ9yKtg4zB0dCwDOIJBl:1rrKhL:GcblLIP9DNzg_Y53IvVCqxRU_kSgMZ1H15sQZC14Bf8; __gads=ID=b71860d3dcf24813-22148070e7e700db:T=1699249197:RT=1711989599:S=ALNI_MavQ-6jP42HbKx3ruaDGB99WNgugw; __eoi=ID=37d80cca431bbefb:T=1711989599:RT=1711989599:S=AA-AfjYgGZ_vfC4QUwAWPZWrkJk4; FCNEC=%5B%5B%22AKsRol-KrleO1mgGUoh9t3OvAZYd7uebnjbrL24JliSM96c3Qtl_RYK3n6N5lgGosAVB7m7D7vOkSsI3msBV9mWzpzdjfyoaB084snRwDf456iNfk9DjAvMIlqpRcU0ApmQZw0dLHbmhdtN1TvO1iCs0jbEZ2ppgMA%3D%3D%22%5D%5D; __cf_bm=d3cCKAV9Vw9_QbEBDh5K7HLW5L3gkR2ncysgChKFy9M-1717270558-1.0.1.1-E3Tx7o25Jw4KuJ5vtffkx46QbJCYrLWm.dN_iwkswOH7ZNJZCeKShKILaEflyhyhOGkqScZ7vCsBQsyawuYB3Q; _gid=GA1.2.983665159.1717270558; 87b5a3c3f1a55520_gr_session_id=45155865-8f6e-4a48-9af5-3c3b49cda908; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=45155865-8f6e-4a48-9af5-3c3b49cda908; 87b5a3c3f1a55520_gr_session_id_sent_vst=45155865-8f6e-4a48-9af5-3c3b49cda908; INGRESSCOOKIE=7d81156bedcdbcb5edfdff7756d94e1d|8e0876c7c1464cc0ac96bc2edceabd27; __stripe_sid=e21b79c6-982e-4cab-90cd-f90db83b88c868cf43; _ga=GA1.2.277596681.1697782084; 87b5a3c3f1a55520_gr_cs1=naman1205jain; _ga_CDRWKZTDEX=GS1.1.1717270558.38.1.1717270582.36.0.0; _dd_s=rum=0&expire=1717271496506' \
  -H 'dnt: 1' \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'"""

    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # print(output.stdout)
    return output.stdout


def get_contest_ranking(contest_id, ranking_page):
    # # print(
    # #     f"https://leetcode.com/contest/api/ranking/{contest_id}/?pagination={ranking_page}"
    # # )
    # headers = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "accept-language": "en-US,en;q=0.9",
    #     "cache-control": "max-age=0",
    #     "dnt": "1",
    #     "priority": "u=0, i",
    #     "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
    #     "sec-ch-ua-mobile": "?1",
    #     "sec-ch-ua-platform": "Android",
    #     "sec-fetch-dest": "document",
    #     "sec-fetch-mode": "navigate",
    #     "sec-fetch-site": "none",
    #     "sec-fetch-user": "?1",
    #     "upgrade-insecure-requests": "1",
    #     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    #     # "cookie": "__stripe_mid=c37fcc42-c814-40a8-8c3a-a0dcc13759295c1628; cf_clearance=ulYeISH87dqHq.Ea5XK3z4K4jjb222squDdS1zgoGSE-1711990126-1.0.1.1-y6rf.ziQUywhDuRzXn5jxVYrwmqBvvic5ipB.75jDrU3JY3g0DJDZ2kFzZDlpJ1Ive8Gdcr10TNVCj7NBd2oAg; cf_clearance=GJF7.5Ew66z8ziq0B6vCDSbyXEz6BBPQ9dDV1MlF6GY-1715437369-1.0.1.1-Tt7sA5de3OYDdNb_zrM7WwAp2JIxU5Mj8ZbK32q131luK6Zd3wEI8W53CVRq8DPKzpRlD11BczYw1.B1qaDWkQ; csrftoken=ZP9Y2tvTznQrFRRcYDQoVi1mNCfX8EhWpY26xh7IzCTuGY6AuM5DWb2hooXq9WMs; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWK5QWpxYZGJiZ5egpxepQpj0WAM6bKrE:1s5nci:Ete-JEJsh7T_4debpoffP4Xg9QGGR-EETLjhNpn1pPM; INGRESSCOOKIE=0e21ad87daa5b51017165e7271d8d519|8e0876c7c1464cc0ac96bc2edceabd27; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMjA2MDEwNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjRmNTk2MWRiODZkNWE1OTNlOGJjYTc3ODUwMDhkZGZjMzVhZjQxZTBmZWZkODFkMDZmZjYxYjY4NmEwZTZiY2UiLCJpZCI6MjA2MDEwNSwiZW1haWwiOiJzeWFtYW50YWsua3VtYXJAZ21haWwuY29tIiwidXNlcm5hbWUiOiJ1c2VyMDA2NmwiLCJ1c2VyX3NsdWciOiJ1c2VyMDA2NmwiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvdXNlcjAwNjZsL2F2YXRhcl8xNTYyMTc3MjM5LnBuZyIsInJlZnJlc2hlZF9hdCI6MTcxNTQzNzM3MSwiaXAiOiI2Mi4yMTguMjA2LjE5MCIsImlkZW50aXR5IjoiN2Y0Mzk1OGZjZDhiMDE0ODM3NGYxMGY4YTBjOTZmMjYiLCJzZXNzaW9uX2lkIjo2MTMwMzUzMCwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.zoL_XQXljFbIGp_CRXtcs9SZkWSjno1oXjosEoKyfJw; __cf_bm=lqV3hIdCfVgoZMI3SoRsp7aEBLQwknnP3bH9GEJvl8Y-1715517285-1.0.1.1-8h2nzuzk1.MnCPuWPdgtHEc6jsUBNBxD2SuSeO.scJ6WycUbRYsxGD9YiCUjGl9HMtf209z3gMW4EjNKMqvbew; _dd_s=rum=0&expire=1715518315388",
    # }
    # s = requests.Session()
    # s.headers.update(headers)
    # s.cookies.update(
    #     {
    #         "__stripe_mid": "c37fcc42-c814-40a8-8c3a-a0dcc13759295c1628",
    #         "cf_clearance": "cf_clearance=ulYeISH87dqHq.Ea5XK3z4K4jjb222squDdS1zgoGSE-1711990126-1.0.1.1-y6rf.ziQUywhDuRzXn5jxVYrwmqBvvic5ipB.75jDrU3JY3g0DJDZ2kFzZDlpJ1Ive8Gdcr10TNVCj7NBd2oAg",
    #         "csrftoken": "ZP9Y2tvTznQrFRRcYDQoVi1mNCfX8EhWpY26xh7IzCTuGY6AuM5DWb2hooXq9WMs",
    #     }
    # )
    # print(s.get("https://leetcode.com/contest/weekly-contest-357/"))

    # response = requests.get(
    #     "https://leetcode.com/contest/api/ranking/weekly-contest-357/?pagination=1",
    #     headers=headers,
    #     allow_redirects=False,
    # )
    # print(response)

    # print(
    #     requests.get(
    #         f"https://leetcode.com/contest/api/ranking/{contest_id}/?pagination={ranking_page}",
    #         headers=headers,
    #     )
    # )
    # # print(
    # #     requests.get(
    # #         f"https://leetcode.com/contest/api/ranking/{contest_id}/?pagination={ranking_page}",
    # #         headers=headers,
    # #     ).content
    # # )
    # res = requests.get(
    #     f"https://leetcode.com/contest/api/ranking/{contest_id}/?pagination={ranking_page}"
    # ).json()

    res = json.loads(subprocess_curl(contest_id, ranking_page))
    sleep(2)

    return ContestRanking(
        id=contest_ranking_id(contest_id, ranking_page),
        is_past=res["is_past"],
        submissions=[
            {
                ContestRankingQuestionId(k): ContestRankingSubmission(
                    **({"lang": None} | v),
                )
            }
            for submission in res["submissions"]
            for k, v in submission.items()
        ],
        questions=res["questions"],
        total_rank=res["total_rank"],
        user_num=res["user_num"],
    )


def main():
    contest_id = "weekly-contest-357"
    ranking_page = 1
    result = get_contest_ranking(contest_id, ranking_page)
    pprint(result)


if __name__ == "__main__":
    main()
