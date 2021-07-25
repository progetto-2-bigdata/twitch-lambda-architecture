#!/bin/bash

# Crea lo schema per Cassandra 1
docker exec -it cassandra1  cqlsh -u cassandra -p cassandra -f /schema.cql
# docker exec cassandra1 cqlsh --username cassandra --password cassandra  -f /schema.cql

# Crea lo schema per Cassandra 2
docker exec -it cassandra2  cqlsh -u cassandra -p cassandra -f /schema.cql
# docker exec cassandra2 cqlsh --username cassandra --password cassandra  -f /schema.cql

# Crea lo schema per Cassandra 3
docker exec -it cassandra3  cqlsh -u cassandra -p cassandra -f /schema.cql
# docker exec cassandra3 cqlsh --username cassandra --password cassandra  -f /schema.cql

# Crea Kafka topic "live-data"
docker exec kafka-stream kafka-topics --create --topic live-data --partitions 1 --replication-factor 3 --if-not-exists --zookeeper zookeeper:2181
