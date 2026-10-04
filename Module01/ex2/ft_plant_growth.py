class Plant:
    """A plant's shared identity and measurements."""

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age_days = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age_days} days old")

    def grow(self, amount: float = 0.8) -> None:
        self.height = round(self.height + amount, 2)

    def age(self, days: int = 1) -> None:
        self.age_days += days


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    rose = Plant("Rose", 25.0, 30)
    initial_height = rose.height
    rose.show()
    for day in range(1, 8):
        rose.grow()
        rose.age()
        print(f"=== Day {day} ===")
        rose.show()
    print(f"Growth this week: {round(rose.height - initial_height, 2)}cm")
