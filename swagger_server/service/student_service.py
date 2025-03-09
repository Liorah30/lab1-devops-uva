import os
import tempfile
from functools import reduce
import uuid
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongo:27017")
db = client["students_db"]
students_collection = db["students"]

def add(student=None):

    student_exists = students_collection.find_one(
        {
        "first_name": student.first_name, 
        "last_name": student.last_name }
    )

    if student_exists :
        return "already exists", 409

    student_data = student.to_dict()
    insert_result = students_collection.insert_one(student_data)
    
    return str(insert_result.inserted_id)

def get_by_id(student_id=None):
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            return 'not found', 404
        student['student_id'] = str(student["_id"])
        del student['_id'] #removing the mongodb's default id because it is not needed and creates error
        return student
    except Exception:
        return 'invalid Id format', 400


def delete(student_id=None):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found', 404

    return student_id