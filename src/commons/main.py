import uvicorn as uvicorn
from fastapi import FastAPI

from src.auth.auth_controller import router as auth_router
from src.groups.group_controller import router as group_router
from src.users.user_controller import router as user_router
from src.shifts.shifts_controller import router as shift_router

app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=group_router)
app.include_router(router=user_router)
app.include_router(router=shift_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
