import argparse
import logging
import multiprocessing as mp
import random
import requests
import time
from typing import Dict, List

from config import FAKE_NAME_GENERATOR_DATA
from fake_data import *
from utils import parse_fake_identities, logo


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def assemble_payloads(identity: Dict[str, str]) -> Dict[str, List]:
    """Assemble payloads to be sent to a target site based on the identity provided.
    Takes an identity dictionary and returns a list of payloads to be sent to a target site.
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
    email = random_email(identity)
    username = random_username(identity, email)
    card = generate_card_details(identity)

    payload0 = {'submit': 'Start'}
    payload1 = {
        'fname': identity["GivenName"] + " " + identity["Surname"],
        'd1': str(random.randint(1, 31)),
        'd2': str(random.randint(1, 31)),
        'd3': str(random.randint(1942, 1999)),
        'email': email,
        'con': county,
        'pc': identity["ZipCode"],
        'town': identity["City"],
        'address': identity["StreetAddress"],
        'address2': '',
        'telephone': identity["TelephoneNumber"].strip(),
        'submit': "Continue"
    }
    payload2 = {
        'name': identity["GivenName"] + " " + identity["Surname"],
        'xxx': card["number"],
        'expiryY': card["expiry"]["year"],
        'expiryM': card["expiry"]["month"],
        'an': str(random.randint(10000000, 99999999)),
        'sn': "-".join([str(random.randint(10, 99)) for _ in range(3)]),
        'xxxxx': identity["NationalID"],
        'submit': "Continue"
    }

    return {
        'payloads': [payload0, payload1, payload2],
        'failRates': [0.0, 0.25, 0.33],
        'target': "https://gov.uk-check.org/refund/",
        'headers': headers,
        'endpoints': ["details", "next2", "next3.php"],
        'logContent': ["Got Session ID", "Sent Fake ID", "Sent Fake CC"]
    }


def punish(config: Dict[str, List]):
    """Send payloads to a target site."""
    try:
        target = config["target"]
        headers = config["headers"]
        payloads = config["payloads"]

        with requests.Session() as session:
            for i, payload in enumerate(payloads):
                response = session.post(target + config["endpoints"][i], headers=headers, data=payload)
                logging.info(response.json)
                if random.random() < config["failRates"][i]:
                    logging.info(f"Decided to fail at step {i}")
                    break
                logging.info(config["logContent"][i])
            logging.info(f"Completed {i + 1} out of {len(payloads)} steps of the process.")
    except Exception as e:
        logging.error("An exception occurred: %s", e)
        time.sleep(10)


def main():
    logo()
    setup_logging()
    logging.info("Script started")

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parallel", action="store_true", help="Run in parallel mode.")
    args = parser.parse_args()

    if args.parallel:
        with mp.Pool(mp.cpu_count()) as pool:
            pool.map(punish, [assemble_payloads(identity) for identity in parse_fake_identities(FAKE_NAME_GENERATOR_DATA)])
    else:
        for identity in parse_fake_identities(FAKE_NAME_GENERATOR_DATA):
            payloads = assemble_payloads(identity)
            punish(payloads)


if __name__ == "__main__":
    main()
