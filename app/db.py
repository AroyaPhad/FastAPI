import pymongo
import time
from datetime import datetime

client = pymongo.MongoClient("mongodb://mongoadmin:thisIsVerySecret@localhost:27017/")
db = client["ekyc"]
students_collection = db["students"]

def query_all_students():
    return list(students_collection.find())

def insert_student_data(student_id: str, name: str):
    if students_collection.find_one({"student_id": student_id}) is not None:
        return None
    d = datetime.now()
    student = {
        "created_at": d,
        "modified_at": d,
        "student_id": student_id,
        "name": name
    }
    result = students_collection.insert_one(student)
    return str(result.inserted_id)
