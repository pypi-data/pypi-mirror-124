from datetime import datetime
import os,sys,math
import json
from flask import Flask, request, render_template
from . import client

app = Flask(__name__)
mdclient = client.Client("127.0.0.1", 23456)
mdclient.connect()

@app.route('/get', methods=["GET"])
def get():
    data_type = request.args.get('data_type') or ""
    symbol = request.args.get('symbol') or ""
    end_timestamp = request.args.get('end_timestamp') or ""

    res = mdclient.get(symbol.encode("utf-8"), data_type.encode("utf-8"), end_timestamp.encode("utf-8"))
    return json.dumps(res)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4001)