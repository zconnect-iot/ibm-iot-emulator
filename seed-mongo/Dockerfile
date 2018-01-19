FROM mongo:3.6-jessie

RUN apt-get update && apt-get install locales python3 python3-pip --no-install-recommends --yes
RUN pip3 install click

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

COPY seed.py seed_projects.sh /

COPY project.json /
COPY mqtt_user.json /
ENV MONGO_HOST=mongodb

CMD /seed_projects.sh
