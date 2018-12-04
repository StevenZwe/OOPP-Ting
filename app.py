from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World! Hello World 3123982748784 Halksdkasjdh as asdhkahsda sdasdasdas'


if __name__ == '__main__':
    app.run()
