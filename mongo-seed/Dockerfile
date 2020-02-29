#### ---------------------------------
#### ---- Set up database seeder ----:
#### ---------------------------------
FROM mongo

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Import data into existing database.
COPY data.csv /data.csv
CMD mongoimport --host mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase "admin"  \
      --type csv -d $MONGO_DB -c $MONGO_COLLECTION --headerline --drop --file data.csv