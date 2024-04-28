from fastapi import FastAPI, APIRouter, Response
from .auth_service.router import router as reg_user_router
from .palette_servise.router import router as palette_router
from .color_servise.router import router as color_router


app = FastAPI()


@app.get(
    "/healthcheck",
    # include_in_schema=False
    tags=["servise"],
    include_in_schema=False,
)
async def healthcheck() -> dict:
    """just for check server"""
    return {"status": "ok"}


v1_root_router = APIRouter()
v1_root_router.include_router(reg_user_router, prefix="/user", tags=["user"])
v1_root_router.include_router(palette_router, prefix="/palette", tags=["palette"])
v1_root_router.include_router(color_router, prefix="/palette", tags=["color"])
app.include_router(v1_root_router, prefix="/v1")

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, proxy_headers=True)
