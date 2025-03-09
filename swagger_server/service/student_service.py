
import os
import uuid
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
db = client["student_db"]
students_collection = db["students"]

def add(student=None):
    student_exists = students_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )

    if student_exists is not None:
        return "duplicate student", 409

    new_id = str(uuid.uuid4())
    student_data = dict(student.to_dict())
    student_data["_id"] = new_id
    insert_result = students_collection.insert_one(student_data)

    return uuid.UUID(insert_result.inserted_id)


def get_by_id(student_id=None):
    student = students_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student["_id"]

    return student


def delete(student_id=None):
    result = students_collection.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        return 'not found', 404

    return uuid.UUID(student_id)
