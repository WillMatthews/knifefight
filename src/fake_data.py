import json
import os
import random
from typing import Dict

from config import FAKE_DATA_DIR, PASSWORDS_FILE, EMAIL_SUFFIXES_FILE, USER_AGENTS_FILE, COUNTIES_FILE


def load_json(filename: str) -> dict:
    """Load a JSON file from the fake_data directory."""
    with open(os.path.join(FAKE_DATA_DIR, filename)) as f:
        return json.load(f)


passwords = load_json(PASSWORDS_FILE)
email_suffixes = load_json(EMAIL_SUFFIXES_FILE)
user_agents = load_json(USER_AGENTS_FILE)
counties = load_json(COUNTIES_FILE)


def random_password() -> str:
    """Generate a random password."""
    passwd = random.choice(passwords).capitalize()
    random_symbol = random.choice(["!", "%", "$", "&", "£", "#", "-", "*", ""])
    random_number = random.choice([str(random.randint(0, 9)), ""])
    passwd += random_number
    return passwd if random.choice([True, False]) else passwd + random_symbol


def random_email_suffix() -> str:
    """Generate a random email suffix (i.e. '@xxxx.tld')."""
    return random.choice(email_suffixes)


def random_email(I: dict) -> str:
    """random_email generates a random email address from an identity dictionary."""
    eml_prefix = random.choice(
        [I["Username"],
         I["GivenName"]+"."+I["Surname"],
         I["GivenName"]+"."+I["Surname"]+I["Birthday"][-3:-1],
         I["GivenName"]+I["Surname"],
         I["GivenName"]+I["Surname"]+I["Birthday"][-3:-1],
         I["GivenName"]+I["Surname"]+I["Birthday"][-2:-1],
         I["EmailAddress"]
         ])
    return eml_prefix if "@" in eml_prefix else eml_prefix+"@"+random_email_suffix()


def random_username(I: dict, email: str) -> str:
    """random_username generates a random username from an identity dictionary and email address."""
    digits = "".join([str(random.randint(0, 9))
                     for _ in range(random.randint(5, 16))])
    return random.choice([digits, email.split(
        "@")[0], email, I["Username"], I["GivenName"]+I["Surname"]])


def fake_client() -> Dict[str, str]:
    """Generate a fake client with a random IP, user agent, and screen size."""
    random_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    headers = {"User-Agent": random.choice(user_agents)}
    return {"ip": random_ip, "headers": headers}


def random_county() -> str:
    """Generate a random county from a list of counties."""
    return random.choice(counties)


def generate_card_details(I: dict) -> Dict[str, Dict[str, str]]:
    """generate_card_details takes an identity dictionary and returns a dictionary of card details."""
    exp = I["CCExpires"].split("/")
    expiry = {
        "month": exp[0],
        "year": exp[1],
        "mm": str(exp[0].zfill(2)),
        "yy": str(exp[1][-2:]),
        "mm/yy": str(exp[0].zfill(2))+"/"+str(exp[1][-2:])
    }
    return {
        "number": I["CCNumber"],
        "expiry": expiry,
        "cvv": I["CVV2"],
        "name": I["GivenName"]+" "+I["Surname"]
    }
