from flask import Flask, render_template
import mysql.connector as mydb

# コネクションの作成
connector = mydb.connect(
host='MySQLが動いているサーバー',
user='MySQLユーザ',
password='パスワード',
database='データベース名',
charset="utf8"
)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route("/hello")
def hello():
    title="FlaskをレンタルサーバXserverで利用する!"
    subtitle="データベースmySQLのInsert,Update,Selectを実行する"
    return render_template('hello.html', title=title,subtitle=subtitle)

@app.route("/select")
def select():
    cursor = connector.cursor()
    sql = "SELECT id, __name__, age FROM kaiin_table WHERE id=103"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        return "id：" + str(row[0]) + "　　name：" + str(row[1]) + "さん　　age：" + str(row[2])
    cursor.close()
    connector.close()

if __name__ == "main":
    app.run(host='0.0.0.0')