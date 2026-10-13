import sys
import typing


def report_error(message: str) -> None:
    print(f"[STDERR] {message}", file=sys.stderr)


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


def transform_data(content: str) -> str:
    lines = []
    for line in content.splitlines():
        lines.append(line + "#\n")
    return "".join(lines)


def save_archive(filename: str, content: str) -> bool:
    archive: typing.IO[str] | None = None
    success = False
    print(f"Saving data to '{filename}'")
    try:
        archive = open(filename, "w", encoding="utf-8")
        archive.write(content)
        success = True
    except (OSError, UnicodeError, ValueError) as error:
        report_error(f"Error opening or writing file '{filename}': {error}")
    finally:
        if archive is not None:
            try:
                archive.close()
            except OSError as error:
                report_error(f"Error closing file '{filename}': {error}")
                success = False
    if success:
        print(f"Data saved in file '{filename}'.")
    else:
        print("Data not saved.")
    return success


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return
    print("=== Cyber Archives Recovery & Preservation ===")
    content = read_archive(sys.argv[1])
    if content is None:
        return
    transformed = transform_data(content)
    print("Transform data:")
    print("---")
    print(transformed, end="")
    print("---")
    try:
        sys.stdout.write("Enter new file name (or empty): ")
        sys.stdout.flush()
        filename = sys.stdin.readline().rstrip("\r\n")
    except (EOFError, KeyboardInterrupt, OSError, UnicodeError) as error:
        report_error(f"Input interrupted: {error}")
        return
    if not filename:
        print("Not saving data.")
        return
    save_archive(filename, transformed)


if __name__ == "__main__":
    main()
