'''
启动入口。host/port/debug 从环境变量读取（见 .env.example），默认 127.0.0.1:8088、debug=True。
前后端传输与数据库存储的密码建议加密，当前为开发测试用途未做加密。
'''
from app import app
from app.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
