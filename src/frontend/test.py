# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import time
 
from datetime import timedelta
 
# 允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])
 
def allowed_file(filename):
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)

# 静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 
 
@app.route('/upload', methods=['POST', 'GET'])
def message_upload():
    if request.method == 'POST':
        f = request.files['upload_file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({f"error": 1001, "msg": "请检查上传的图片类型, 仅限于{ALLOWED_EXTENSIONS}"})
 
        user_input = request.form.get("选项1")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # # 使用Opencv转换一下图片格式和名称
        # img = cv2.imread(upload_path)
        # cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
 
        return render_template('upload_ok.html',userinput=user_input, _filename = "./images/" + f.filename)
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='192.168.103.172', port=5000, debug=True)