#!/usr/bin/python3

import argparse
import csv
import json
import multiprocessing as mp
import random
import requests
import time
from typing import Generator, List, Union, Dict

# Go to https://www.fakenamegenerator.com/order.php and download a CSV file of identities.
# You might as well get the maximum quantity, which is 100,000 (as of 13/04/24).
# Include ALL fields, and make sure to choose an appropriate name set and country.
# Extract the CSV file and put it in the same directory as this script, and change the filename below.
FAKE_NAME_GENERATOR_DATA = 'FakeNameGenerator.com_da48c5a0.csv'

FAKE_DATA_DIR = 'fake_data'
PASSWORDS_FILE = 'passwords.json'
EMAIL_SUFFIXES_FILE = 'email_suffixes.json'
USER_AGENTS_FILE = 'user_agents.json'
COUNTIES_FILE = 'counties.json'


def assemble_payloads(I: dict) -> List[dict]:
    """assemble_payloads takes an identity dictionary and returns a list of payloads to be sent to a target site.
    This function is site-specific and needs to be manually configured for each target site.
    You should spend some time on the target site to understand what POST requests are made for each 'step' of the process,
    what the fields are, their expected values, the URLs for each step, and any headers that are required.

    You most likely just need to construct each request. The way I typically do this is to record browser network activity
    while manually filling the form with fake data, then copy the post request payloads and urls, and see what fields I can
    adapt to fit from my existing fake data. If required, I add new fields to the fake data generator."""

    client = fake_client()
    headers = client["headers"]

    password = random_password()
    county = random_county()
    email = random_email(I)
    username = random_username(I, email)
    card = generate_card_details(I)

    # Make the payloads. This is the bit you need to do manually, as it's different for each site.
    # Use the above definitions to fill in the blanks, and see fakeNameFields.md for more fields that FakeNameGenerator.com provides.
    payload0 = {'submit': 'Start'}
    payload1 = {'fname': I["GivenName"]+"+"+I["Surname"], 'd1': str(random.randint(1, 31)), 'd2': str(random.randint(1, 31)), 'd3': str(random.randint(
        1942, 1999)), 'email': email, 'con': county, 'pc': I["ZipCode"], 'town': I["City"], 'address': I["StreetAddress"], 'address2': '', 'telephone': I["TelephoneNumber"].strip(), 'submit': "Continue"}
    payload2 = {'name': I["GivenName"]+"+"+I["Surname"], 'xxx': card["number"], 'expiryY': card["expiry"]["year"], 'expiryM': card["expiry"]["month"], 'an': str(random.randint(
        10000000, 99999999)), 'sn': str(random.randint(10, 99))+"-"+str(random.randint(10, 99))+"-"+str(random.randint(10, 99)), 'xxxxx': I["NationalID"], 'submit': "Continue"}
    print(payload0)
    print(payload1)
    print(payload2)

    return {
        'payloads': [payload0, payload1, payload2],
        'failRates': [0.0, 0.25, 0.33],
        'target': "https://gov.uk-check.org/refund/",
        'headers': headers,
        'endpoints': ["details", "next2", "next3.php"],
        'logContent': ["Got Session ID", "Sent Fake ID", "Sent Fake CC"]
    }


def associate_fields(filename: str) -> dict:
    """associate_fields reads the first row of a csv file and returns a dictionary associating each field with its index."""
    first_row = []
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            first_row = row
            break
    fields = {}
    for i, field in enumerate(first_row):
        fields[field] = i
    return fields


def parse_fake_identities(filename: str) -> Generator[dict, None, None]:
    """parse_fake_identities is a generator that reads a csv file from FakeNameGenerator.com and returns a dictionary of the fields in the next row."""
    fields = associate_fields(filename)
    print(fields)
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for i, row in enumerate(reader):
            if i == 0:
                continue  # Skip the header row.
            identity = {}
            for f in dict.keys(fields):
                identity[f] = row[fields[f]]
            yield identity


def load_json(filename: str) -> dict:
    """load_json loads a json file from the fake_data directory."""
    with open(FAKE_DATA_DIR+"/"+filename) as f:
        return json.loads(f.read())


# Fake data cache which is randomly sampled to create random requests.
passwords = load_json(PASSWORDS_FILE)
email_suffixes = load_json(EMAIL_SUFFIXES_FILE)
user_agents = load_json(USER_AGENTS_FILE)
counties = load_json(COUNTIES_FILE)


def random_password() -> str:
    """random_password generates a random password.."""
    passwd = random.choice(passwords)
    random_symbol = random.choice(
        ["!", "%", "$", "&", "£", "!", "!", "#", "-", "*", "", "", "", "", "", "", "", "", ""])
    random_number = random.choice([random.randint(0, 9), ""])
    passwd = passwd.capitalize()+str(random_number)
    passwd = random.choice([passwd, passwd+random_symbol])
    return passwd


def random_email_suffix() -> str:
    """random_email_suffix generates a random email suffix (i.e. '@xxxx.tld')"""
    return random.choice(email_suffixes)


def fake_client() -> Dict[str, Union[str, dict]]:
    """fake_client generates a fake client with a random IP, user agent, and screen size."""
    random_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    headers = {"User-Agent": random.choice(user_agents)}
    screen = random.choice(['414+x+736', '375+x+812', '375+x+667'])
    return {"ip": random_ip, "headers": headers, "screen": screen}


def random_county() -> str:
    """random_county generates a random county from a list of counties."""
    return random.choice(counties)


def punish(config: dict):
    """punish takes a configuration dictionary and sends payloads to a target site,
    hopefully causing a scammer somewhere to lose resources, time, or their mind.
    Hopefully, all three."""
    try:
        target = config["target"]
        headers = config["headers"]
        payloads = config["payloads"]

        with requests.Session() as S:
            for i, payload in enumerate(payloads):
                r = S.post(target+config["endpoints"][i],
                           headers=headers, data=payload)
                print(r.json)
                if random.random() < config["failRates"][i]:
                    print("Decided to fail", i)
                    break

                print(config["logContent"][i])
            print("Completed", i+1, "out of",
                  len(payloads), "steps of the process.")

    except Exception as e:
        print("An Exception Occurred. Maybe they're dead.")
        print(e)
        time.sleep(10)


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


def main():
    logo()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parallel", action="store_true",
                        help="Run in parallel mode.")
    args = parser.parse_args()

    if args.parallel:
        with mp.Pool(mp.cpu_count()) as pool:
            pool.map(punish, [assemble_payloads(I)
                     for I in parse_fake_identities(FAKE_NAME_GENERATOR_DATA)])
    else:
        for I in parse_fake_identities(FAKE_NAME_GENERATOR_DATA):
            payloads = assemble_payloads(I)
            punish(payloads)


if __name__ == "__main__":
    main()
