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
    start_consumer()
    asyncio.create_task(
        consume_user_created_events(settings.RABBITMQ_URL)
    )

async def start_consumer():
    while True:
        try:
            await consume_user_created_events(settings.RABBITMQ_URL)
        except Exception as e:
            print(f"Consumer error: {e}, retrying in 5s...")
            await asyncio.sleep(5)

asyncio.create_task(start_consumer())