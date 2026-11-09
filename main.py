from fastapi import FastAPI

from user_operations.auth import router

app = FastAPI()
app.include_router(router)
