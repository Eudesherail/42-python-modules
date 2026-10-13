from abc import ABC, abstractmethod
from typing import Any, Protocol


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

    def restore_output(self, batch: list[tuple[int, str]]) -> None:
        """Return the most recently removed batch after an export failure."""
        if batch:
            self._queue[0:0] = [value for _, value in batch]
            self._rank = batch[0][0]

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


class ExportPlugin(Protocol):
    """Structural interface; plugins need not inherit from this class."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        if nb < 0:
            print("DataStream error - output count cannot be negative")
            return
        for processor in self._processors:
            batch: list[tuple[int, str]] = []
            total, remaining = processor.statistics()
            try:
                for _ in range(min(nb, remaining)):
                    batch.append(processor.output())
                if batch:
                    plugin.process_output(batch)
            except Exception as error:
                # Failed exports remain available for a later retry.
                processor.restore_output(batch)
                print(f"DataStream export error: {error}")


class CSVExportPlugin:
    """Write a CSV row, quoting empty fields and special characters."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields: list[str] = []
        for _, value in data:
            if (value == "" or "," in value or '"' in value
                    or "\r" in value or "\n" in value):
                value = '"' + value.replace('"', '""') + '"'
            fields.append(value)
        print("CSV Output:")
        print(",".join(fields))


class JSONExportPlugin:
    """Encode strings manually, including every JSON control character."""

    @staticmethod
    def _quote(value: str) -> str:
        encoded = '"'
        for character in value:
            if character == '"':
                encoded += '\\"'
            elif character == "\\":
                encoded += "\\\\"
            elif ord(character) < 32 or 0xD800 <= ord(character) <= 0xDFFF:
                encoded += f"\\u{ord(character):04x}"
            else:
                encoded += character
        return encoded + '"'

    def process_output(self, data: list[tuple[int, str]]) -> None:
        items = [f'"item_{rank}": {self._quote(value)}'
                 for rank, value in data]
        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
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
    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()
    next_batch: list[Any] = [
        21, ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR", "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168], "World hello",
    ]
    print(f"Send another batch of data: {next_batch}")
    stream.process_stream(next_batch)
    stream.print_processors_stats()
    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
