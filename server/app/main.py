from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.file_router import router as file_router
from routers.chat_router import router as chat_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(file_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
