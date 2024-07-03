import pandas as pd
import re
import ast

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from typing import List

current_year = datetime.now().year

STAGE_PROFILE_WEIGHTING = {
    # p1: Flat
    # p2: Hills, flat finish
    # p3: Hills, uphill finish
    # p4: Mountains, flat finish
    # p5: Mountains, uphill finish
    "p1": {
        "one_day_races": 0.2,
        "gc": 0.0,
        "time_trial": 0.0,
        "sprint": 0.8,
        "climber": 0.0,
    },
    "p2": {
        "one_day_races": 0.3,
        "gc": 0.1,
        "time_trial": 0.2,
        "sprint": 0.4,
        "climber": 0.0,
    },
    "p3": {
        "one_day_races": 0.4,
        "gc": 0.3,
        "time_trial": 0.1,
        "sprint": 0.1,
        "climber": 0.1,
    },
    "p4": {
        "one_day_races": 0.0,
        "gc": 0.5,
        "time_trial": 0.0,
        "sprint": 0.0,
        "climber": 0.5,
    },
    "p5": {
        "one_day_races": 0.0,
        "gc": 0.7,
        "time_trial": 0.0,
        "sprint": 0.0,
        "climber": 0.3,
    },
}
STAGE_WEIGHTING = {1: 0.7, 2: 0.3, 3: 0.001}
POINT_PR_YEAR_WEIGHTING = {
    current_year: 1.0,
    current_year - 1: 0.7,
    current_year - 2: 0.4,
    current_year - 3: 0.1,
}


def standardize_name(name):
    name = name.strip().lower()
    name = re.sub(r"[áàâä]", "a", name)
    name = re.sub(r"[éèêë]", "e", name)
    name = re.sub(r"[íìîï]", "i", name)
    name = re.sub(r"[óòôö]", "o", name)
    name = re.sub(r"[úùûü]", "u", name)
    name = re.sub(r"[çč]", "c", name)
    name = re.sub(r"[ñņ]", "n", name)
    name = re.sub(r"[š]", "s", name)
    name = re.sub(r"[-]", "", name)
    name = re.sub(r"  ", " ", name)
    return name


def combine_rider_data(stage_number):
    holdet_data = pd.read_csv(f"data/{stage_number}_holdet_data.csv", index_col=0)
    pcs_rider_data = pd.read_csv("data/pcs_rider_data.csv", index_col=0)

    holdet_data["name"] = holdet_data["name"].apply(standardize_name)
    pcs_rider_data["name"] = pcs_rider_data["name"].apply(standardize_name)
    combined_data = pd.merge(holdet_data, pcs_rider_data, on="name", how="inner")
    combined_data.rename(
        columns={
            "points_per_speciality.one_day_races": "one_day_races",
            "points_per_speciality.gc": "gc",
            "points_per_speciality.time_trial": "time_trial",
            "points_per_speciality.sprint": "sprint",
            "points_per_speciality.climber": "climber",
        },
        inplace=True,
    )
    combined_data.to_csv("data/combined_rider_data.csv", index=False)
    return combined_data


def normalize_rider_points(df: pd.DataFrame):

    for col in [
        "one_day_races",
        "gc",
        "time_trial",
        "sprint",
        "climber",
    ]:
        # df[col] = df[col].apply(lambda x: (x - df[col].mean()) / df[col].std())
        scaler = MinMaxScaler()
        scaler.fit(df[col].values.reshape(-1, 1))
        df[col] = scaler.transform(df[col].values.reshape(-1, 1))
        df[col] = df[col] * df["age"].apply(age_adjustment)
    return df


def calculate_weighted_points(points_per_season_history, weighting_factor):
    points_per_season_history = ast.literal_eval(points_per_season_history)
    w_p = 0
    for season_data in points_per_season_history:
        season = season_data["season"]
        points = season_data["points"]
        weight = weighting_factor.get(season, 0)
        w_p += points * weight
    return w_p


def calculate_age(dateofbirth: str):
    dateofbirth = datetime.strptime(dateofbirth, "%Y-%m-%d")
    today = datetime.today()
    age = (
        today.year
        - dateofbirth.year
        - ((today.month, today.day) < (dateofbirth.month, dateofbirth.day))
    )
    return age


def age_adjustment(age):
    return 1.0 - 0.1 * (age - 25)


def apply_stage_weighting(
    stages_df: pd.DataFrame,
    rider_df: pd.DataFrame,
    stage_number,
    forward_looking_stages=3,
):
    stages_df = stages_df.iloc[(stage_number - 1) :, :].reset_index(drop=True)
    accumelated_points_lst = []
    for _, rider in rider_df.iterrows():
        accumelated_points = 0
        for idx, stage in stages_df.iterrows():
            if idx + 1 > forward_looking_stages:
                break
            profile = stage["profile_icon"]
            s_w = STAGE_WEIGHTING[idx + 1]
            s_p_w = STAGE_PROFILE_WEIGHTING[profile]
            accumelated_points += sum(rider[col] * s_p_w[col] for col in s_p_w) * s_w
        accumelated_points_lst.append(accumelated_points)

    return accumelated_points_lst


def data_preprocessing(stage_number: int, currently_selected_riders: List):
    df = combine_rider_data(stage_number)
    df["age"] = df["birthdate"].apply(calculate_age)
    df["w_p"] = df["points_per_season_history"].apply(
        calculate_weighted_points, args=(POINT_PR_YEAR_WEIGHTING,)
    )
    df = normalize_rider_points(df)

    df_stages = pd.read_csv("data/pcs_stages_data.csv", index_col=0)
    df["predicted_accumlated_points"] = apply_stage_weighting(
        df_stages, df, stage_number=stage_number
    )
    df["currently_selected_riders"] = df["name"].apply(
        lambda x: 0 if x in currently_selected_riders else 1
    )
    assert sum(df["currently_selected_riders"]) == df.shape[0] - 8

    df.to_csv(
        "data/opti_rider_data.csv",
        columns=[
            "name",
            "price",
            "predicted_accumlated_points",
            "currently_selected_riders",
        ],
    )
    return


if __name__ == "__main__":
    stage_number = 2
    combine_rider_data(stage_number)
    df = pd.read_csv("data/combined_rider_data.csv")
    df["age"] = df["birthdate"].apply(calculate_age)
    df["w_p"] = df["points_per_season_history"].apply(
        calculate_weighted_points, args=(POINT_PR_YEAR_WEIGHTING,)
    )
    df = normalize_rider_points(df)

    stages = pd.read_csv("data/pcs_stages_data.csv", index_col=0)
    df["predicted_accumlated_points"] = apply_stage_weighting(
        stages, df, stage_number=stage_number
    )
    df.to_csv(
        "data/opti_rider_data.csv",
        columns=["name", "price", "predicted_accumlated_points"],
    )
