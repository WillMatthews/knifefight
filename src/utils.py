import csv
from typing import Generator, Dict


def associate_fields(filename: str) -> Dict[str, int]:
    """Associate fields in the first row of a CSV file with their indices."""
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        return {field: i for i, field in enumerate(next(reader))}


def parse_fake_identities(filename: str) -> Generator[dict, None, None]:
    """Parse fake identities from a CSV file and yield them as dictionaries."""
    fields = associate_fields(filename)
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader)  # Skip header row
        for row in reader:
            yield {f: row[idx] for f, idx in fields.items()}


def logo():
    """logo prints a text logo to the console."""
    logo_str = """
    ██╗░░██╗███╗░░░██╗██╗███████╗███████╗███████╗██╗░██████╗░██╗░░██╗████████╗
    ██║░██╔╝████╗░░██║██║██╔════╝██╔════╝██╔════╝██║██╔════╝░██║░░██║╚══██╔══╝
    █████╔╝░██╔██╗░██║██║█████╗░░█████╗░░█████╗░░██║██║░░███╗███████║░░░██║░░░
    ██╔═██╗░██║╚██╗██║██║██╔══╝░░██╔══╝░░██╔══╝░░██║██║░░░██║██╔══██║░░░██║░░░
    ██║░░██╗██║░╚████║██║██║░░░░░███████╗██║░░░░░██║╚██████╔╝██║░░██║░░░██║░░░
    ╚═╝░░╚═╝╚═╝░░╚═══╝╚═╝╚═╝░░░░░╚══════╝╚═╝░░░░░╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░"""

    # Color the logo: █ is white, ░ is blue, and ║╚═╝╔╗ is yellow.
    logo_str = logo_str.replace("░", "\033[94m░\033[0m")
    logo_str = logo_str.replace("█", "\033[97m█\033[0m")
    double_lined = ["║", "╚", "═", "╝", "╗", "╔"]
    for c in double_lined:
        logo_str = logo_str.replace(c, "\033[93m"+c+"\033[0m")

    print(logo_str)
