#!/bin/sh

set -ex

TAG=0.3.21
# BASEREPO=871947736413.dkr.ecr.eu-west-2.amazonaws.com/
BASEREPO=871947736413.dkr.ecr.eu-west-2.amazonaws.com/

cd seed-mongo
docker build -t ${BASEREPO}mockson-seed:${TAG} .
# docker push ${BASEREPO}mockson-seed:${TAG}
cd -

### Mockson webhooks container

cd app
docker build -t ${BASEREPO}mockson-webhooks:${TAG} .
# docker push ${BASEREPO}mockson-webhooks:${TAG}
cd -
