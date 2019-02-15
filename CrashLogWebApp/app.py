from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    index = open("static/index.html").read().decode("utf_8")
    return index


if __name__ == '__main__':
    app.run()
