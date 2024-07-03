from typing import List

STAGEPLACEMENT = {
    1: 200000,
    2: 150000,
    3: 130000,
    4: 120000,
    5: 110000,
    6: 100000,
    7: 95000,
    8: 90000,
    9: 85000,
    10: 80000,
    11: 70000,
    12: 55000,
    13: 40000,
    14: 30000,
    15: 15000,
}

GC_PLACEMENT = {
    1: 100000,
    2: 90000,
    3: 80000,
    4: 70000,
    5: 60000,
    6: 50000,
    7: 40000,
    8: 30000,
    9: 20000,
    10: 10000,
}

TEAM_BONUS = {1: 60000, 2: 30000, 3: 2000}

STAGE_BONUS = {
    8: 400000,
    7: 220000,
    6: 120000,
    5: 65000,
    4: 35000,
    3: 15000,
    2: 8000,
    1: 4000,
}

JERSEY_BONUS = {
    "yellow": 25000,
    "green": 25000,
    "polka": 25000,
    "white": 15000,
    "combative": 50000,
}


class Rules:
    @staticmethod
    def stage_placement_eval(stage_placement: int) -> int:
        return STAGEPLACEMENT.get(stage_placement, 0)

    @staticmethod
    def gc_placement_eval(gc_placement: int) -> int:
        return GC_PLACEMENT.get(gc_placement, 0)

    @staticmethod
    def team_placement_eval(team_placement: int) -> int:
        return TEAM_BONUS.get(team_placement, 0)

    @staticmethod
    def stage_eval(stage_placement: int) -> int:
        return STAGE_BONUS.get(stage_placement, 0)

    @staticmethod
    def late_arriaval_eval(late_arrival: int) -> int:
        if late_arrival is None:
            # No arrival time -> rider out of the tour
            return -100000
        return max(-90000, -3000 * late_arrival)

    @staticmethod
    def points_eval(points: List[int]) -> int:
        return sum([3000 * point for point in points])

    @staticmethod
    def jersey_eval(jersey: str) -> int:
        return JERSEY_BONUS.get(jersey, 0)

    @staticmethod
    def captain_bonus_eval(value_increase):
        return 1 * value_increase


if __name__ == "__main__":
    model = Rules()
    print(model.points_eval([10, 15]))

    print(model.stage_placement_eval(1))
    print(model.stage_placement_eval(5324))

    print(model.jersey_eval(None))
    print(model.jersey_eval("green"))
