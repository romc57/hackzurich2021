import json
from csv import writer

def load_json_file(path):
    with open(path, 'r') as file:
        return json.loads(file.read())


def write_json_file(path, json_dict):
    with open(path, 'w') as file:
        file.write(json.dumps(json_dict))


def append_row_to_csv(path, col_list):
    with open(path, 'a') as file:
        writer_obj = writer(file)
        writer_obj.writerow(col_list)
        file.close()


def add_to_link_entries():
    pass

def add_to_read_entries():
    pass

def convert_int_to_sentiment(int_sent):
    sent_list = ['Sadness', 'Joy', 'Fear', 'Disgust', 'Anger']
    return sent_list[int_sent - 1]