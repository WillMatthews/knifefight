#!/usr/bin/python3

import requests
import os
import random
import string
import json
import csv
import time


"""
1Number,
2Gender,
3NameSet,
4Title,
5GivenName,
6MiddleInitial,
7Surname,
8StreetAddress,
9City,
10State,
11StateFull,
12ZipCode,
13Country,
14CountryFull,
15EmailAddress,
16Username,
17Password,
18BrowserUserAgent,
19TelephoneNumber,
20TelephoneCountryCode,
21MothersMaiden,
22Birthday,
23Age,
24TropicalZodiac,
25CCType,
26CCNumber,
27CVV2,
28CCExpires,
"""


start_val =  random.randint(0,90000)
passwords = json.loads(open('pwds.json').read())
user_agents = json.loads(open('uas.json').read())
counties = json.loads(open('counties.json').read())

itervar = 1
with open("./FakeNameGenerator.com_e75ab0f0.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    for i, I in enumerate(reader):
        if i < 1 + start_val:
            continue

        # Fake Client Gen
        randip =".".join(map(str, (random.randint(0, 255)
                    for _ in range(4))))
        headers={"User-Agent":random.choice(user_agents)}
        screen = random.choice(['414+x+736', '375+x+812','375+x+667'])

        # Fake ID Gen
        county = random.choice(counties)
        passwd = random.choice(passwords)
        eml_prefix = random.choice(
                [I[15],
                I[4]+"."+I[6],
                I[4]+"."+I[6]+I[21][-3:-1],
                I[4]+I[5]+I[6],
                I[4]+I[5]+I[6]+I[21][-3:-1],
                I[4]+I[6]+I[21][-2:-1],
                I[14]
            ])
        eml_suffix = random.choice(["yahoo.com", "btinternet.co.uk","gmail.com","icloud.com","outlook.com","hotmail.com","hotmail.co.uk","yahoo.co.uk","aol.com","gmail.com"])

        if "@" not in eml_prefix:
            email = eml_prefix+"@"+eml_suffix
        else:
            email = eml_prefix

        # Fake Username Gen
        digits = "".join([str(random.randint(0,9)) for i in range(random.randint(5,16))])
        username = random.choice([digits,eml_prefix,email])


        # Fake Password Gen
        randsym = random.choice(["!","%","$","&","£","!","!","#","-","*","","","","","","","","",""])
        randnum = random.choice([random.randint(0,9),""])
        passwd = passwd.capitalize()+str(randnum)
        passwd = random.choice([passwd, passwd+randsym])


        # Make the payload.
        payload0={'submit':'Start'}
        payload1 = {'fname':I[4]+"+"+I[6],'d1':str(random.randint(1,31)),'d2':str(random.randint(1,31)),'d3':str(random.randint(1942,1999)),'email':email,'con':county,'pc':I[11],'town':I[8],'address':I[7],'address2':'','telephone':I[18].strip(),'submit':"Continue"}
        payload2= {'name':I[4]+"+"+I[6], 'xxx':I[25], 'expiryY': str(random.randint(2022,2029)) , 'expiryM': str(random.randint(1,12)), 'an': str(random.randint(10000000,99999999)), 'sn':str(random.randint(10,99))+"-"+str(random.randint(10,99))+"-"+str(random.randint(10,99)), 'xxxxx':I[26], 'submit':"Continue"}
        print(payload0)
        print(payload1)
        print(payload2)

        # Send
        try:
            with requests.Session() as S:
                r1 = S.post("https://gov.uk-check.org/refund/details", headers=headers, data=payload0)
                print(r1.json)
                print("GOT SESSID")
                if random.choice([0,0,0,1]) == 0:
                    r2 = S.post("https://gov.uk-check.org/refund/next2", headers=headers, data=payload1)
                    print(r2.json)
                    print("SENT FAKE ID")

                    if random.choice([0,0,1]) == 0:
                        r3 = S.post("https://gov.uk-check.org/refund/next3.php",headers=headers,data=payload2)
                        print(r3.json)
                        print(i, ": Sent Fake CC")

                print("Completed", itervar, "identities")
        except Exception as e:
            print("An Exception Occured. Maybe they're dead.")
            print(e)
            time.sleep(10)

        itervar += 1
