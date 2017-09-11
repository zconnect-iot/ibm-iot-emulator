FROM mongo:latest

COPY acl.json /acl.json
CMD sleep 5 \
	&& mongo --host $MONGO_HOST \
	--eval 'db = db.getSiblingDB("vernemq"); db.vmq_acl_auth.drop();' \
	&& mongoimport --host $MONGO_HOST --collection vmq_acl_auth --db vernemq\
	--type json --file /acl.json --jsonArray
