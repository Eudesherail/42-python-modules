class GardenError(Exception):
    """A general garden problem."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        Exception.__init__(self, message)


class PlantError(GardenError):
    """A problem specific to a plant."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        GardenError.__init__(self, message)


class WaterError(GardenError):
    """A problem specific to watering."""

    def __init__(self, message: str = "Unknown water error") -> None:
        GardenError.__init__(self, message)


def check_plant(wilting: bool) -> None:
    if wilting:
        raise PlantError("The tomato plant is wilting!")


def check_water(available: int) -> None:
    if available <= 0:
        raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")
    print("Testing PlantError...")
    try:
        check_plant(True)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
    print("Testing WaterError...")
    try:
        check_water(0)
    except WaterError as error:
        print(f"Caught WaterError: {error}")
    print("Testing catching all garden errors...")
    for plant_problem in (True, False):
        try:
            if plant_problem:
                check_plant(True)
            else:
                check_water(0)
        except GardenError as error:
            print(f"Caught GardenError: {error}")
    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
