from pyspark.sql import SparkSession
from pyspark.sql.functions import get_json_object, dayofweek, hour, month, year, avg
from pyspark.sql.functions import sum

cluster_seeds = ['localhost:9042', 'localhost:9043']
# initialize the SparkSession

spark = SparkSession \
    .builder \
    .appName("Twitch lives Analyzer") \
    .config("spark.cassandra.connection.host", ','.join(cluster_seeds)) \
    .getOrCreate()

# DF that is cyclically reads events from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "live-data") \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Reconstruct the dataframe from the json string with fields
df = df.select(
    get_json_object(df.value, '$.liveStreamID').alias('liveStreamID'),
    get_json_object(df.value, '$.beginTime').alias('beginTime'),
    get_json_object(df.value, '$.endTime').alias('endTime'),
    get_json_object(df.value, '$.duration').alias('duration'),
    get_json_object(df.value, '$.closeBy').alias('closeBy'),
    get_json_object(df.value, '$.maxLiveViewerCounter').alias('maxLiveViewerCounter'),
    get_json_object(df.value, '$.maxLiveViewerTime').alias('maxLiveViewerTime'),
    get_json_object(df.value, '$.privateLiveStream').alias('privateLiveStream'),
    get_json_object(df.value, '$.receivedLikeCount').alias('receivedLikeCount'),
    get_json_object(df.value, '$.streamerType').alias('streamerType'),
    get_json_object(df.value, '$.isShow').alias('isShow'),
    get_json_object(df.value, '$.cultureGroup').alias('cultureGroup'),
    get_json_object(df.value, '$.streamerID').alias('streamerID'),
    get_json_object(df.value, '$.registerTime').alias('registerTime'),
    get_json_object(df.value, '$.registerCountry').alias('registerCountry'),
    get_json_object(df.value, '$.isContracted').alias('isContracted'),
    get_json_object(df.value, '$.uniqueViewerCount').alias('uniqueViewerCount'),
    get_json_object(df.value, '$.ios').alias('ios'),
    get_json_object(df.value, '$.android').alias('android'),
    get_json_object(df.value, '$.durationGTE5sec').alias('durationGTE5sec'),
    get_json_object(df.value, '$.durationGTE2min').alias('durationGTE2min'),
    get_json_object(df.value, '$.durationGTE10min').alias('liveStreamID'),
    get_json_object(df.value, '$.totalViewerDuration').alias('totalViewerDuration'),
    get_json_object(df.value, '$.avgViewerDuration').alias('avgViewerDuration'),
    get_json_object(df.value, '$.avgStreamJoinDuration').alias('avgStreamJoinDuration'),
    get_json_object(df.value, '$.count').alias('count'),
    get_json_object(df.value, '$.followIncreaseEstimated').alias('followIncreaseEstimated'),
    get_json_object(df.value, '$.receivePointEstimated').alias('receivePointEstimated'),
    get_json_object(df.value, '$.dau').alias('dau'),
    get_json_object(df.value, '$.receiverUserID').alias('receiverUserID'),
    get_json_object(df.value, '$.utcTimestamp').alias('utcTimestamp'),
    get_json_object(df.value, '$.id').alias('id'),
    get_json_object(df.value, '$.userID').alias('userID'),
    get_json_object(df.value, '$.type').alias('type'),
    get_json_object(df.value, '$.giftID').alias('giftID'),
    get_json_object(df.value, '$.point').alias('point'),
    get_json_object(df.value, '$.timestamp').alias('timestamp'),
    get_json_object(df.value, '$.isCanceled').alias('isCanceled'),
    get_json_object(df.value, '$.migration').alias('migration'),
    get_json_object(df.value, '$.isCanceled').alias('isCanceled'),
    get_json_object(df.value, '$.recordID').alias('recordID'),
    get_json_object(df.value, '$.recordPoint').alias('recordPoint'),
    get_json_object(df.value, '$.tradeID').alias('tradeID')
)

# --------------------------------STREAMING ANALYSIS ------------------------------------------------

# 1: Total donations for every hour and day of the week
total_donations = df \
    .withColumn("dayOfTheWeek", dayofweek("utcTimestamp")) \
    .withColumn("hourOfDay", hour("utcTimestamp"))

total_donations = total_donations.groupBy("dayOfTheWeek", "hourOfDay", "country").agg(
    sum("points").alias("totalDonations")).select("dayOfTheWeek", "hourOfDay", "country","totalDonations")

# Start the computation of the query and periodically save the results to Cassandra
total_donations_query = total_donations.writeStream \
    .trigger(processingTime="5 seconds") \
    .option("checkpointLocation", '/tmp/check_point/') \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "AnalyticsKeySpace") \
    .option("table", "Total_Donations") \
    .outputMode("update") \
    .start()

# --------------------------------2---------------------------------------------------------------------
# 2: Donations for every streamer divided by month and year

streamer_df = df \
    .withColumn("month", month("utcTimestamp")) \
    .withColumn("year", year("utcTimestamp"))

streamer_donations = streamer_df.groupBy("streamerID", "year", "month") \
    .agg(sum("points").alias("totalDonations")).select("streamerID", "year", "month", "totalDonations")

# Start the computation of the query and periodically save the results to Cassandra
streamer_donations_query = streamer_donations.writeStream \
    .trigger(processingTime="5 seconds") \
    .option("checkpointLocation", '/tmp/check_point/') \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "AnalyticsKeySpace") \
    .option("table", "Streamer_Analytics_Donations") \
    .outputMode("update") \
    .start()

# --------------------------------3---------------------------------------------------------------------

# 3 avg Followers for every day of the week per streamer
live_df = df.select("liveStreamID",
                    "streamerID",
                    "beginTime",
                    "followIncreaseEstimated") \
    .drop_duplicates() \
    .withColumn("dayOfTheWeek", dayofweek("beginTime")) \
    .groupBy("streamerID", "dayOfTheWeek") \
    .agg(avg("followIncreaseEstimated").alias("avgFollowersAdded")) \
    .select("streamerID", "dayOfTheWeek", "avgFollowersAdded")

# Start the computation of the query and periodically save the results to Cassandra
live_df_query = live_df.writeStream \
    .trigger(processingTime="5 seconds") \
    .option("checkpointLocation", '/tmp/check_point/') \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "AnalyticsKeySpace") \
    .option("table", "Streamer_Analytics_Followers") \
    .outputMode("update") \
    .start()

# --------------------------------4---------------------------------------------------------------------


views_df = df.select("liveStreamID",
                     "streamerID",
                     "maxLiveViewerTime",
                     "maxLiveViewerCount") \
    .drop_duplicates() \
    .withColumn("hourOfTheDay", hour("maxLiveViewerTime")) \
    .groupBy("streamerID", "hourOfTheDay") \
    .agg(avg("maxLiveViewerCount").alias("avgViews")) \
    .select("streamerID", "hourOfTheDay", "avgViews")

# Start the computation of the query and periodically save the results to Cassandra
views_df_query = views_df.writeStream \
    .trigger(processingTime="5 seconds") \
    .option("checkpointLocation", '/tmp/check_point/') \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "AnalyticsKeySpace") \
    .option("table", "Streamer_Analytics_Views") \
    .outputMode("update") \
    .start()

# -----------------------------------------------------------------------------------------------------


# Wait for the terminations of the computations
total_donations_query.awaitTermination()
streamer_donations_query.awaitTermination()
live_df_query.awaitTermination()
views_df_query.awaitTermination()
