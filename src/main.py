#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
from flask import Flask, render_template, request , jsonify, make_response
from werkzeug.utils import secure_filename
from datetime import timedelta

import json
import os
import sys
import time

# 注意：保持你原有的导入路径不变
from backend.weather.api import WeatherInformation as __WeatherInformation
from backend.weather.api import GetCityName as __GetCityName

app = Flask(
    __name__,
    template_folder="./frontend/templates"      
)

# 允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 静态文件缓存过期时间（避免静态资源缓存导致页面不刷新）
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/', methods=['POST', 'GET'])
def main_page():
    return render_template('weather.html')

@app.route('/api/weather/view', methods=['POST', 'GET'])
def get_weather():
    # 1. 兼容前端传递的 adcode 和 city 两种参数名，优先获取有效城市名
    city_name = request.args.get('adcode', None)  # 兼容旧参数名 adcode
    if not city_name:
        city_name = request.args.get('city', None)  # 优先使用标准参数名 city
        # 补充：支持 POST 请求的表单/JSON 参数（提高接口灵活性）
        if request.method == 'POST':
            # 先从表单获取，再从 JSON 数据获取
            form_city = request.form.get('city')
            json_city = request.get_json().get('city') if request.is_json else None
            city_name = form_city or json_city or city_name
    
    # 2. 参数校验：空值兜底（避免传入空字符串导致接口异常）
    if not city_name or city_name.strip() == '':
        city_name = "上海市"  # 兜底默认城市，也可返回错误信息
    else:
        city_name = city_name.strip()  # 去除首尾空格

    # 3. 动态传入城市名称，不再写死（核心：实现根据参数返回对应天气）
    weather_data = __WeatherInformation(city_name)

    # 4. 处理中文显示：关闭 Unicode 转义，确保返回的 JSON 中文正常展示
    weather_json_str = json.dumps(weather_data, ensure_ascii=False)
    resp = make_response(weather_json_str)
    resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return resp

@app.route('/api/weather/get_citys', methods=['POST', 'GET'])
def get_all_weather_citys():
    # 读取城市列表并处理中文显示
    city_list = __GetCityName()
    city_json_str = json.dumps(city_list, ensure_ascii=False)
    resp = make_response(city_json_str)
    resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return resp

@app.route('/upload', methods=['POST', 'GET'])
def message_upload():
    if request.method == 'POST':
        f = request.files['upload_file']
 
        if not (f and allowed_file(f.filename)):
            # 修复字符串格式化问题
            return jsonify({"error": 1001, "msg": f"请检查上传的图片类型, 仅限于{ALLOWED_EXTENSIONS}"})
 
        user_input1 = request.form.get("选项1")
        user_input2 = request.form.get("选项2")
        user_input3 = request.form.get("选项3")
        user_input4 = request.form.get("选项4")
        user_input5 = request.form.get("选项5")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # 确保上传目录存在（避免文件夹不存在导致保存失败）
        upload_dir = os.path.join(basepath, 'frontend/static/images')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        upload_path = os.path.join(upload_dir, secure_filename(f.filename))
        
        f.save(upload_path)
 
        time.sleep(2)
        return jsonify({ "success": True, "message": "上传成功" })
 
    return render_template('upload.html')
 
if __name__ == '__main__':
    # 启动服务（保持你的原有配置）
    app.run(host='192.168.103.172', port=5000, debug=True)