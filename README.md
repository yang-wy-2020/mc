# 智能穿搭助手 / Smart Outfit Assistant

## 项目简介 / Project Introduction

智能穿搭助手是一个基于Flask框架的Web应用，通过AI图像识别技术和个性化推荐算法，为用户提供个性化的服装搭配建议。系统能够根据用户的身材特征、个人喜好、当前天气条件等因素，智能推荐最适合的穿搭方案。

Smart Outfit Assistant is a Flask-based web application that provides personalized clothing recommendations using AI image recognition technology and personalized recommendation algorithms. The system intelligently recommends the most suitable outfit combinations based on user's body characteristics, personal preferences, and current weather conditions.

## 功能特性 / Features

- **智能穿搭推荐**：基于用户身材特征和个人喜好的个性化搭配建议
- **天气适配**：集成天气API，根据当前天气推荐适合的穿搭
- **图片识别**：自动识别用户上传的衣物图片并分类
- **移动优先**：专为移动设备优化的响应式界面设计
- **数据库管理**：SQLite数据库存储用户信息和衣物数据

- **Smart Outfit Recommendation**: Personalized outfit suggestions based on user's body characteristics and preferences
- **Weather Adaptation**: Integrate weather API to recommend outfits suitable for current weather
- **Image Recognition**: Automatically recognize and categorize uploaded clothing images
- **Mobile First**: Responsive interface design optimized for mobile devices
- **Database Management**: SQLite database for storing user information and clothing data

## 技术栈 / Tech Stack

- **后端框架**: Flask
- **前端技术**: HTML5, CSS3, JavaScript, Bootstrap
- **图像处理**: OpenCV, Pillow
- **机器学习**: TensorFlow/Keras 或 PyTorch (用于图像识别)
- **数据库**: SQLite
- **第三方服务**: 天气API (如OpenWeatherMap)

- **Backend Framework**: Flask
- **Frontend Technologies**: HTML5, CSS3, JavaScript, Bootstrap
- **Image Processing**: OpenCV, Pillow
- **Machine Learning**: TensorFlow/Keras or PyTorch (for image recognition)
- **Database**: SQLite
- **Third-party Services**: Weather API (such as OpenWeatherMap)

## 安装说明 / Installation Instructions

1. 克隆项目到本地：
   ```bash
   git clone <repository-url>
   cd smart-outfit-assistant
   ```

2. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. 初始化数据库：
   ```bash
   python init_db.py
   ```

4. 运行应用：
   ```bash
   python app.py
   ```

1. Clone the project to your local machine:
   ```bash
   git clone <repository-url>
   cd smart-outfit-assistant
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## 使用说明 / Usage Guide

1. 启动应用后，在浏览器中访问 `http://localhost:5000`
2. 注册账户或直接登录
3. 上传个人照片和衣柜中的衣物图片
4. 系统将自动分析并推荐合适的穿搭组合
5. 可以保存喜欢的搭配方案或分享给朋友

1. After starting the application, visit `http://localhost:5000` in your browser
2. Register an account or log in directly
3. Upload personal photos and clothing images from your wardrobe
4. The system will automatically analyze and recommend suitable outfit combinations
5. You can save favorite outfit combinations or share them with friends

## 项目结构 / Project Structure

```
smart-outfit-assistant/
│
├── app.py                 # 主应用程序入口
├── init_db.py            # 数据库初始化脚本
├── requirements.txt      # 项目依赖列表
├── static/              # 静态文件 (CSS, JS, 图片)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # HTML模板文件
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── models/              # 数据模型定义
│   └── user_model.py
├── utils/               # 工具函数
│   └── image_processor.py
└── uploads/             # 用户上传文件存储目录
```

```
smart-outfit-assistant/
│
├── app.py                 # Main application entry point
├── init_db.py            # Database initialization script
├── requirements.txt      # Project dependencies list
├── static/              # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # HTML template files
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── models/              # Data model definitions
│   └── user_model.py
├── utils/               # Utility functions
│   └── image_processor.py
└── uploads/             # User uploads storage directory
```

## 移动端适配 / Mobile Adaptation

本项目采用移动端优先的设计策略，确保在各种尺寸的移动设备上都能提供良好的用户体验。界面设计考虑了触控交互的便利性，并对响应式布局进行了优化。

This project adopts a mobile-first design strategy, ensuring a good user experience on various sizes of mobile devices. The interface design considers the convenience of touch interaction and optimizes responsive layout.

## API接口 / API Endpoints

- `GET /` - 首页
- `POST /upload` - 上传图片
- `GET /recommendations` - 获取穿搭推荐
- `POST /login` - 用户登录
- `POST /register` - 用户注册

- `GET /` - Homepage
- `POST /upload` - Upload images
- `GET /recommendations` - Get outfit recommendations
- `POST /login` - User login
- `POST /register` - User registration

## 贡献指南 / Contribution Guidelines

欢迎提交Issue和Pull Request来改进本项目。请遵循以下步骤：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

Welcome to submit Issues and Pull Requests to improve this project. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 许可证 / License

本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 致谢 / Acknowledgments

- 感谢所有为本项目做出贡献的开发者
- 特别感谢使用的开源库和框架的维护者们
- 感谢用户反馈和建议，帮助我们不断改进产品

- Thanks to all developers who contributed to this project
- Special thanks to the maintainers of open-source libraries and frameworks used
- Appreciate user feedback and suggestions that help us continuously improve the product