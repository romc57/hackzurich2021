from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_genre_weights')
def get_genre_weights():
    return


if __name__ == '__main__':
    app.run()
