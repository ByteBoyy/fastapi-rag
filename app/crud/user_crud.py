from app.database import users_collection
from app.auth.auth_handler import hash_password, verify_password
from bson.objectid import ObjectId

def create_user(username: str, email: str, password: str):
    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hash_password(password),
        "role": "user"
    }
    result = users_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return user_data

def get_user_by_username(username: str):
    user = users_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
    return user

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

def get_user_by_id(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
    return user

def update_user_email(user_id: str, new_email: str):
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"email": new_email}})
    return get_user_by_id(user_id)

def delete_user(user_id: str):
    return users_collection.delete_one({"_id": ObjectId(user_id)})

def update_user_role(username: str, new_role: str):
    return users_collection.update_one({"username": username}, {"$set": {"role": new_role}})

def delete_user_by_username(username: str):
    return users_collection.delete_one({"username": username})


