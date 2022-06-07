from time import time
initTime = time()
print(f"[INFO] Started main.py")
import motor.motor_asyncio
import asyncio
from db.mongo import Document
import os

print(f"[INFO] Imported libraries: {time() - initTime}s")

MONGOURI = os.getenv("MONGOURI")
PORT = os.getenv("PORT")

mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGOURI)
forumDb = mongo["Forum"]
usersCollection = Document(forumDb, "Users")
postsCollection = Document(forumDb, "Posts")
categoriesCollection = Document(forumDb, "Categories")

print(f"[INFO] Connected to database collections: {time() - initTime}s")
