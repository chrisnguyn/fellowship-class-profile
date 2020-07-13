from flask import Flask
app = Flask(__name__)


@app.route('/')
def goodbye_world():
    return 'Au revoir, world!'
