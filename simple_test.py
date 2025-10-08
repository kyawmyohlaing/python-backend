import uvicorn
from fastapi import FastAPI
import os

app = FastAPI(title="Simple Test FastAPI Backend")

@app.get("/")
def root():
    return {"message": "Simple Test FastAPI Backend"}

@app.post("/test")
def test_endpoint():
    return {"message": "Test endpoint working"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8088))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "simple_test:app",
        host=host,
        port=port,
        reload=True,
        log_level="debug"
    )