#!/bin/sh

set -ex

BASEREPO=871947736413.dkr.ecr.eu-west-2.amazonaws.com/

cd seed-mongo
docker build -t ${BASEREPO}mockson-seed:0.1.2 .
docker push ${BASEREPO}mockson-seed:0.1.2
cd -

### Mockson webhooks container

cd app
docker build -t ${BASEREPO}mockson-webhooks:latest .
docker push ${BASEREPO}mockson-webhooks:latest
cd -
