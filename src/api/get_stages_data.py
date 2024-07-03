from procyclingstats import Stage
import pandas as pd


def fetch_stages(i: str):
    stage = Stage(f"race/tour-de-france/2024/stage-{i}")
    return {
        "stage": f"stage-{i}",
        "distance": stage.distance(),
        "vertical": stage.vertical_meters(),
        "nr_of_climbs": len(stage.climbs()),
        "profile_score": stage.profile_score(),
        "profile_icon": stage.profile_icon(),
        "stage_type": stage.stage_type(),
    }


def fetch_stages_data():
    stages = []
    for i in range(1, 22):
        stages.append(fetch_stages(i))

    df = pd.DataFrame.from_records(stages)
    df.to_csv("data/pcs_stages_data.csv")
    return


if __name__ == "__main__":
    stages = []
    for i in range(1, 22):
        stages.append(fetch_stages(i))

    df = pd.DataFrame.from_records(stages)
    df.to_csv("pcs_stages_data.csv")
