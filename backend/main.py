from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME, VERSION
from routes.search import router_api

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

# Allow the frontend to talk to the backend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later we'll restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router_api)


@app.get("/")
async def root():
    return {
        "status": "online",
        "project": APP_NAME,
        "version": VERSION
    }