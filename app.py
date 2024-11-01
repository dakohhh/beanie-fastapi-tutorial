from fastapi import FastAPI
from tasks import router as task_router
from database import connect_to_mongo


app  = FastAPI(title="Beanie Tutorial") 


@app.on_event("startup")
async def connect():
    await connect_to_mongo()




app.include_router(task_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}