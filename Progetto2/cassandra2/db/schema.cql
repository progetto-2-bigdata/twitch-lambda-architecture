//Create keyspace
CREATE KEYSPACE IF NOT EXISTS AnalyticsKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

//Create table
CREATE TABLE IF NOT EXISTS AnalyticsKeySpace.Total_Donations (hourOfTheDay text, dayOfTheWeek text, country text, totalDonations bigint, PRIMARY KEY (hourOfTheDay, dayOfTheWeek, country));

CREATE TABLE IF NOT EXISTS AnalyticsKeySpace.Streamer_Analytics_Donations (streamerID text, year text, month text, totalDonations bigint, PRIMARY KEY (streamerID, year, month);

CREATE TABLE IF NOT EXISTS AnalyticsKeySpace.Streamer_Analytics_Followers (streamerID text, dayOfTheWeek text, avgFollowersAdded bigint, PRIMARY KEY (streamerID, dayOfTheWeek));

CREATE TABLE IF NOT EXISTS AnalyticsKeySpace.Streamer_Analytics_Views (streamerID text, hourOfTheDay text, avgViews bigint,  PRIMARY KEY (streamerID, hourOfTheDay));

CREATE TABLE IF NOT EXISTS AnalyticsKeySpace.Streamer_Analytics_FollowersInCommon (streamer_ID_1 text, streamer_ID_2 text, number_of_users bigint,  PRIMARY KEY (streamer_ID_1, streamer_ID_2));

//Select from table
SELECT * FROM AnalyticsKeySpace.Total_Donations;
SELECT * FROM AnalyticsKeySpace.Streamer_Analytics_Donations;
SELECT * FROM AnalyticsKeySpace.Streamer_Analytics_Followers;
SELECT * FROM AnalyticsKeySpace.Streamer_Analytics_Views;
SELECT * FROM AnalyticsKeySpace.Streamer_Analytics_FollowersInCommon;


