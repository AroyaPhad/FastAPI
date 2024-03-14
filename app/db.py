import pymongo
from datetime import date

client = pymongo.MongoClient("mongodb://mongoadmin:thisIsVerySecret@localhost:27017/")
db = client["ekyc"]
students_collection = db["students"]

def query_all_students():
    return students_collection.find()

def insert_student_data(id, name):
    if students_collection.find_one({"student_id": str(id)}) is not None:
        return
    now = date.today()
    student = {
        "created_at": now,
        "modified_at": now,
        "student_id": str(id),
        "name": str(name)
    }
    students_collection.insert_one(student)
