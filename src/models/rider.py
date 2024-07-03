from enum import Enum
from procyclingstats import Rider as Rider_pcs


class RiderProfile(Enum):
    CLIIMBER = 1
    SPRINTER = 2
    ROULEUR = 3
    PUNCHEUR = 4
    DOMESTIQUE = 5


class Rider:
    def __init__(self, name, team, captain, weight, rider_profile, value):
        self.name: str = name
        self.team: str = team
        self.captain: bool = captain
        self.weight: float = weight
        self.rider_profile: RiderProfile = RiderProfile(rider_profile)
        self.value: int = value


if __name__ == "__main__":
    tmp = Rider(
        name="Tadej",
        team="UAE",
        captain=True,
        weight=155.0,
        rider_profile=1,
        value=14000000,
    )
    print(tmp.__dict__)

    rider = Rider_pcs("rider/tadej-pogacar")
    print(rider.birthdate())

    print(rider.parse(), sep="\n")
