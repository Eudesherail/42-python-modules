class GardenError(Exception):
    """Base error with a default message without extra authorized builtins."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        self.args = (message,)


class PlantError(GardenError):
    """A problem specific to a plant."""

    def __init__(self, message: str = "Unknown plant error") -> None:
        self.args = (message,)


def water_plant(plant_name: str) -> None:
    if not plant_name or plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(
    plants: tuple[str, ...] = ("Tomato", "Lettuce", "Carrots"),
) -> None:
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    print("Testing valid plants...")
    test_watering_system()
    print("Testing invalid plants...")
    test_watering_system(("Tomato", "lettuce", "Carrots"))
    print("Cleanup always happens, even with errors!")
