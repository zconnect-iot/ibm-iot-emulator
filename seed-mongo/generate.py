#!/usr/bin/env python

import bcrypt
import json

project = "abc123"

def pwhash(string):
    return bcrypt.hashpw(string.encode("utf8"), bcrypt.gensalt(prefix=b"2a")).decode("utf8")

data = [
    {
        "username": "v1:pid123:aircon:0xbeef",
        "passhash": pwhash("abc"),
        "client_id": "fk4opgk4pokwep4otk490tk34t",
    },
]

# TODO
# call seed() so we dont have to do this

with open("acl.json", "w") as ofile:
    ofile.write(json.dumps(data, indent=2))
