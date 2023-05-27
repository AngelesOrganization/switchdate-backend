import uvicorn as uvicorn
from fastapi import FastAPI, APIRouter

from src.main.auth.auth_controller import router as auth_router
from src.main.groups.group_controller import router as group_router
from src.main.users.user_controller import router as user_router
from src.main.shifts.shifts_controller import router as shift_router
from src.main.swaps.swap_controller import router as swap_router
from fastapi.middleware.cors import CORSMiddleware

api_router = APIRouter()
api_router.include_router(router=auth_router)
api_router.include_router(router=group_router)
api_router.include_router(router=user_router)
api_router.include_router(router=shift_router)
api_router.include_router(router=swap_router)

app = FastAPI()
app.include_router(api_router)

# Configurar CORS
origins = [
    "http://localhost:3000",  # Permitir solicitudes desde el dominio front-end
    "http://127.0.0.1:3000",  # Permitir solicitudes desde el dominio front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
