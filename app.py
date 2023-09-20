import pymysql
import paramiko
from sshtunnel import SSHTunnelForwarder

class DatabaseConnection:
    def __init__(self):
        # SSH接続情報
        self.ssh_host = 'sv14591.xserver.jp'
        self.ssh_port = 10022
        self.ssh_username = 'xs739875'
        self.ssh_key_file = './.ssh/xs739875.key'

        # MySQLデータベース接続情報
        self.mysql_host = '127.0.0.1'  # ローカルホスト（SSHトンネルを介して接続）
        self.mysql_port = 3306
        self.mysql_user = 'xs739875_demo'
        self.mysql_password = 'adminadmin'
        self.mysql_db = 'xs739875_demo'

        self.ssh_key = paramiko.RSAKey.from_private_key_file(self.ssh_key_file)
        self.tunnel = None
        self.connection = None

    def connect(self):
        # SSHトンネルの設定
        self.tunnel = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_username,
            ssh_pkey=self.ssh_key,
            remote_bind_address=(self.mysql_host, self.mysql_port)
        )
        self.tunnel.start()

        # MySQLへの接続
        self.connection = pymysql.connect(
            host='localhost',
            port=self.tunnel.local_bind_port,
            user=self.mysql_user,
            passwd=self.mysql_password,
            db=self.mysql_db
        )

    def execute_query(self, query):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def execute_update(self, query):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()  # データベースの変更をコミット
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
        if self.tunnel:
            self.tunnel.stop()

# Flaskアプリケーション
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_skill_data():
    try:
        db = DatabaseConnection()
        query = "SELECT * FROM skill"
        result_data = db.execute_query(query)
        db.close()
        return jsonify(result_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_skill', methods=['POST'])
def update_skill():
    try:
        data = request.json
        if 'query' in data:
            query = data['query']
            db = DatabaseConnection()
            db.execute_update(query)
            db.close()
            return jsonify({'message': 'Update successful'})
        else:
            return jsonify({'error': 'Query is required in the request body'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
