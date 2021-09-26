import json
from csv import writer


def load_json_file(path):
    with open(path, 'r') as file:
        return json.loads(file.read())


def write_json_file(path, json_dict):
    with open(path, 'w') as file:
        file.write(json.dumps(json_dict))


def append_row_to_csv(path, col_list):
    with open(path, 'a', encoding='utf-8', newline='') as file:
        writer_obj = writer(file)
        writer_obj.writerow(col_list)


def add_to_link_entries(col_list):
    csv_cols = ['date_time', 'sentiment_int']
    if len(col_list) != len(csv_cols):
        return
    append_row_to_csv('data/link_entries.csv', col_list)


def add_to_read_entries(col_list):
    csv_cols = ['date_time', 'sentiment_int']
    if len(col_list) != len(csv_cols):
        return
    append_row_to_csv('read_entries.csv', col_list)


def get_last_csv_row(path):
    with open(path, 'r') as file:
        rows = file.readlines()
        if len(rows) == 0:
            return
        return rows[-1]

def csv_row_to_list(row):
    row = row.split('\n')[0]
    return row.split(',')


def get_last_link_entry():
    return get_last_csv_row('data/link_entries.csv')


def convert_int_to_sentiment(int_sent):
    sent_list = ['Sadness', 'Joy', 'Fear', 'Disgust', 'Anger']
    return sent_list[int_sent - 1]


def time_to_sec(time_str):
    time_str = time_str.split(':')
    time_str[2] = time_str[2].split('.')[0]
    return sum([a * b for a, b in zip([3600, 60, 1], map(int, time_str))])
