import pandas as pd
from datetime import datetime


def filter_row(row):
    begin_time = row["beginTime"]
    end_time = row["endTime"]
    timestamp = row["utcTimestamp"]

    begin_time = datetime.strptime(begin_time[0:-4], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time[0:-4], '%Y-%m-%d %H:%M:%S')
    timestamp = datetime.strptime(timestamp[0:-4], '%Y-%m-%d %H:%M:%S')
    return begin_time <= timestamp <= end_time


def remove_UTCs(row):
    row["beginTime"] = row["beginTime"][0:-4]
    row["endTime"] = row["endTime"][0:-4]
    row["utcTimestamp"] = row["utcTimestamp"][0:-4]
    row["maxLiveViewerTime"] = row["maxLiveViewerTime"][0:-4]
    return row


def join_datasets(path1: str, path2: str, new_file_path: str):
    # live data
    df1 = pd.read_csv(path1)
    # donations data
    df2 = pd.read_csv(path2)

    new_df = df1.merge(df2, left_on="streamerID", right_on="receiverUserID", suffixes=None)
    m = new_df.apply(filter_row, axis=1)
    df = new_df[m]
    df = df.apply(remove_UTCs, axis=1)

    df.to_csv(new_file_path, index=False)


if __name__ == '__main__':
    join_datasets("data/all_stream_info.csv", "data/points_transaction_log.csv", "data/dataset.csv")
