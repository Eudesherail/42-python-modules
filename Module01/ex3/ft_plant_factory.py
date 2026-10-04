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
    print("=== Plant Factory Output ===")
    for plant in (Plant("Rose", 25.0, 30), Plant("Oak", 200.0, 365),
                  Plant("Cactus", 5.0, 90), Plant("Sunflower", 80.0, 45),
                  Plant("Fern", 15.0, 120)):
        print("Created: ", end="")
        plant.show()
