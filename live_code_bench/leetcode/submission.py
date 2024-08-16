import json
import subprocess
from time import sleep
from pprint import pprint

import requests
from pydantic.dataclasses import dataclass


@dataclass
class Submission:
    code: str
    lang: str
    contest_submission: int
    id: int
    question_id: int


@dataclass
class Submissions:
    submissions: list[Submission]
    contest_id: str
    question_id: int
    id: int

    def add_submission(self, submission: Submission):
        self.submissions.append(submission)

    @property
    def length(self):
        return len(self.submissions)

    @property
    def python3_length(self):
        return len([s for s in self.submissions if s.lang == "python3"])


def subprocess_curl(url):
    cmd = f"""curl '{url}' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: gr_user_id=32499272-87cd-499d-8267-d8be1522c7d7; 87b5a3c3f1a55520_gr_last_sent_cs1=naman1205jain; __stripe_mid=32c88075-ddd5-456f-82c0-d3ed11b7ea50afb849; __gpi=UID=00000a4051697fb9:T=1699249197:RT=1699249197:S=ALNI_MaZbbctApfY6GoaiQ-CgXdqiF5IHA; cf_clearance=.rVmOBJdtd1iM52JDXayS07UMSM4eYA7cV1XZyU8pao-1711989583-1.0.1.1-qtGcpUYbSv9RC9fnEaOwuy1bs4nElI3eEDFr.DBJ7_We_0MljkcTbt4ogr5VEOewHX2MndrP0qeC24i0XWt5RA; csrftoken=uDCJbpfYBluUPuAYjvTAmGnAETBasKij7gKIun0bx7CdAnNfLnBGwfz4pxqc56pQ; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWK-Ql5ibmGRoZmGYlZubpKcXq4DIiMr9UISOxLBWmPb-0BJ9yKtg4zB0dCwDOIJBl:1rrKhL:GcblLIP9DNzg_Y53IvVCqxRU_kSgMZ1H15sQZC14Bf8; __gads=ID=b71860d3dcf24813-22148070e7e700db:T=1699249197:RT=1711989599:S=ALNI_MavQ-6jP42HbKx3ruaDGB99WNgugw; __eoi=ID=37d80cca431bbefb:T=1711989599:RT=1711989599:S=AA-AfjYgGZ_vfC4QUwAWPZWrkJk4; FCNEC=%5B%5B%22AKsRol-KrleO1mgGUoh9t3OvAZYd7uebnjbrL24JliSM96c3Qtl_RYK3n6N5lgGosAVB7m7D7vOkSsI3msBV9mWzpzdjfyoaB084snRwDf456iNfk9DjAvMIlqpRcU0ApmQZw0dLHbmhdtN1TvO1iCs0jbEZ2ppgMA%3D%3D%22%5D%5D; _gid=GA1.2.983665159.1717270558; INGRESSCOOKIE=7d81156bedcdbcb5edfdff7756d94e1d|8e0876c7c1464cc0ac96bc2edceabd27; 87b5a3c3f1a55520_gr_session_id=9c44352b-35b1-430f-b23a-a16609c888da; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=9c44352b-35b1-430f-b23a-a16609c888da; 87b5a3c3f1a55520_gr_session_id_sent_vst=9c44352b-35b1-430f-b23a-a16609c888da; __stripe_sid=7cd40005-481c-481d-9d3f-614109263f849eb69c; _ga_CDRWKZTDEX=GS1.1.1717274047.39.1.1717274093.14.0.0; _ga=GA1.2.277596681.1697782084; 87b5a3c3f1a55520_gr_cs1=naman1205jain; _dd_s=rum=0&expire=1717275001173; __cf_bm=f5dB2UmeuLyAn_ffM1dm9cOCAh6rk3DdAJtXpxVykNY-1717274473-1.0.1.1-BXnqeJSmX819blu5qAtIamWtshcxffqpXOgkJ0aHjoy98DR4qVxXnzwl.unNYBhydj08UYif9XmclggdgUXrhg' \
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


def get_submission(submission_id, data_region, question_id):
    if data_region == "CN":
        url = f"https://leetcode.cn/api/submissions/{submission_id}/"
    else:
        url = f"https://leetcode.com/api/submissions/{submission_id}/"

    res = json.loads(subprocess_curl(url))
    sleep(2)

    # if res.status_code != 200:
    #     raise Exception(
    #         submission_id, question_id, res.reason, res.status_code, res.url
    #     )
    # res = res.json()
    # if res.status_code != 200:
    #     print(submission_id, res.reason, res.status_code, res.url)
    #     return get_submission(submission_id)

    # try:
    #     res = res.json()
    # except Exception as e:
    #     import traceback

    #     traceback.print_exc()
    #     print(res.__dict__)
    #     import pdb

    #     pdb.set_trace()

    return Submission(**res, question_id=question_id)


def main():
    submission_id = 1013393950
    result = get_submission(submission_id)
    pprint(result)


if __name__ == "__main__":
    main()
