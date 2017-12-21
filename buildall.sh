#!/bin/sh

set -ex

cd seed-mongo
docker build -t 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-seed:0.1.2 .
docker push 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-seed:0.1.2
cd -

### Mockson webhooks container

cd app
docker build -t 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-webhooks:latest .
docker push 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-webhooks:latest
cd -
