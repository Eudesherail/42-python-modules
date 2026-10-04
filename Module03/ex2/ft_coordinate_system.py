import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        text = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            first, second, third = text.split(",")
        except ValueError:
            print("Invalid syntax")
            continue
        values: list[float] = []
        for parameter in (first, second, third):
            try:
                value = float(parameter)
                if value != value or value in (float("inf"), -float("inf")):
                    raise ValueError("coordinate must be finite")
                values.append(value)
            except ValueError as error:
                print(f"Error on parameter '{parameter}': {error}")
                break
        else:
            return values[0], values[1], values[2]


def distance(first: tuple[float, float, float],
             second: tuple[float, float, float]) -> float:
    x1, y1, z1 = first
    x2, y2, z2 = second
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def main() -> None:
    print("=== Game Coordinate System ===")
    try:
        print("Get a first set of coordinates")
        first = get_player_pos()
        print(f"Got a first tuple: {first}")
        x, y, z = first
        print(f"It includes: X={x}, Y={y}, Z={z}")
        print(f"Distance to center: {round(distance(first, (0, 0, 0)), 4)}")
        print("Get a second set of coordinates")
        second = get_player_pos()
        print("Distance between the 2 sets of coordinates: "
              f"{round(distance(first, second), 4)}")
    except (EOFError, KeyboardInterrupt):
        print("Coordinate input ended.")
    except OverflowError:
        print("Distance is outside floating-point range.")


if __name__ == "__main__":
    main()
