from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def test():
    return {"message": "OK"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")

