def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    for value in ("25", "abc"):
        print(f"Input data is '{value}'")
        try:
            temperature = input_temperature(value)
            print(f"Temperature is now {temperature}°C")
        except (ValueError, TypeError) as error:
            print(f"Caught input_temperature error: {error}")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
