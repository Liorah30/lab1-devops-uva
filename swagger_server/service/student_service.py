import os
from functools import reduce

from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

print("MONGO_URI:", os.getenv("MONGO_URI"))
print("DB_NAME:", os.getenv("DB_NAME"))

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
students_collection = db["students"]

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def add(student=None):
    logging.info("We are here")
    try:
        student_exists = students_collection.find_one(
            {"first_name": student.first_name, "last_name": student.last_name}
        )
        logging.info("made it here")

        if student_exists is not None:
            return "already exists", 409

        student_data = dict(student.to_dict())
        insert_result = students_collection.insert_one(student_data)

        return str(insert_result.inserted_id)
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        return "Internal server error", 500

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

    return str(student_id)