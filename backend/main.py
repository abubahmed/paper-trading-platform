from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import engine, Base
import models  # noqa: F401 — registers all models with Base
from routers import auth, leaderboard, orders, portfolio, prices

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Princeton Trading API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(prices.router, prefix="/prices", tags=["prices"])

@app.get("/health")
def health():
    return {"status": "ok"}