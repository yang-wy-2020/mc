from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制
app.config['DATA_FILE'] = 'products.json'

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 加载商品数据
def load_products():
    try:
        if os.path.exists(app.config['DATA_FILE']):
            with open(app.config['DATA_FILE'], 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return []

# 保存商品数据
def save_products(products_data):
    with open(app.config['DATA_FILE'], 'w', encoding='utf-8') as f:
        json.dump(products_data, f, ensure_ascii=False, indent=2)

# 全局商品列表（从文件加载）
products = load_products()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_product():
    global products  # 声明使用全局变量
    try:
        # 获取表单数据
        product_type = request.form.get('product_type', '').strip()
        product_name = request.form.get('product_name', '').strip()
        price = request.form.get('price', '0').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        stock = request.form.get('stock', '0').strip()
        brand = request.form.get('brand', '').strip()
        
        # 验证必要字段
        if not product_name or not product_type or not price:
            flash('请填写商品名称、类型和价格', 'error')
            return redirect(url_for('index'))
        
        # 验证价格和库存为数字
        try:
            price_float = float(price)
            stock_int = int(stock) if stock else 0
        except ValueError:
            flash('价格和库存必须是数字', 'error')
            return redirect(url_for('index'))
        
        # 处理文件上传
        image_url = None
        if 'product_image' in request.files:
            file = request.files['product_image']
            if file and file.filename != '' and allowed_file(file.filename):
                # 生成安全的文件名
                filename = secure_filename(file.filename)
                # 添加UUID防止重名
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_url = f"uploads/{unique_filename}"
        
        # 生成商品ID
        if products:
            product_id = max(p['id'] for p in products) + 1
        else:
            product_id = 1
        
        # 创建商品对象
        product = {
            'id': product_id,
            'product_type': product_type,
            'product_name': product_name,
            'price': price_float,
            'category': category,
            'description': description,
            'stock': stock_int,
            'brand': brand,
            'image_url': image_url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 添加到商品列表
        products.append(product)
        save_products(products)
        
        flash('商品信息提交成功！', 'success')
        return redirect(url_for('product_detail', product_id=product['id']))
        
    except Exception as e:
        flash(f'提交失败: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('商品不存在', 'error')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

@app.route('/products')
def product_list():
    return render_template('product_list.html', products=products)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products  # 声明使用全局变量
    try:
        product = next((p for p in products if p['id'] == product_id), None)
        
        if not product:
            flash('商品不存在', 'error')
            return redirect(url_for('product_list'))
        
        # 删除商品图片文件（如果存在）
        if product.get('image_url'):
            image_path = os.path.join('static', product['image_url'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # 从列表中移除商品
        products = [p for p in products if p['id'] != product_id]
        save_products(products)
        
        flash(f'商品 "{product["product_name"]}" 已成功删除', 'success')
        return redirect(url_for('product_list'))
        
    except Exception as e:
        flash(f'删除失败: {str(e)}', 'error')
        return redirect(url_for('product_list'))

@app.route('/edit_product/<int:product_id>')
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('商品不存在', 'error')
        return redirect(url_for('product_list'))
    return render_template('edit_product.html', product=product)

@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    global products  # 声明使用全局变量
    try:
        product = next((p for p in products if p['id'] == product_id), None)
        
        if not product:
            flash('商品不存在', 'error')
            return redirect(url_for('product_list'))
        
        # 更新商品信息
        product['product_type'] = request.form.get('product_type', '').strip()
        product['product_name'] = request.form.get('product_name', '').strip()
        product['price'] = float(request.form.get('price', '0').strip())
        product['category'] = request.form.get('category', '').strip()
        product['description'] = request.form.get('description', '').strip()
        product['stock'] = int(request.form.get('stock', '0').strip())
        product['brand'] = request.form.get('brand', '').strip()
        product['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 处理新的图片上传
        if 'product_image' in request.files:
            file = request.files['product_image']
            if file and file.filename != '' and allowed_file(file.filename):
                # 删除旧的图片文件
                if product.get('image_url'):
                    old_image_path = os.path.join('static', product['image_url'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # 保存新图片
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                product['image_url'] = f"uploads/{unique_filename}"
        
        save_products(products)
        flash('商品信息更新成功！', 'success')
        return redirect(url_for('product_detail', product_id=product_id))
        
    except Exception as e:
        flash(f'更新失败: {str(e)}', 'error')
        return redirect(url_for('edit_product', product_id=product_id))

@app.route('/batch_delete', methods=['POST'])
def batch_delete():
    global products  # 在函数开头声明
    try:
        # 获取要删除的商品ID列表
        product_ids = request.form.getlist('product_ids')
        if not product_ids:
            flash('请选择要删除的商品', 'error')
            return redirect(url_for('product_list'))
        
        # 转换为整数列表
        product_ids = [int(id) for id in product_ids]
        
        deleted_count = 0
        # 使用新的列表来存储不会被删除的商品
        new_products = []
        
        for product in products:
            if product['id'] in product_ids:
                # 删除商品图片文件
                if product.get('image_url'):
                    image_path = os.path.join('static', product['image_url'])
                    if os.path.exists(image_path):
                        os.remove(image_path)
                deleted_count += 1
            else:
                new_products.append(product)
        
        # 更新全局products变量
        products = new_products
        save_products(products)
        flash(f'成功删除 {deleted_count} 个商品', 'success')
        return redirect(url_for('product_list'))
        
    except Exception as e:
        flash(f'批量删除失败: {str(e)}', 'error')
        return redirect(url_for('product_list'))

@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def api_delete_product(product_id):
    """API接口：删除商品"""
    global products  # 声明使用全局变量
    try:
        product = next((p for p in products if p['id'] == product_id), None)
        
        if not product:
            return jsonify({'success': False, 'error': '商品不存在'}), 404
        
        # 删除商品图片文件（如果存在）
        if product.get('image_url'):
            image_path = os.path.join('static', product['image_url'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # 从列表中移除商品
        products = [p for p in products if p['id'] != product_id]
        save_products(products)
        
        return jsonify({'success': True, 'message': '商品删除成功'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products')
def get_products_api():
    return jsonify({'products': products})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, host="192.168.103.172", port=5000)