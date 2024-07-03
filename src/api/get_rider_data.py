import pandas as pd

from procyclingstats import Rider, RaceStartlist
from typing import List


def fetch_rider_data(riders: List[str]):
    riders_lst = []
    for rider in riders:
        try:
            obj = Rider(f"{rider}")
            obj_dict = obj.parse()
            riders_lst.append(obj_dict)
        except Exception:
            print(rider)
            continue
    return riders_lst


def fetch_riders():
    # Robbe Ghys
    race_startlist = RaceStartlist("race/tour-de-france/2024/startlist").startlist()
    riders = []
    for rider in race_startlist:
        riders.append(rider["rider_url"])
    return riders


def fetch_pcs_rider_data(data_path="data/pcs_rider_data.csv"):
    riders = fetch_riders()
    rider_data = fetch_rider_data(riders)
    df = pd.json_normalize(rider_data)
    df.drop(
        ["teams_history", "image_url"],
        inplace=True,
        axis=1,
    )
    df.to_csv(data_path)
    return


if __name__ == "__main__":
    riders = fetch_riders()
    rider_data = fetch_rider_data(riders)
    rider_data = pd.json_normalize(rider_data)
    rider_data.drop(
        ["teams_history", "image_url"],
        inplace=True,
        axis=1,
    )
    rider_data.to_csv("data/pcs_rider_data.csv")
