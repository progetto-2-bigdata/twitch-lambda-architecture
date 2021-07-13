echo Starting infrastructure...

docker-compose up 

./init.sh

python3 kafka-producer/producer.py

docker exec spark-master /spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 --master spark://localhost:7077 spark-streaming-processor/streaming_processor.py

