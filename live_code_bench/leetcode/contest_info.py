import json
import subprocess
from time import sleep
from pprint import pprint
from typing import List, Optional

import requests
from pydantic.dataclasses import dataclass

from live_code_bench.utils.streamlit import StreamlitMixin


@dataclass
class Question:
    id: int
    question_id: int
    credit: int
    title: str
    title_slug: str


@dataclass
class Company:
    name: str
    description: str
    logo: Optional[str]


@dataclass
class Contest:
    id: int
    title: str
    title_slug: str
    description: str
    duration: int
    start_time: int
    is_virtual: bool
    origin_start_time: int
    is_private: bool
    discuss_topic_id: Optional[int]


@dataclass(repr=False)
class ContestInfo(StreamlitMixin):
    id: str
    contest: Contest
    questions: List[Question]
    company: Company
    containsPremium: bool
    registered: bool
    survey: Optional[str]  # Setting it to Optional because it could be None
    current_timestamp: float


def subprocess_curl(contest_id):
    cmd = f"""curl 'https://leetcode.com/contest/api/info/{contest_id}/' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: gr_user_id=32499272-87cd-499d-8267-d8be1522c7d7; 87b5a3c3f1a55520_gr_last_sent_cs1=naman1205jain; __stripe_mid=32c88075-ddd5-456f-82c0-d3ed11b7ea50afb849; __gpi=UID=00000a4051697fb9:T=1699249197:RT=1699249197:S=ALNI_MaZbbctApfY6GoaiQ-CgXdqiF5IHA; cf_clearance=.rVmOBJdtd1iM52JDXayS07UMSM4eYA7cV1XZyU8pao-1711989583-1.0.1.1-qtGcpUYbSv9RC9fnEaOwuy1bs4nElI3eEDFr.DBJ7_We_0MljkcTbt4ogr5VEOewHX2MndrP0qeC24i0XWt5RA; csrftoken=uDCJbpfYBluUPuAYjvTAmGnAETBasKij7gKIun0bx7CdAnNfLnBGwfz4pxqc56pQ; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWK-Ql5ibmGRoZmGYlZubpKcXq4DIiMr9UISOxLBWmPb-0BJ9yKtg4zB0dCwDOIJBl:1rrKhL:GcblLIP9DNzg_Y53IvVCqxRU_kSgMZ1H15sQZC14Bf8; __gads=ID=b71860d3dcf24813-22148070e7e700db:T=1699249197:RT=1711989599:S=ALNI_MavQ-6jP42HbKx3ruaDGB99WNgugw; __eoi=ID=37d80cca431bbefb:T=1711989599:RT=1711989599:S=AA-AfjYgGZ_vfC4QUwAWPZWrkJk4; FCNEC=%5B%5B%22AKsRol-KrleO1mgGUoh9t3OvAZYd7uebnjbrL24JliSM96c3Qtl_RYK3n6N5lgGosAVB7m7D7vOkSsI3msBV9mWzpzdjfyoaB084snRwDf456iNfk9DjAvMIlqpRcU0ApmQZw0dLHbmhdtN1TvO1iCs0jbEZ2ppgMA%3D%3D%22%5D%5D; _gid=GA1.2.983665159.1717270558; INGRESSCOOKIE=7d81156bedcdbcb5edfdff7756d94e1d|8e0876c7c1464cc0ac96bc2edceabd27; 87b5a3c3f1a55520_gr_session_id=9c44352b-35b1-430f-b23a-a16609c888da; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=9c44352b-35b1-430f-b23a-a16609c888da; 87b5a3c3f1a55520_gr_session_id_sent_vst=9c44352b-35b1-430f-b23a-a16609c888da; __cf_bm=o5smEl9uSy2Mw.kn4Y1PnEMFlQK.1z3w_rcS..2T1AI-1717274049-1.0.1.1-cifTQSXT6OyjtH97CSQPnhyQ0HGfqSNOEKALkWCQOhIsbk4fj1zONLDtyAerpk0zjAi1LAol20XF367hn8P5tw; __stripe_sid=7cd40005-481c-481d-9d3f-614109263f849eb69c; _ga_CDRWKZTDEX=GS1.1.1717274047.39.1.1717274093.14.0.0; _ga=GA1.2.277596681.1697782084; 87b5a3c3f1a55520_gr_cs1=naman1205jain; _dd_s=rum=0&expire=1717275001173' \
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


def get_contest_info(contest_id: str):
    # User-Agenbt
    # res = requests.get(
    #     f"https://leetcode.com/contest/api/info/{contest_id}",
    #     headers={
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    #     },
    # )

    # res.raise_for_status()
    # res_json = res.json()
    res_json = json.loads(subprocess_curl(contest_id))

    contest = res_json["contest"]
    questions = res_json["questions"]
    company = res_json["company"]

    return ContestInfo(
        id=contest_id,
        **{
            **res_json,
            **{
                "contest": Contest(**contest),
                "questions": [Question(**question) for question in questions],
                "company": Company(**company),
            },
        },
    )


def main():
    contest_id = "weekly-contest-261"
    result = get_contest_info(contest_id)

    pprint(result)


if __name__ == "__main__":
    main()
