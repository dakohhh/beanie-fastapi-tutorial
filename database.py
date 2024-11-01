import beanie
import motor
import motor.motor_asyncio
from models import Task


async def connect_to_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")


    # TaskDB is the name of the database
    await beanie.init_beanie(database=client.TaskDB, document_models=[Task])

    print("Connected to MongoDB database")