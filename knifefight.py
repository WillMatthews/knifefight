#!/usr/bin/python3

import requests
import os
import random
import string
import json
import csv
import time

# Go to https://www.fakenamegenerator.com/order.php and download a CSV file of identities.
# You might as well get the maximum quantity, which is 100,000 (as of 13/04/24).
# Include ALL fields, and make sure to choose an appropriate name set and country.
# Extract the CSV file and put it in the same directory as this script, and change the filename below.
datafile = "FakeNameGenerator.com_da48c5a0.csv"

def associateFields(filename: str) -> dict:
    """associateFields reads the first row of a csv file and returns a dictionary associating each field with its index."""
    first_row = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            first_row = row
            break
    fields = {}
    for i, field in enumerate(first_row):
        fields[field] = i
    return fields

def parseFakeNameGen(filename: str) -> dict:
    """parseFakeNameGen is a generator that reads a csv file from FakeNameGenerator.com and returns a dictionary of the fields in the next row."""
    fields = associateFields(filename)
    print(fields)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            identity = {}
            for f in dict.keys(fields):
                identity[f] = row[fields[f]]
            yield identity

passwords = json.loads(open('pwds.json').read())
def randomPassword() -> str:
    """randomPassword generates a random password.."""
    passwd = random.choice(passwords)
    randsym = random.choice(["!","%","$","&","£","!","!","#","-","*","","","","","","","","",""])
    randnum = random.choice([random.randint(0,9),""])
    passwd = passwd.capitalize()+str(randnum)
    passwd = random.choice([passwd, passwd+randsym])
    return passwd

user_agents = json.loads(open('uas.json').read())
def fakeClient() -> {"ip":str, "headers":dict, "screen":str}:
    randip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    headers = {"User-Agent":random.choice(user_agents)}
    screen = random.choice(['414+x+736', '375+x+812','375+x+667'])
    return {"ip":randip, "headers":headers, "screen":screen}

counties = json.loads(open('counties.json').read())
def randomCounty() -> str:
    return random.choice(counties)

def logo():
    print("""
    ██╗░░██╗███╗░░░██╗██╗███████╗███████╗███████╗██╗░██████╗░██╗░░██╗████████╗
    ██║░██╔╝████╗░░██║██║██╔════╝██╔════╝██╔════╝██║██╔════╝░██║░░██║╚══██╔══╝
    █████╔╝░██╔██╗░██║██║█████╗░░█████╗░░█████╗░░██║██║░░███╗███████║░░░██║░░░
    ██╔═██╗░██║╚██╗██║██║██╔══╝░░██╔══╝░░██╔══╝░░██║██║░░░██║██╔══██║░░░██║░░░
    ██║░░██╗██║░╚████║██║██║░░░░░███████╗██║░░░░░██║╚██████╔╝██║░░██║░░░██║░░░
    ╚═╝░░╚═╝╚═╝░░╚═══╝╚═╝╚═╝░░░░░╚══════╝╚═╝░░░░░╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░""")

def randomEmail(I: dict) -> str:
    eml_prefix = random.choice(
            [I["Username"],
            I["GivenName"]+"."+I["Surname"],
            I["GivenName"]+"."+I["Surname"]+I["Birthday"][-3:-1],
            I["GivenName"]+I["Surname"],
            I["GivenName"]+I["Surname"]+I["Birthday"][-3:-1],
            I["GivenName"]+I["Surname"]+I["Birthday"][-2:-1],
            I["EmailAddress"]
        ])
    eml_suffix = random.choice(["yahoo.com", "btinternet.co.uk","gmail.com","icloud.com","outlook.com","hotmail.com","hotmail.co.uk","yahoo.co.uk","aol.com","gmail.com"])
    email = eml_prefix if "@" in eml_prefix else eml_prefix+"@"+eml_suffix
    return email

def getCard(I: dict) -> {"number":str, "expiry": {"month":str, "year":str, "mm":str, "yy":str, "mm/yy":str}, "cvv":str, "name":str}:
    """getCard takes an identity dictionary and returns a dictionary of card details."""
    exp = I["CCExpires"].split("/")
    expiry = {
        "month":exp[0],
        "year":exp[1],
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

def assemblePayloads(I: dict) -> [dict]:
    """assemblePayloads takes an identity dictionary and returns a list of payloads to be sent to a target site."""
    client = fakeClient()
    headers = client["headers"]

    passwd = randomPassword()
    county = randomCounty()
    email  = randomEmail(I)
    card   = getCard(I)

    digits = "".join([str(random.randint(0,9)) for i in range(random.randint(5,16))])
    username = random.choice([digits, email.split("@")[0], email])

    # Make the payloads. This is the bit you need to do manually, as it's different for each site.
    # Use the above definitions to fill in the blanks, and see fakeNameFields.md for more fields that FakeNameGenerator.com provides.
    payload0={'submit':'Start'}
    payload1={'fname':I["GivenName"]+"+"+I["Surname"],'d1':str(random.randint(1,31)),'d2':str(random.randint(1,31)),'d3':str(random.randint(1942,1999)),'email':email,'con':county,'pc':I["ZipCode"],'town':I["City"],'address':I["StreetAddress"],'address2':'','telephone':I["TelephoneNumber"].strip(),'submit':"Continue"}
    payload2={'name': I["GivenName"]+"+"+I["Surname"], 'xxx':card["number"], 'expiryY': card["expiry"]["year"], 'expiryM': card["expiry"]["month"], 'an': str(random.randint(10000000,99999999)), 'sn':str(random.randint(10,99))+"-"+str(random.randint(10,99))+"-"+str(random.randint(10,99)), 'xxxxx':I["NationalID"], 'submit':"Continue"}
    print(payload0)
    print(payload1)
    print(payload2)

    config = {
        payloads: [payload0, payload1, payload2],
        failRates: [0.0, 0.25, 0.33],
        target: "https://gov.uk-check.org/refund/"
        endpoints: ["details", "next2", "next3.php"]
        logContent: ["Got Session ID", "Sent Fake ID", "Sent Fake CC"]
    }
    return config


def punish(config: dict):
    """punish takes a configuration dictionary and sends payloads to a target site,
    hopefully causing a scammer somewhere to lose resources, time, or their mind.
    Hopefully, all three."""
    try:
        with requests.Session() as S:
            while j < len(config["payloads"]):
                r = S.post(target+config["endpoints"][j], headers=headers, data=config["payloads"][j])
                print(r.json)
                if random.random() < config["failRates"][j]:
                    print("Decided to fail", j)
                    break
                print(config["logContent"][j])
                j += 1
            print("Completed", i, "identities")
    except Exception as e:
        print("An Exception Occured. Maybe they're dead.")
        print(e)
        time.sleep(10)

def main():
    ids = parseFakeNameGen(datafile)
    for i, I in enumerate(ids):
        if i == 0:
            logo()
            # Skip the first identity- it's the header row.
            continue

        payloads = assemblePayloads(I)
        punish(payloads)

if __name__ == "__main__":
    main()

