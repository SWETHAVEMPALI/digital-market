"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, products


# Create all database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A digital marketplace for selling digital products",
    version="0.1.0",
    debug=settings.debug,
)

# CORS - allow React frontend (port 5173) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(products.router)


# Health check (for monitoring)
@app.get("/health")
def health_check():
    return {"status": "healthy"}