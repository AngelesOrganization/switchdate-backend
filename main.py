import uvicorn
from fastapi import FastAPI

from presentation.controllers import group_controller

app = FastAPI()
app.include_router(group_controller.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
