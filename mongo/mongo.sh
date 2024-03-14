#!/usr/bin/env bash

docker run --rm --name mongo-db  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
  -e MONGO_INITDB_ROOT_PASSWORD=thisIsVerySecret \
  -v /Users/ukekeilele/Desktop/Coding/Python/database/db:/data/db \
  mongo
