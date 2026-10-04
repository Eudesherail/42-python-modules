def secure_archive(filename: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    """Read or replace a UTF-8 archive and always close its handle."""
    try:
        if action == "read":
            with open(filename, "r", encoding="utf-8") as archive:
                return True, archive.read()
        if action == "write":
            with open(filename, "w", encoding="utf-8") as archive:
                archive.write(content)
            return True, "Content successfully written to file"
        return False, "Invalid action: use 'read' or 'write'"
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        return False, str(error)


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print("Using 'secure_archive' to read from a regular file:")
    success, data = secure_archive("ancient_fragment.txt")
    print((success, data))
    if success:
        print("Using 'secure_archive' to write previous content "
              "to a new file:")
        print(secure_archive("new_fragment.txt", "write", data))
