from pprint import pprint
from typing import List

import requests
from bs4 import BeautifulSoup, ResultSet
from pydantic.dataclasses import dataclass

from live_code_bench.utils.streamlit import StreamlitMixin


@dataclass(repr=False)
class ContestGeneral(StreamlitMixin):
    id: str

    # scraped
    name: str
    start_time: str
    duration: str
    rated_range: str

    badge_title: str

    # This is a badge on each contest but I don't know what exactly it means
    user_color: str


def get_contests_general(page: int):
    res = requests.get(
        f"https://atcoder.jp/contests/archive?page={page}",
    )
    res.raise_for_status()
    res_text = res.text

    soup = BeautifulSoup(res_text, "html.parser")

    # Find table
    table = soup.find("table")

    # Find rows
    rows = table.find_all("tr")

    # Header row
    header_row = rows[0]

    # Header row ths
    header_row_ths = header_row.find_all("th")

    # Header row ths texts
    header_row_ths_texts = [th.text.strip() for th in header_row_ths]

    # Check if they are correct
    assert header_row_ths_texts == [
        "Start Time (local time)",
        "Contest Name",
        "Duration",
        "Rated Range",
    ]

    # * Modify header_row_ths_texts
    header_row_ths_texts = [
        header_row_ths_texts[0],
        "_badge_title",
        "_user_color",
        "_id",
        header_row_ths_texts[1],
        header_row_ths_texts[2],
        header_row_ths_texts[3],
    ]

    # Data rows
    data_rows = rows[1:]

    # Data rows tds
    data_rows_tds: List[ResultSet] = [data_row.find_all("td") for data_row in data_rows]

    # Data rows tds texts
    def extract_one_row(data_row_tds) -> list:
        result = []

        for i, data_row_td in enumerate(data_row_tds):
            if i == 1:
                for span in data_row_td.find_all("span"):
                    # This is for badge title
                    if span.has_attr("title"):
                        result.append(span["title"])
                    # This is for user color
                    if span.has_attr("class"):
                        result.append(str(span["class"]))
                    # Remove for contest name
                    span.extract()

                # Get link
                a = data_row_td.find("a")
                # Get id
                result.append(a["href"].split("/")[-1])

                # Contest name
                text = data_row_td.text.strip()
                result.append(text)

            else:
                text = data_row_td.text.strip()
                result.append(text)

        return result

    data_rows_tds_texts = [
        extract_one_row(data_row_tds) for data_row_tds in data_rows_tds
    ]

    # Create list of dicts
    contests_general_dicts = [
        dict(zip(header_row_ths_texts, data_row_tds_texts))
        for data_row_tds_texts in data_rows_tds_texts
    ]

    # Create list of ContestGeneral
    contests_general = [
        ContestGeneral(
            id=contest_general_dict["_id"],
            name=contest_general_dict["Contest Name"],
            start_time=contest_general_dict["Start Time (local time)"],
            duration=contest_general_dict["Duration"],
            rated_range=contest_general_dict["Rated Range"],
            badge_title=contest_general_dict["_badge_title"],
            user_color=contest_general_dict["_user_color"],
        )
        for contest_general_dict in contests_general_dicts
    ]

    return contests_general


def main():
    page = 1
    results = get_contests_general(page)

    # Print
    pprint(results[0])


if __name__ == "__main__":
    main()
