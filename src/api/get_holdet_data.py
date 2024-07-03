import requests
import pandas as pd

from typing import List


def get_holdet_data(i: str) -> List:
    req = requests.get(
        f"https://www.holdet.dk/handlers/tradedata.ashx?language=da&game=tour-de-france-2024&userteam=&partial-name=&positions=&team=&formation=cycling_trading_8_riders&minimum-value=0&maximum-value=0&lineup=&original-lineup=&sort=value&addable-only=false&direction=-1&page={i}&include-headers=false&include-formations=false&include-lineup=false&include-fields=false&r=1719514946777"
    )
    req = req.json()
    values = [[i["Values"][2], i["Values"][16]] for i in req["Dataset"]["Items"]]
    return values


def fetch_holdet_data(stage_number: int):
    responses = []
    for i in range(0, 8):
        responses.extend(get_holdet_data(i))
    df = pd.DataFrame(responses, columns=["name", "price"])
    df.to_csv(f"data/{stage_number}_holdet_data.csv")
    return


if __name__ == "__main__":
    responses = []
    for i in range(0, 8):
        responses.extend(get_holdet_data(i))
    df = pd.DataFrame(responses, columns=["name", "price"])
    df.to_csv("data/2_holdet_data.csv")
