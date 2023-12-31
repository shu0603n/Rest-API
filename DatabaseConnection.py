import pymysql

class DatabaseConnection:
    def __init__(self):
        # MySQLデータベース接続情報
        self.mysql_host = '127.0.0.1'  # ローカルホスト
        self.mysql_port = 3306
        self.mysql_user = 'xs739875_demo'
        self.mysql_password = 'adminadmin'
        self.mysql_db = 'xs739875_demo'

        self.connection = None

    def connect(self):
        # MySQLへの接続
        self.connection = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
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