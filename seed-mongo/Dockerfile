FROM mongo:3.6-jessie

RUN apk update && apk add python3

RUN pip3 install click bcrypt

COPY seed_projects.sh .

CMD seed_projects.sh
