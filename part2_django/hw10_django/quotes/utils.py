from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost:8000")

    db = client.hw10
    return db
