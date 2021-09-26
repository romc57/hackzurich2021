from flask import Flask, render_template, request, url_for, redirect
from modules import fitrockr_api, utils, genre_scaler, like_update
from datetime import datetime
from flask_cors import CORS
from pytz import timezone

app = Flask(__name__)
CORS(app)

USER_ID = fitrockr_api.get_user_info('new user RC')[0]['id']

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/getGenreWeights', methods=["GET"])
def get_genre_weights():
    if request.method == 'GET':
        global USER_ID
        json_obj = utils.load_json_file('data/weights.json')
        cur_time = utils.time_to_sec(str(datetime.now(timezone('Europe/Zurich'))).split(' ')[1])
        stress_level = fitrockr_api.get_user_stress_level(USER_ID, cur_time)
        if stress_level and stress_level > 0:
            weight_bin = genre_scaler.get_state(stress_level, json_obj['stress_bins'])
        else:
            weight_bin = '1'
        return {'sentiment': genre_scaler.get_weights(json_obj['stress_weights'][str(weight_bin)])}


@app.route('/getStressStatistics', methods=["GET"])
def get_stress_statistics():
    global USER_ID
    cur_date = str(datetime.now(timezone('Europe/Zurich'))).split(' ')[0]
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


@app.route('/addLike/<article_id>', methods=['POST'])
def like(article_id):
    last_link = utils.csv_row_to_list(utils.get_last_link_entry())[1]
    like_update.update_graph_by_like(int(article_id), str(last_link))
    return redirect(request.referrer)


@app.route('/wasClicked/<sentiment_id>', methods=['POST'])
def link_was_clicked(sentiment_id):
    utils.add_to_link_entries([str(datetime.now(timezone('Europe/Zurich'))), sentiment_id])
    return redirect(request.referrer)


@app.route('/getArticleGraph/<id>', methods=['GET'])
def get_article_gragh(id):
    return utils.load_json_file('data/articles_data_reduced.txt')[id]


@app.route('/justRead', methods=['POST'])
def read():
    global USER_ID
    prev_click = utils.csv_row_to_list(utils.get_last_link_entry())
    date = prev_click[0].split(' ')[0]
    time_in_sec = utils.time_to_sec(prev_click[0].split(' ')[1])
    prev_stress = fitrockr_api.get_user_stress_level(USER_ID, time_in_sec, date)
    time_in_sec = utils.time_to_sec(str(datetime.now(timezone('Europe/Zurich'))).split(' ')[1])
    cur_stress = fitrockr_api.get_user_stress_level(USER_ID, time_in_sec)
    w_json = utils.load_json_file('data/weights.json')
    scores = genre_scaler.update_score(prev_stress, cur_stress, prev_click[1], w_json['stress_bins'], w_json['stress_weights'])
    w_state = genre_scaler.get_state(prev_click[1], w_json['stress_bins'])
    w_json['stress_weights'][str(w_state)] = scores
    utils.write_json_file('data/weights.json', w_json)
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
