import sys
import typing


def report_error(message: str) -> None:
    print(message)


def read_archive(filename: str) -> str | None:
    archive: typing.IO[str] | None = None
    content: str | None = None
    print(f"Accessing file '{filename}'")
    try:
        archive = open(filename, "r", encoding="utf-8")
        content = archive.read()
    except (OSError, UnicodeError, ValueError) as error:
        report_error(f"Error opening or reading file '{filename}': {error}")
    finally:
        if archive is not None:
            try:
                archive.close()
            except OSError as error:
                report_error(f"Error closing file '{filename}': {error}")
                content = None
    if content is not None:
        print("---")
        print(content, end="" if content.endswith("\n") else "\n")
        print("---")
        print(f"File '{filename}' closed.")
    return content


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    print("=== Cyber Archives Recovery ===")
    read_archive(sys.argv[1])


if __name__ == "__main__":
    main()
