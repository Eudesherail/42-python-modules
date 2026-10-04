import random


ACHIEVEMENTS = [
    "Crafting Genius", "World Savior", "Master Explorer", "Collector Supreme",
    "Untouchable", "Boss Slayer", "Strategist", "Unstoppable", "Speed Runner",
    "Survivor", "Treasure Hunter", "First Steps", "Sharp Mind",
    "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    count = random.randint(5, 9)
    return set(random.sample(ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===")
    players = ["Alice", "Bob", "Charlie", "Dylan"]
    achievements: list[set[str]] = []
    for player in players:
        earned = gen_player_achievements()
        achievements.append(earned)
        print(f"Player {player}: {earned}")
    distinct: set[str] = set()
    common = set(ACHIEVEMENTS)
    for earned in achievements:
        distinct = distinct.union(earned)
        common = common.intersection(earned)
    print(f"All distinct achievements: {distinct}")
    print(f"Common achievements: {common}")
    index = 0
    for player in players:
        others: set[str] = set()
        other_index = 0
        for earned in achievements:
            if index != other_index:
                others = others.union(earned)
            other_index += 1
        print(f"Only {player} has: {achievements[index].difference(others)}")
        index += 1
    index = 0
    for player in players:
        missing = set(ACHIEVEMENTS).difference(achievements[index])
        print(f"{player} is missing: {missing}")
        index += 1


if __name__ == "__main__":
    main()
