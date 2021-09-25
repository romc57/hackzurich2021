from flask import Flask, render_template
from modules import fitrockr_api

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_genre_weights')
def get_genre_weights():
    user = fitrockr_api.get_user_info('new user RC')  # Query user named Rom
    user_id = user[0]['id']
    return 'Mira stress: {}'.format(fitrockr_api.get_user_stress_records(user_id, fitrockr_api.time_to_sec('10', '12', '00')))


if __name__ == '__main__':
    app.run()
