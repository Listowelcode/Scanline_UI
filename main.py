from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.history import router as history_router
from routes.scan import router as scan_router
from routes.download import router as download_router
from routes.progress import router as progress_router
from routes.preview import router as preview_router

app = FastAPI(
    title="ScanLine API",
    description="AI coding tutorial extraction system",
    version="1.0"
)


# Allow frontend connection
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# Register ScanLine routes
app.include_router(
    scan_router
)

# Register download routes
app.include_router(
    download_router
)

app.include_router(
    progress_router
)

app.include_router(
    preview_router
)

app.include_router(
    history_router
)

@app.get("/")
def home():

    return {
        "message": "ScanLine backend is running",
        "status": "online"
    }