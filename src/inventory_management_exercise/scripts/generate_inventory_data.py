#!/usr/bin/env python3
"""Script to generate realistic inventory data."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Real-world data
ARCHITECTURES = [
    ("x86_64", "64-bit x86 architecture"),
    ("arm64", "64-bit ARM architecture"),
    ("x86", "32-bit x86 architecture"),
    ("arm", "32-bit ARM architecture"),
    ("riscv64", "64-bit RISC-V architecture"),
]

MANUFACTURERS = [
    ("Intel", "Santa Clara", "USA", "https://www.intel.com", "+1-408-765-8080", "contact@intel.com"),
    ("Apple", "Cupertino", "USA", "https://www.apple.com", "+1-408-996-1010", "contact@apple.com"),
    ("AMD", "Santa Clara", "USA", "https://www.amd.com", "+1-408-749-4000", "contact@amd.com"),
    ("Qualcomm", "San Diego", "USA", "https://www.qualcomm.com", "+1-858-587-1121", "contact@qualcomm.com"),
    ("Samsung", "Suwon", "South Korea", "https://www.samsung.com", "+82-2-2053-3000", "contact@samsung.com"),
    ("Dell", "Round Rock", "USA", "https://www.dell.com", "+1-512-728-7800", "contact@dell.com"),
    ("HP", "Palo Alto", "USA", "https://www.hp.com", "+1-650-857-1501", "contact@hp.com"),
    ("Lenovo", "Beijing", "China", "https://www.lenovo.com", "+86-10-58868888", "contact@lenovo.com"),
]

# Real-world computer configurations
COMPUTER_CONFIGS = [
    # Apple Computers
    {
        "computer_type": "Laptop",
        "manufacturer": "Apple",
        "cpu_model": "Apple M2",
        "cpu_manufacturer": "Apple",
        "cpu_cores": 8,
        "os_name": "macOS",
        "os_version": "13.2.1",
        "os_type": "macOS",
        "min_cost": 1299,
        "max_cost": 1599,
        "memory_options": [8, 16],
        "model_prefix": "MacBook Air",
    },
    {
        "computer_type": "Laptop",
        "manufacturer": "Apple",
        "cpu_model": "Apple M2 Pro",
        "cpu_manufacturer": "Apple",
        "cpu_cores": 10,
        "os_name": "macOS",
        "os_version": "13.2.1",
        "os_type": "macOS",
        "min_cost": 1999,
        "max_cost": 2499,
        "memory_options": [16, 32],
        "model_prefix": "MacBook Pro",
    },
    # Dell Computers
    {
        "computer_type": "Laptop",
        "manufacturer": "Dell",
        "cpu_model": "Intel Core i7-12700H",
        "cpu_manufacturer": "Intel",
        "cpu_cores": 14,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1299,
        "max_cost": 1599,
        "memory_options": [16, 32],
        "model_prefix": "XPS 15",
    },
    {
        "computer_type": "Desktop",
        "manufacturer": "Dell",
        "cpu_model": "Intel Core i9-13900K",
        "cpu_manufacturer": "Intel",
        "cpu_cores": 24,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1999,
        "max_cost": 2499,
        "memory_options": [32, 64],
        "model_prefix": "XPS Desktop",
    },
    # HP Computers
    {
        "computer_type": "Laptop",
        "manufacturer": "HP",
        "cpu_model": "AMD Ryzen 7 7840U",
        "cpu_manufacturer": "AMD",
        "cpu_cores": 8,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 999,
        "max_cost": 1299,
        "memory_options": [16, 32],
        "model_prefix": "Envy x360",
    },
    {
        "computer_type": "Desktop",
        "manufacturer": "HP",
        "cpu_model": "AMD Ryzen 9 7950X",
        "cpu_manufacturer": "AMD",
        "cpu_cores": 16,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1499,
        "max_cost": 1999,
        "memory_options": [32, 64],
        "model_prefix": "Pavilion Desktop",
    },
    # Lenovo Computers
    {
        "computer_type": "Laptop",
        "manufacturer": "Lenovo",
        "cpu_model": "Intel Core i7-13700H",
        "cpu_manufacturer": "Intel",
        "cpu_cores": 14,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1299,
        "max_cost": 1599,
        "memory_options": [16, 32],
        "model_prefix": "ThinkPad X1 Carbon",
    },
    {
        "computer_type": "Desktop",
        "manufacturer": "Lenovo",
        "cpu_model": "Intel Core i9-13900K",
        "cpu_manufacturer": "Intel",
        "cpu_cores": 24,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1999,
        "max_cost": 2499,
        "memory_options": [32, 64],
        "model_prefix": "ThinkStation",
    },
    # Samsung Computers
    {
        "computer_type": "Laptop",
        "manufacturer": "Samsung",
        "cpu_model": "Intel Core i7-1360P",
        "cpu_manufacturer": "Intel",
        "cpu_cores": 12,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 1299,
        "max_cost": 1599,
        "memory_options": [16, 32],
        "model_prefix": "Galaxy Book3",
    },
    {
        "computer_type": "Tablet",
        "manufacturer": "Samsung",
        "cpu_model": "Snapdragon 8 Gen 2",
        "cpu_manufacturer": "Qualcomm",
        "cpu_cores": 8,
        "os_name": "Windows 11 Pro",
        "os_version": "22H2",
        "os_type": "Windows",
        "min_cost": 999,
        "max_cost": 1299,
        "memory_options": [8, 16],
        "model_prefix": "Galaxy Tab S9",
    },
]


def generate_serial_number(manufacturer: str) -> str:
    """Generate a realistic serial number based on manufacturer."""
    prefix = {
        "Dell": "DELL",
        "HP": "HP",
        "Lenovo": "LEN",
        "Apple": "A",
        "Samsung": "SAMS",
    }.get(manufacturer, "UNK")

    year = str(random.randint(2020, 2024))
    month = str(random.randint(1, 12)).zfill(2)
    random_part = "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=8))

    return f"{prefix}{year}{month}{random_part}"


def generate_model_number(computer_type: str, manufacturer: str, model_prefix: str) -> str:
    """Generate a realistic model number based on computer type and manufacturer."""
    year = str(random.randint(2020, 2023))
    model = str(random.randint(1000, 9999))

    return f"{model_prefix}-{year}{model}"


def generate_inventory_data(num_records: int = 1000) -> list[dict]:
    """Generate realistic inventory data."""
    records = []

    for _ in range(num_records):
        # Select random computer configuration
        config = random.choice(COMPUTER_CONFIGS)

        # Generate computer-specific data
        purchase_date = date(2020, 1, 1) + timedelta(days=random.randint(0, 1095))  # 3 years
        original_cost = round(random.uniform(config["min_cost"], config["max_cost"]), 2)
        installed_memory = random.choice(config["memory_options"])
        max_memory = installed_memory * 2  # Most modern systems can double their memory

        # Get manufacturer details
        manufacturer = next(m for m in MANUFACTURERS if m[0] == config["manufacturer"])

        record = {
            "architecture_name": "arm64" if config["cpu_manufacturer"] == "Apple" else "x86_64",
            "architecture_description": "64-bit ARM architecture"
            if config["cpu_manufacturer"] == "Apple"
            else "64-bit x86 architecture",
            "manufacturer_name": manufacturer[0],
            "manufacturer_city": manufacturer[1],
            "manufacturer_country": manufacturer[2],
            "manufacturer_website": manufacturer[3],
            "manufacturer_phone": manufacturer[4],
            "manufacturer_email": manufacturer[5],
            "cpu_model": config["cpu_model"],
            "cpu_manufacturer": config["cpu_manufacturer"],
            "cpu_cores": config["cpu_cores"],
            "operating_system_name": config["os_name"],
            "operating_system_version": config["os_version"],
            "operating_system_os_type": config["os_type"],
            "computer_computer_type": config["computer_type"],
            "computer_purchase_date": purchase_date.isoformat(),
            "computer_original_cost": original_cost,
            "computer_installed_memory": installed_memory,
            "computer_max_memory": max_memory,
            "computer_system_model": generate_model_number(
                config["computer_type"], config["manufacturer"], config["model_prefix"]
            ),
            "computer_serial_number": generate_serial_number(config["manufacturer"]),
            "computer_cpu_count": 1,  # Most modern systems have a single CPU
        }
        records.append(record)

    return records


def main():
    """Generate inventory data and save to CSV."""
    output_file = Path(__file__).parent / "inventory_data.csv"
    records = generate_inventory_data()

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records in {output_file}")


if __name__ == "__main__":
    main()
