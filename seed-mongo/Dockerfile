FROM mongo:3.6

COPY acl.json /acl.json
ENV MONGO_HOST=mongodb://mongodb
CMD sleep 5 \
	&& mongo --host $MONGO_HOST \
	--eval 'db = db.getSiblingDB("vernemq"); db.vmq_acl_auth.drop();' \
	&& mongoimport --host $MONGO_HOST --collection vmq_acl_auth --db vernemq \
	--type json --file /acl.json --jsonArray
