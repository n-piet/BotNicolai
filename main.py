import argparse

from src.api.get_rider_data import fetch_pcs_rider_data
from src.api.get_holdet_data import fetch_holdet_data
from src.api.get_stages_data import fetch_stages_data
from src.data.data_preprocessing import data_preprocessing
from src.optimizer.optimizer import select_riders
from src.helpers.misc import check_if_file_exists

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Optimize rider selection within a budget."
    )
    parser.add_argument("stage_number", type=int, help="Current TdF stage.", default=1)
    parser.add_argument(
        "budget", type=float, help="Budget for selecting riders.", default=50_000_000
    )
    currently_selected_riders = [
        "Bram Welten",
        "Piet Allegaert",
        "Dylan Groenewegen",
        "Danny Van Poppel",
        "Mike Teunissen",
        "Fabio Jakobsen",
        "Jasper Philipsen",
        "Arnaud Demare",
    ]
    currently_selected_riders = [x.lower() for x in currently_selected_riders]

    args = parser.parse_args()
    check_if_file_exists("data/pcs_rider_data.csv", fetch_pcs_rider_data)
    check_if_file_exists(
        f"data/{args.stage_number}_holdet_data.csv",
        fetch_holdet_data,
        args.stage_number,
    )
    check_if_file_exists("data/pcs_stages_data.csv", fetch_stages_data)
    data_preprocessing(args.stage_number, currently_selected_riders)
    select_riders(args.budget)
