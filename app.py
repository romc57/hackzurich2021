from flask import Flask, render_template, request, url_for
from modules import fitrockr_api, utils, genre_scaler
from datetime import datetime

app = Flask(__name__)

USER_ID = fitrockr_api.get_user_info('new user RC')[0]['id']

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getGenreWeights', methods=["GET"])
def get_genre_weights():
    if request.method == 'GET':
        global USER_ID
        json_obj = utils.load_json_file('data/w.json')
        cur_time = str(datetime.now()).split(' ')[1].split(':')
        cur_time = fitrockr_api.time_to_sec(cur_time[0], cur_time[1], cur_time[2])
        stress_level = fitrockr_api.get_user_stress_level(USER_ID, cur_time)
        if stress_level and stress_level > 0:
            weight_bin = genre_scaler.get_state(stress_level, json_obj['stress_bins'])
        else:
            weight_bin = '1'
        return {'sentiment': json_obj['stress_weights'][str(weight_bin)]}


@app.route('/getStressStatistics', methods=["GET"])
def get_stress_statistics():
    global USER_ID
    cur_date = str(datetime.now()).split(' ')[0]
    stress_records = fitrockr_api.get_user_stress_records(USER_ID, cur_date, cur_date)
    time_stamps = list()
    stress_sum = 0
    record_count = 0
    for record in stress_records:
        start_time = record['startTime']['time']
        stress = record['stressLevelValue']
        if not stress or stress <= 0:
            stress = stress_sum / max(record_count, 1)
        time_stamps.append(["{}T{}:{}:{}Z".format(cur_date, start_time['hour'], start_time['minute'],
                                                  start_time['second']), int(stress)])
        record_count += 1
        stress_sum += stress
    return {'timeStamps': time_stamps, 'averageStress': stress_sum/record_count}


if __name__ == '__main__':
    app.run()
