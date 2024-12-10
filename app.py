from flask import Flask
from app.routes import routes  # 导入 routes



app = Flask(__name__)

# 注册 Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)