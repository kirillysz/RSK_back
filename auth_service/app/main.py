from fastapi import FastAPI
from routes.users_router.router import router as user_router

app = FastAPI(title='FastAPI',description='xxx',docs_url='/docs')


app.include_router(user_router)