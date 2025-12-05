from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.prisma import prisma
from app.api import rfp, vendor, email, user, rfp_vendor


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    print("Prisma connected.")
    
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
app.include_router(rfp_vendor.router, prefix="/rfp-vendor")
