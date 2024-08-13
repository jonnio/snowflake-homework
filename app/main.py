import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World",
            "version": 3,
            "SNOW": os.environ.get("SNOWFLAKE_PASSWORD", "NONE HERE")
            }
