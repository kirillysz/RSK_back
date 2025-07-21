import asyncio
from fastapi import FastAPI
from routes.profile_routers.router import router
from services.rabbitmq import consume_user_created_events
from config import settings

app = FastAPI(title='FastAPI',description='xxx',docs_url='/')


app.include_router(router)

app = FastAPI()

@app.on_event("startup")
async def startup():
    
    asyncio.create_task(
        consume_user_created_events(settings.RABBITMQ_URL)
    )