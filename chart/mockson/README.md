# Mockson IoT

Mock of watson iot

https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

## Steps

### Database seed container

1. `cd seed-mongo`
2. `docker build -t 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-seed:latest .`
3. `docker push 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-seed:latest`

### Mockson webhooks container

1. `cd app`
2. `docker build -t 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-webhooks:latest .`
3. `docker push 871947736413.dkr.ecr.eu-west-2.amazonaws.com/mockson-webhooks:latest`
