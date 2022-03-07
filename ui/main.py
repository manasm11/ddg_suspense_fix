"""Server to be used by frontend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

origins = [
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint to test if server is running."""
    return {"message": "SERVER IS ON"}


@app.get("/possible-parties")
async def possible_parties(desc):
    """Get possible_parties with the given desc."""
    logger.info(f"desc={desc}")
    return ["JAIPUR MOHAN"]
