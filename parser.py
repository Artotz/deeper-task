from dataclasses import dataclass
from pymongo import MongoClient
from datetime import datetime
import json, pytz

uri="mongodb+srv://arturmcatunda:Vongol%4010@cluster0.tm5hf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

filepath = "udata.json"

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool

def parse_user_data(json_data):
    users = []
    for user_data in json_data.get("users", []):
        roles = []

        if user_data["is_user_admin"]:
            roles.append("admin")
        if user_data["is_user_manager"]:
            roles.append("manager")
        if user_data["is_user_tester"]:
            roles.append("tester")

        preferences = UserPreferences(timezone=user_data["user_timezone"])

        created_ts = datetime.strptime(user_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        created_ts = created_ts.replace(tzinfo=pytz.UTC).timestamp()

        user = User(
            username=user_data["user"],
            password=user_data["password"],
            roles=roles,
            preferences=preferences,
            created_ts=created_ts,
            active=user_data["is_user_active"]
        )
        users.append(user)
    
    return users

def upload_to_mongo(users):
    client = MongoClient(uri)
    db = client["mydatabase"]
    collection = db["users"]
    
    users_data = [
        {
            "username": user.username,
            "password": user.password,
            "roles": user.roles,
            "preferences": {"timezone": user.preferences.timezone},
            "active": user.active,
            "created_ts": user.created_ts
        }
        for user in users
    ]
    
    collection.insert_many(users_data)
    print(f"Uploaded {len(users_data)} users to MongoDB.")

with open(filepath, "r", encoding="utf-8") as file:
    json_data = json.load(file)

users = parse_user_data(json_data)
upload_to_mongo(users)
