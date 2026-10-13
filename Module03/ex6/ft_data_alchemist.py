import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    players = ["Alice", "bob", "Charlie", "dylan", "Emma", "Gregory",
               "john", "kevin", "Liam"]
    capitalized = [name.capitalize() for name in players]
    initial_capitals = [name for name in players if name == name.capitalize()]
    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {capitalized}")
    print(f"New list of capitalized names only: {initial_capitals}")
    scores = {name: random.randint(0, 1000) for name in capitalized}
    average = sum(scores.values()) / len(scores)
    high_scores = {name: score for name, score in scores.items()
                   if score > average}
    print(f"Score dict: {scores}")
    print(f"Score average is {round(average, 2)}")
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
