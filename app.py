from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import routes  # 导入 routes

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 注册 Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)