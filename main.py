from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI()

# データをメモリ上に保存する辞書 { 10: { ... }, 11: { ... } }
bingo_data_store = {}


@app.get("/", response_class=HTMLResponse)
async def get_index():
  if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
      return f.read()
  raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/view", response_class=HTMLResponse)
async def get_viewer():
  if os.path.exists("viewer.html"):
    with open("viewer.html", "r", encoding="utf-8") as f:
      return f.read()
  raise HTTPException(status_code=404, detail="viewer.html not found")


@app.post("/api/upload")
async def upload_data(id: int = Query(...), data: dict = None):
  if not id:
    raise HTTPException(status_code=400, detail="ID parameter is required")
  bingo_data_store[id] = data
  return {"status": "success", "id": id}


@app.get("/api/get")
async def get_data(id: int = Query(...)):
  if id in bingo_data_store:
    return bingo_data_store[id]
  raise HTTPException(status_code=404, detail=f"No data found for ID: {id}")


@app.get("/api/get_all")
async def get_all_data():
  """0〜99すべての保存データを一括返却"""
  return bingo_data_store

@app.delete("/api/delete")
async def delete_data(id: int = Query(...)):
  """指定されたIDのデータを削除"""
  if id in bingo_data_store:
    del bingo_data_store[id]
    return {"status": "deleted", "id": id}
  return {"status": "not_found", "id": id}

@app.get("/lottery", response_class=HTMLResponse)
async def get_lottery():
  """'/lottery' で lottery.html を返す"""
  if os.path.exists("lottery.html"):
    with open("lottery.html", "r", encoding="utf-8") as f:
      return f.read()
  raise HTTPException(status_code=404, detail="lottery.html not found")

if __name__ == "__main__":
  import uvicorn

  port = int(os.environ.get("PORT", 8000))
  uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)