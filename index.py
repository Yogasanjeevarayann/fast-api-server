import os
from fastapi import FastAPI, HTTPException, Response, status
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

load_dotenv()

app = FastAPI()

# Load environment variables
# mongo_db_url = os.getenv("MONGO_DB_URL")

# MongoDB client and collection initialization
client = MongoClient("mongodb+srv://yoga1234:yoga1234@cluster0.z7les3c.mongodb.net/")
db = client['JuneCore']
students_collection = db['students']  # Ensure this is the correct collection name

# Routes
@app.get("/", response_class=Response)
async def get_hello():
    return 'Hello World!'

@app.get("/api/students", response_class=Response)
async def get_students(userID: str = None):
    filter = {} if userID is None else {"userID": userID}
    students = list(students_collection.find(filter))
    return Response(content=dumps(students), media_type="application/json")

@app.post("/api/students", status_code=status.HTTP_201_CREATED)
async def add_student(student: dict):
    students_collection.insert_one(student)
    return {"message": "Student added successfully"}

@app.delete("/api/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student(id: str):
    result = students_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@app.put("/api/students/{id}", status_code=status.HTTP_200_OK)
async def update_student(id: str, student: dict):
    result = students_collection.update_one({'_id': ObjectId(id)}, {"$set": student})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return Response(
        content=dumps({
            "errorCode": exc.status_code,
            "errorDescription": exc.detail,
            "errorName": exc.__class__.__name__
        }),
        media_type="application/json",
        status_code=exc.status_code
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return Response(
        content=dumps({
            "errorCode": 500,
            "errorDescription": "Internal Server Error",
            "errorDetailedDescription": str(exc),
            "errorName": exc.__class__.__name__
        }),
        media_type="application/json",
        status_code=500
    )

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
