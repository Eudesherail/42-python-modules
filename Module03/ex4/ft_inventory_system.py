import sys


def parse_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for argument in arguments:
        try:
            item, quantity_text = argument.split(":")
            if not item:
                raise ValueError("empty item name")
        except ValueError:
            print(f"Error - invalid parameter '{argument}'")
            continue
        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue
        try:
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError("quantity cannot be negative")
        except ValueError as error:
            print(f"Quantity error for '{item}': {error}")
            continue
        inventory[item] = quantity
    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")
    items = list(inventory.keys())
    print(f"Item list: {items}")
    total = sum(inventory.values())
    print(f"Total quantity of the {len(items)} items: {total}")
    for item in inventory:
        percentage = round(inventory[item] / total * 100, 1) if total else 0.0
        print(f"Item {item} represents {percentage}%")
    if items:
        most = least = items[0]
        for item in inventory:
            if inventory[item] > inventory[most]:
                most = item
            if inventory[item] < inventory[least]:
                least = item
        print(f"Item most abundant: {most} with quantity {inventory[most]}")
        print(f"Item least abundant: {least} with quantity {inventory[least]}")
    else:
        print("Inventory is empty; no most or least abundant item.")
    new_item = "magic_item"
    while new_item in inventory:
        new_item += "_new"
    inventory.update({new_item: 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
