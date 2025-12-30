from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime, time
from queue import Queue
import subprocess
import time
import os

app = Flask(__name__)
progress_queue = Queue()

_ip:str = "192.168.103.172"
_port:int = 1234

@app.route('/_information')
def display_csv_data() -> render_template:
    return render_template('display_csv.html', data=df_system.to_html())


@app.route('/_project_information')
def display_project_information() -> render_template:
    return render_template('display_project_information.html', data=df_project.to_html())

@app.route("/get")
def get_input_msg() -> render_template:
    return render_template("input_msg.html")

@app.route('/_get_duty_personnel')
def get_updated_duty_personnel() -> str:
    duty_person = get_duty_personnel()
    print(duty_person[0],duty_person[1])
    return duty_person[0]

@app.route('/')
def mainPage() -> render_template:
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host=_ip, port=_port)
