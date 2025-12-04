from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.prisma import prisma
from app.api import rfp, vendor, email


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await prisma.connect()
    print("Prisma connected.")
    
    yield
    
    # Shutdown
    await prisma.disconnect()
    print("Prisma disconnected.")


app = FastAPI(
    title="RFP AI Backend",
    lifespan=lifespan
)

app.include_router(rfp.router, prefix="/rfp")
app.include_router(vendor.router, prefix="/vendor")
app.include_router(email.router, prefix="/email")
