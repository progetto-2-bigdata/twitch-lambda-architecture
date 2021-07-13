from kafka import KafkaProducer
import pandas as pd
import time
import json

df = pd.read_csv("data/dataset.csv")

donations = df.values.tolist()

# crea un produttore che si connette alla porta 9092 di localhost
# dove si trova il canale kafka in ascolto
# codifica i messaggi in json
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


# Ctrl + C per bloccare la generazione di eventi
# Ogni 10 secondi vengono pubblicate 100 record di donazioni
while True:
    index = 0
    for donation in donations:
        donation= tuple(donation)
        to_send = {
            'liveStreamID':donation[0],
            'beginTime':donation[1],
            'endTime':donation[2],
            'duration':donation[3],
            'closeBy':donation[4],
            'maxLiveViewerTime': donation[5],
            'privateLiveStream': donation[6],
            'receivedLikeCount': donation[7],
            'streamerType': donation[8],
            'isShow': donation[9],
            'cultureGroup': donation[10],
            'streamerID': donation[11],
            'registerTime': donation[12],
            'registerCountry': donation[13],
            'isContracted': donation[14],
            'uniqueViewerCount': donation[15],
            'ios': donation[16],
            'android': donation[17],
            'durationGTE5sec': donation[18],
            'durationGTE2min': donation[19],
            'durationGTE10min': donation[20],
            'totalViewerDuration': donation[21],
            'avgViewerDuration': donation[22],
            'avgStreamJoinDuration': donation[23],
            'count': donation[24],
            'followIncreaseEstimated': donation[25],
            'receivePointEstimated': donation[26],
            'dau': donation[27],
            'receiverUserID': donation[28],
            'utcTimestamp': donation[29],
            'id': donation[30],
            'userID': donation[31],
            'type': donation[32],
            'giftID': donation[33],
            'point': donation[34],
            'timestamp': donation[35],
            'isCanceled': donation[36],
            'migration': donation[37],
            'recordID': donation[38],
            'recordPoint': donation[39],
            'tradeID': donation[40]
        }
        producer.send('live-data', value=to_send)
        index += 1
        if (index % 100) == 0:
            time.sleep(10)

