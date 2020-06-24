#### ---------------------------------
#### ---- Set up database seeder ----:
#### ---------------------------------
FROM mongo:latest

LABEL maintainer="alexseliverstov@yahoo.com"

# Import production and user login/password data into existing database

CMD mongoimport --host mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase "$authenticationDatabase"  \
      --type csv -d "$MONGO_DB" -c "$MONGO_COLLECTION" --headerline --drop --file "$SECRET_DATA" && \
    mongoimport --host mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase "$authenticationDatabase"  \
    --type csv -d "$MONGO_DB_USERS" -c "$MONGO_COLLECTION_USERS" --headerline --drop --file "$SECRET_USERS"
