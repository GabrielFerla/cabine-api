# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.database import init_db
from app.core.ratelimit import limiter
from app.seed import seed
from app.routers import auth, cabins, readings, alerts, crops

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed()
    yield

app = FastAPI(title="Cabine API", version="1.0.0", lifespan=lifespan)

# rate limiting (bonus de seguranca)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# routers (camada Controller)
app.include_router(auth.router)
app.include_router(cabins.router)
app.include_router(readings.router)
app.include_router(alerts.router)
app.include_router(crops.router)
