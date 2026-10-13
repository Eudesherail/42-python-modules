from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """A FIFO queue with stable, zero-based extraction ranks."""

    def __init__(self) -> None:
        self._queue: list[str] = []
        self._rank = 0
        self._total = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Return whether the complete input can be ingested."""
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Validate before changing stored data."""
        ...

    def _store(self, items: list[str]) -> None:
        self._queue.extend(items)
        self._total += len(items)

    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise IndexError("No processed data available")
        result = self._rank, self._queue.pop(0)
        self._rank += 1
        return result

    def statistics(self) -> tuple[int, int]:
        return self._total, len(self._queue)


class NumericProcessor(DataProcessor):
    """Accept numbers and homogeneous or mixed numeric lists."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if type(item) not in (int, float):
                    return False
            return True
        return type(data) in (int, float)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        values = data if isinstance(data, list) else [data]
        self._store([str(value) for value in values])


class TextProcessor(DataProcessor):
    """Accept strings and lists of strings, preserving each item."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
            return True
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            self._store(data)
        else:
            self._store([data])


class LogProcessor(DataProcessor):
    """Accept arbitrary string dictionaries, including standard log entries."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        for entry in entries:
            if not isinstance(entry, dict):
                return False
            for key, value in entry.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False
        return True

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        values = data if isinstance(data, list) else [data]
        rendered: list[str] = []
        for value in values:
            if set(value) == {"log_level", "log_message"}:
                rendered.append(
                    f"{value['log_level']}: {value['log_message']}")
            else:
                rendered.append("; ".join(
                    f"{key}: {message}" for key, message in value.items()))
        self._store(rendered)


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    numeric = NumericProcessor()
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        # Deliberate wrong argument required by the subject: keep mypy warning.
        numeric.ingest("foo")
    except ValueError as error:
        print(f"Got exception: {error}")
    print("Processing data: [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")
    text = TextProcessor()
    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {text.validate(42)}")
    print(f"Trying to validate input 'Hello': {text.validate('Hello')}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(["Hello", "Nexus", "World"])
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")
    log = LogProcessor()
    print("Testing Log Processor...")
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    records = [{"log_level": "NOTICE", "log_message": "Connection to server"},
               {"log_level": "ERROR", "log_message": "Unauthorized access!!"}]
    print(f"Trying to validate log records: {log.validate(records)}")
    print(f"Processing data: {records}")
    log.ingest(records)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
