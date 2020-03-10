#### ---------------------------------
#### ---- Set up database seeder ----:
#### ---------------------------------
FROM mongo

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Import data into existing database.
COPY data.csv /data.csv
CMD mongoimport --host mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase "admin"  \
      --type csv -d $MONGO_DB -c $MONGO_COLLECTION --headerline --drop --file data.csv

# Import password and login info
COPY users.csv /users.csv
CMD mongoimport --host mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase "admin"  \
    --type csv -d $MONGO_DB_USERS -c $MONGO_COLLECTION_USERS --headerline --drop --file users.csv