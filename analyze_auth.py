#!/usr/bin/env python
# coding: utf-8

# A program to analyze auth.log files looking for people trying to login
# to either an account that doesn't exist (Failed password for invalid user)
# or an account that does exist but which the user has a bad password
# (Failed password)

import glob
import json
import os
import pprint
import sys
from typing import Dict, Tuple

import requests
global agg_dict

CC = "country_code"
CN = "country_name"
US = "username"
pp = pprint.PrettyPrinter(indent=4, width=200)

print(os.getcwd())
with open(sys.argv[1], "rt") as fp:
    records = fp.readlines()
print(f"Read {len(records)} raw records")

# keep the API key from IPAPI someplace accessible but where it's unlikely to
# get uploaded to a github repository or get lost or destroyed.
with open("/tmp/ipapi_api_key", "rt") as fp:
    api_key = fp.readline().strip()

# There is a file, currently called login_failures_2020-12-31_countries.dat that was made by watching the output from the
# geolocation service ipapi (https://ipapi.com/) which accepts IPv4 addresses in queries and returns JSON.  Each time I called
# ipapi, I saved the returned JSON in a file geo_locate_IPV4_ADDRESS.json.

geo_locate_dict = {}
for filename in glob.iglob("geo_locate*.json"):
    with open(filename, "rt") as fp:
        geo_locate_rec = json.load(fp)
    if "ip" in geo_locate_rec:
        addr = geo_locate_rec["ip"]     # Both IPv4 and IPv6, if that makes a difference, then look at key "type"
        geo_locate_dict[addr] = {CC: geo_locate_rec[CC], CN: geo_locate_rec[CN] }
    else:
        print("File {filename} was found and it's bad", file=sys.stderr)
        print ( pp.pformat(geo_locate_rec), file=sys.stderr )
        if geo_locate_rec["error"]["type"] == "invalid_access_key":
            os.remove(filename)
            print("Deleted file {filename} and moving on")
        "geo_locate_*.json"
        #012345678901 54321
        # I have to index from the end because an IPv4 address can have as few
        # as 7 chars or as many as 15
        addr = filename[11:-5]
        geo_locate_dict[addr] = {CC: "??", CN: "unknown" }
        # curl http://api.ipapi.com/24.17.21.230?access_key=21462a7f8fd8a59bc2d89a3599ad5775
# pp.pprint( geo_locate_dict )

# noinspection PyShadowingNames
def geo_locate(ip_addr: str, api_key: str ) -> Tuple[str, str]:
    #
    # Avoid going to IPAPI if I can help it
    assert ip_addr not in geo_locate_dict, \
        f"IP address {ip_addr} is *already* in geo_locate_dict in geo_locate"\
        f"geo_locate_dict[{ip_addr}] is {geo_locate_dict[ip_addr]}"

    url =f"http://api.ipapi.com/${ip_addr}?access_key={api_key}"
    r = requests.get(url=url)
    geo_locate_rec = {}
    if r.status_code == 200:
        geo_locate_rec: Dict = r.json()
        if "success" not in geo_locate_rec or geo_locate_rec["success"]:
            with open(f"geo_locate_{ip_addr}.json", "wt") as fp:
                # r.text is already JSON
                print(r.text, file=fp)
    # Didn't get anything useful from IPAPI, so fill known bad values.
    # It isn't obvious that the caller can do a better job of handling the
    # error, so no point in raising an exception
    if CC not in geo_locate_rec or geo_locate_rec[CC] is None:
        geo_locate_rec[CC] = "??"
    if CN not in geo_locate_rec or geo_locate_rec[CN] is None:
        geo_locate_rec[CN] = "unknown"
    return ( geo_locate_rec[CC], geo_locate_rec[CN] )


my_rec = records[34]
print(records[34:46])
for i in range(34,45):
    print(i, "||", records[i])
my_rec = records[42]
print(my_rec)
fields = my_rec.split()
my_datetime=fields[0:3]
my_username = fields[10]
my_address = fields[12]
print(my_datetime, my_username, my_address)

agg_dict = dict()
for i in range(len(records)):
    fields = records[i].split()
    datetime_str = " ".join(fields[0:3])
    if "Failed" != fields[5] or "password" != fields[6]:
        continue
    invalid_user = fields[8] == "invalid"
    if invalid_user:
        if fields[9] != "user":
            raise ValueError(f"fields[9] should be 'user' but it's {fields[9]}")
        else:
            username = fields[10]
            if fields[11] != "from":
                raise ValueError(f"fields[11] should be 'from' but it's actually {fields[11]}")
            else:
                address = fields[12]
    elif fields[9] == "from":
        username = fields[8]
        address = fields[10]
    else:
        raise ValueError(f"fields[9] should be 'from' because fields[8] was not 'invalid', but it's {fields[9]}")
    #
    # print(f"{datetime_str} {username} {' ' if invalid_user else '*'} @ {address} ")
    if address in agg_dict:
        agg_dict[address][US].append(username)
        assert CC in agg_dict[address], f"{CC} not in agg_dict[{address}], it's {agg_dict[address]}"
        assert CN in agg_dict[address], f"{CN} not in agg_dict[{address}], it's {agg_dict[address]}"
    else:
        agg_dict[address] = dict()
        if address in geo_locate_dict:
            country_code, country_name = geo_locate_dict[address][CC], geo_locate_dict[address][CN]
        else:
            country_code, country_name = geo_locate(address, api_key=api_key)
            geo_locate_dict[address] = {CC: country_code, CN: country_name}
        agg_dict[address][US] = [username]
        assert len(
            country_code) == 2, f"country_code should be a string on length 2 but it's {country_name}"
        agg_dict[address][CC] = country_code
        agg_dict[address][CN] = country_name


# agg_dict now has a database of all of the usernames that each address used,
# the country code and country name.
for a in agg_dict.keys():
    pp.pprint(f"{a}: {agg_dict[a]}")

