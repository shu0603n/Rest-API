from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
import paramiko
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)
CORS(app)

# SSH接続情報
ssh_host = 'sv14591.xserver.jp'  # SSHホスト名
ssh_port = 10022  # SSHポート番号
ssh_username = 'xs739875'  # SSHユーザー名
ssh_key_file = './xs739875.key'  # 秘密鍵ファイルのパス

# MySQLデータベース接続情報
mysql_host = '127.0.0.1'  # ローカルホスト（SSHトンネルを介して接続）
mysql_port = 3306  # MySQLポート番号
mysql_user = 'xs739875_demo'  # MySQLユーザーID
mysql_password = 'adminadmin'  # MySQLパスワード
mysql_db = 'xs739875_demo'

# SSH秘密鍵の設定
ssh_key = paramiko.RSAKey.from_private_key_file(ssh_key_file)

# SSHトンネルの設定
with SSHTunnelForwarder(
    (ssh_host, ssh_port),  # SSHサーバーのホストとポート
    ssh_username=ssh_username,
    ssh_pkey=ssh_key,  # SSH秘密鍵を指定
    remote_bind_address=(mysql_host, mysql_port)  # MySQLサーバーのホストとポート
) as tunnel:
    # MySQLへの接続
    conn = pymysql.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=mysql_user,
        passwd=mysql_password,
        db=mysql_db
    )

    # SQLAlchemyのセットアップ
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}:{tunnel.local_bind_port}/{mysql_db}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app, session_options={"autocommit": True})
# モデルの定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)



# # SSH接続情報
# ssh_host = 'sv14591.xserver.jp'  # SSHホスト名
# ssh_port = 10022  # SSHポート番号
# ssh_username = 'xs739875'  # SSHユーザー名
# ssh_key_file = 'xs739875.key'  # 秘密鍵ファイルのパス

# # MySQLデータベース接続情報
# mysql_host = '127.0.0.1'  # ローカルホスト（SSHトンネルを介して接続）
# mysql_port = 3306  # MySQLポート番号
# mysql_user = 'xs739875_demo'  # MySQLユーザーID
# mysql_password = 'adminadmin'  # MySQLパスワード
# mysql_db = 'xs739875_demo'

# # SSHクライアントを作成
# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# try:
#     # 秘密鍵を指定してSSH接続
#     ssh_key = paramiko.RSAKey(filename=ssh_key_file)
#     ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, pkey=ssh_key)

#     # SSHトンネルを作成
#     ssh_transport = ssh_client.get_transport()
#     mysql_tunnel = ssh_transport.open_channel('direct-tcpip', (mysql_host, mysql_port), (mysql_host, mysql_port))

#     # MySQL接続を設定
#     pymysql_conn = pymysql.connect(host=mysql_tunnel, user=mysql_user, password=mysql_password, db=mysql_db)

    # MySQLクエリを実行するなどの操作を行うことができます
    # db = SQLAlchemy(app)

# except paramiko.AuthenticationException as auth_error:
#     print(f"SSH認証エラー: {auth_error}")
# except Exception as e:
#     print(f"SSH接続エラー: {e}")
    

# except paramiko.AuthenticationException as auth_error:
#     print(f"SSH認証エラー1: {auth_error}")
# except Exception as e:
#     print(f"SSH接続エラー2: {e}")

if __name__ == '__main__':
    app.run(debug=True)
    
# データベースモデルを定義
class Technic(db.Model):
    technic_id = db.Column(db.Integer, primary_key=True)
    technic_name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, technic_name):  # 属性名を修正
        self.technic_name = technic_name  # 属性名を修正

# ルート定義
@app.route('/')
def get_user():
    # Userテーブルからデータを取得
    technics = Technic.query.all()
    
    # データをJSON形式に変換して正しくエンコード
    technic_list = []
    for technic in technics:
        technic_data = {
            'technic_id': technic.technic_id,
            'technic_name': technic.technic_name
        }
        technic_list.append(technic_data)
    
    # jsonifyを使ってJSONレスポンスを返す
    return jsonify(technic_list)

@app.route('/test')
def test():
    print('test')
    return "test"

if __name__ == '__main__':
    with app.app_context():
        # データベース初期化とアプリケーションの実行
        db.create_all()
    app.run(debug=True)