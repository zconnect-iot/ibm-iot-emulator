FROM mongo:3.6-jessie

RUN apt-get update && apt-get install python3 python3-pip --no-install-recommends --yes
RUN pip3 install click

COPY seed.py seed_projects.sh /

ONBUILD COPY mqtt_user.json project.json /

CMD /seed_projects.sh
