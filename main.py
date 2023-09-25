from fastapi import FastAPI
from DatabaseSSHConnection import DatabaseSSHConnection

app = FastAPI()
# DatabaseConnectionクラスのインスタンスを作成
db_connection = DatabaseSSHConnection()

# 接続テスト
query = "SELECT * FROM skill"
result = db_connection.execute_query(query)
    
print(result)


@app.on_event("startup")
async def startup_event():
    # アプリケーション起動時にデータベースに接続
    db_connection.connect()

@app.on_event("shutdown")
async def shutdown_event():
    # アプリケーション終了時にデータベース接続を閉じる
    db_connection.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/skill/")
def read_item():
    # SQLクエリを実行
    query = "SELECT * FROM skill"
    result = db_connection.execute_query(query)
    
    # 結果をJSON形式で返す
    return {result}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}





# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
