FROM mongo:3.6

ONBUILD COPY mqtt_user.json project.json .

COPY seed_projects.sh .

CMD seed_projects.sh
