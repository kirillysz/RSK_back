from fastapi import FastAPI
from app.routes.teams_router.router import router as team_router

app = FastAPI(title='FastAPI',description='xxx',docs_url='/')


app.include_router(team_router)