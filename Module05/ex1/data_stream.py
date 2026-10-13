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


class DataStream:
    """Route through the first accepting registered processor."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self._processors:
            self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for processor in self._processors:
                try:
                    if not processor.validate(element):
                        continue
                    processor.ingest(element)
                except Exception as error:
                    print(f"DataStream processor error: {error}")
                break
            else:
                print("DataStream error - Can't process element in stream: "
                      f"{element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        for processor in self._processors:
            total, remaining = processor.statistics()
            name = type(processor).__name__.replace("Processor", " Processor")
            print(f"{name}: total {total} items processed, "
                  f"remaining {remaining} on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    print("Registering Numeric Processor")
    stream.register_processor(numeric)
    batch: list[Any] = [
        "Hello world", [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO", "log_message": "User wil is connected"}],
        42, ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print("Registering other data processors")
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print("Consume some elements: Numeric 3, Text 2, Log 1")
    for _ in range(3):
        numeric.output()
    for _ in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
