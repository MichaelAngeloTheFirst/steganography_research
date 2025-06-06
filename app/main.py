from fastapi import FastAPI
from app.routers import stego_mail_reader, stego_mail_writer

app = FastAPI()

app.include_router(stego_mail_reader.router)
app.include_router(stego_mail_writer.router)


@app.get("/")
async def root():
    return {"message": "Go to /docs"}
