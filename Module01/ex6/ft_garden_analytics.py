class Plant:
    """Keep measurements protected and validate every supported update."""

    class Statistics:
        """Per-instance counters, accessed through methods only."""

        def __init__(self) -> None:
            self._grow = 0
            self._age = 0
            self._show = 0
            self._shade = 0

        def record_grow(self) -> None:
            self._grow += 1

        def record_age(self) -> None:
            self._age += 1

        def record_show(self) -> None:
            self._show += 1

        def record_shade(self) -> None:
            self._shade += 1

        def show(self, tree: bool = False) -> None:
            print(f"Stats: {self._grow} grow, {self._age} age, "
                  f"{self._show} show")
            if tree:
                print(f"{self._shade} shade")

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        return age > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    def show_statistics(self) -> None:
        self._statistics.show()

    def __init__(self, name: str, height: float, age: int) -> None:
        self._statistics = self.Statistics()
        self.name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            return
        self._height = height

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
            return
        self._age = age

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def grow(self, amount: float = 0.8) -> None:
        self._statistics.record_grow()
        self.set_height(round(self._height + amount, 2))

    def age(self, days: int = 1) -> None:
        self._statistics.record_age()
        self.set_age(self._age + days)

    def show(self) -> None:
        self._statistics.record_show()
        print(f"{self.name}: {self._height:.1f}cm, {self._age} days old")


class Flower(Plant):
    """A plant with a color and a persistent blooming state."""

    def __init__(self, name: str, height: float, age: int,
                 color: str) -> None:
        super().__init__(name, height, age)
        self.color = color
        self._bloomed = False

    def bloom(self) -> None:
        self._bloomed = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self._bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    """A plant whose trunk and height describe its shade."""

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def show_statistics(self) -> None:
        self._statistics.show(tree=True)

    def produce_shade(self) -> None:
        self._statistics.record_shade()
        print(f"Tree {self.name} now produces a shade of "
              f"{self.get_height():.1f}cm long and "
              f"{self.trunk_diameter:.1f}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter:.1f}cm")


class Vegetable(Plant):
    """A plant whose growth and aging each improve nutritional value."""

    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str) -> None:
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = 0.0

    def grow(self, amount: float = 2.1) -> None:
        before = self.get_height()
        super().grow(amount)
        if self.get_height() > before:
            self.nutritional_value += 0.5

    def age(self, days: int = 1) -> None:
        before = self.get_age()
        super().age(days)
        if self.get_age() > before:
            self.nutritional_value += 0.5 * days

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {self.nutritional_value:g}")


class Seed(Flower):
    """A flower that produces seeds when it blooms."""

    def __init__(self, name: str, height: float, age: int,
                 color: str) -> None:
        super().__init__(name, height, age, color)
        self._seeds = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._seeds}")


def display_statistics(plant: Plant) -> None:
    print(f"[statistics for {plant.name}]")
    plant.show_statistics()


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    for days in (30, 400):
        print(f"Is {days} days more than a year? -> "
              f"{Plant.is_older_than_year(days)}")
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_statistics(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow(8)
    rose.bloom()
    rose.show()
    display_statistics(rose)
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_statistics(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_statistics(oak)
    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30)
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    display_statistics(sunflower)
    print("=== Anonymous")
    anonymous = Plant.anonymous()
    anonymous.show()
    display_statistics(anonymous)
