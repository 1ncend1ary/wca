#### ---------------------------------
#### ---- Set up database seeder ----:
#### ---------------------------------
FROM mongo:latest

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Import production data into existing database
COPY secret_data.csv /data.csv
CMD mongoimport --host mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $authenticationDatabase  \
      --type csv -d $MONGO_DB -c $MONGO_COLLECTION --headerline --drop --file data.csv

# Import user login/password data
COPY secret_users.csv /users.csv
CMD mongoimport --host mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $authenticationDatabase  \
    --type csv -d $MONGO_DB_USERS -c $MONGO_COLLECTION_USERS --headerline --drop --file users.csv