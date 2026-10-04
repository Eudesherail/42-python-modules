class Plant:
    """A plant's shared identity and measurements."""

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age_days = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age_days} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    for plant in (Plant("Rose", 25, 30), Plant("Sunflower", 80, 45),
                  Plant("Cactus", 15, 120)):
        plant.show()
