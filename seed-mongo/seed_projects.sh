#!/bin/sh

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --datafile mqtt_user.json \
    --collection mqtt_user

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --datafile project.json \
    --collection project
