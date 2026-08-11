from fastapi import FastAPI
from app.jobs import router as jobs_router
from app.profile import router as profile_router
from contextlib import asynccontextmanager
from app.scheduler import starts_scheduler,stop_scheduler

app = FastAPI()

@asynccontextmanager
async def lifespan(app:FastAPI):
    starts_scheduler()
    yield
    stop_scheduler()

app = FastAPI(lifespan=lifespan)
app.include_router(jobs_router)
app.include_router(profile_router)


@app.get("/")
def root():
    print("Root reached")
    return {"message": "ok"}
