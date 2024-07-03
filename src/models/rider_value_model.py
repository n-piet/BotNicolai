from typing import List

from rules.rules import Rules

rules = Rules()


class RiderValueUpdate:
    def __init__(
        self,
        stage_placement,
        gc_placement,
        team_bonus,
        stage_bonus,
        points,
        jerseys,
        late_arrival,
        captain,
    ) -> None:

        self.stage_placement = stage_placement
        self.gc_placement = gc_placement
        self.team_bonus: int = team_bonus
        # self.stage_bonus = stage_bonus
        # stage_bonus should only be evaluated once pr selected team
        self.captain: bool = captain
        self.points: List[int] = points
        self.jerseys: List[str] = jerseys
        self.late_arrival = late_arrival
        self.value_change = 0

    def eval(self):

        self.value_change += rules.stage_placement_eval(self.stage_placement)
        self.value_change += rules.gc_placement_eval(self.gc_placement)
        self.value_change += rules.team_placement_eval(self.team_bonus)
        self.value_change += rules.points_eval(self.points)
        self.value_change += sum([rules.jersey_eval(jersey) for jersey in self.jerseys])
        self.value_change += rules.late_arriaval_eval(self.late_arrival)
        self.value_change += (
            rules.captain_bonus_eval(self.value_change) if self.captain else 0
        )


if __name__ == "__main__":
    riderupdate = RiderValueUpdate(
        stage_placement=1,
        gc_placement=1,
        team_bonus=1,
        stage_bonus=8,
        captain=True,
        points=[10, 10],
        jerseys=["green", "yellow"],
        late_arrival=0,
    )
    riderupdate.eval()
