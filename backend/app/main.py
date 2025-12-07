from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.db_client import prisma

from app.api import rfp, vendor, email, user, rfp_vendor, proposal, email_log, recommendation
from fastapi import FastAPI
from app.tasks.email_sync import sync_email_loop
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    print("Prisma connected.")
    
    # 🚀 Start background email sync task
    # loop = asyncio.get_event_loop()
    # loop.create_task(sync_email_loop(interval=20))
    
    yield
    
    await prisma.disconnect()
    print("Prisma disconnected.")


app = FastAPI(
    title="RFP AI Backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfp.router, prefix="/rfp")
app.include_router(vendor.router, prefix="/vendor")
app.include_router(email.router, prefix="/email")
app.include_router(user.router, prefix="/user")
app.include_router(proposal.router, prefix="/proposal")
app.include_router(rfp_vendor.router, prefix="/rfp-vendor")
app.include_router(email_log.router, prefix="/logs")
app.include_router(recommendation.router, prefix="/recommendation")