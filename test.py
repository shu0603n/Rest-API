# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)
print('サーバー起動！！！！')
@app.route('/')
def index():
    print('/に入っています')
    return 'It works!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
