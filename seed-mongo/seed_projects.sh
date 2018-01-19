#!/bin/sh

sleep 1

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --datafile /mqtt_user.json \
    --ssl False \
    --with-host-prefix True \
    --collection mqtt_user

python3 seed.py \
    --host $MONGO_HOST \
    --db vmq_acl_auth \
    --datafile /project.json \
    --ssl False \
    --with-host-prefix True \
    --collection project
