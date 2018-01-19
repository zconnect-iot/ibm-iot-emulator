#!/bin/sh

sleep 1

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --drop True \
    --datafile /mqtt_user.json \
    --ssl False \
    --collection mqtt_user

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --drop True \
    --datafile /project.json \
    --ssl False \
    --collection project
