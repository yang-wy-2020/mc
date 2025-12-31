#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
from flask import Flask, render_template, request ,jsonify
from werkzeug.utils import secure_filename
import os, sys, time

 
from datetime import timedelta

from backend.weather.api import WeatherInformation as GetWeatherInfo

# 允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(
    __name__,
    template_folder="./frontend/templates"      
)

# 静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 

@app.route('/', methods=['POST', 'GET'])
def main_page():
    return render_template('weather.html')

@app.route('/api/weather', methods=['POST', 'GET'])
def get_weather():
    weather = GetWeatherInfo("上海市")
    return jsonify(weather)

@app.route('/upload', methods=['POST', 'GET'])
def message_upload():
    if request.method == 'POST':
        f = request.files['upload_file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({f"error": 1001, "msg": "请检查上传的图片类型, 仅限于{ALLOWED_EXTENSIONS}"})
 
        user_input1 = request.form.get("选项1")
        user_input2 = request.form.get("选项2")
        user_input3 = request.form.get("选项3")
        user_input4 = request.form.get("选项4")
        user_input5 = request.form.get("选项5")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'frontend/static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # print(
        #     user_input1,
        #     user_input2,
        #     user_input3,
        #     user_input4,
        #     user_input5
        # )
        time.sleep(2)
        return jsonify({ "success": True, "message": "上传成功" })
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='192.168.103.172', port=5000, debug=True)