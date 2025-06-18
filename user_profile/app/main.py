from fastapi import FastAPI
from routes.profile_routers.router import router
app = FastAPI(title='FastAPI',description='xxx',docs_url='/')


app.include_router(router)