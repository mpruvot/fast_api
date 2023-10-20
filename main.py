from fastapi import FastAPI, Request, HTTPException
from enum import Enum
import uuid
from pydantic import BaseModel, Field
import json
from my_exceptions import *
from typing import Optional


class UserType(Enum):
    ADMIN = "admin"
    GUEST = "visitor"


class User(BaseModel):
    role: UserType
    name: str
    uid: uuid.UUID = Field(default_factory=uuid.uuid4)


class UserManager:
    def __init__(self) -> None:
        try:
            with open("users.json", "r") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {"users_by_id": {}}

    def check_unique_username(self, name: str):
        usernames = [i["name"] for i in self.users["users_by_id"].values()]
        return name not in usernames

    def add_user(self, role: UserType, name: str) -> User:
        """create <User> with unique ID from Class User and store it into "users.json" file"""
        if not self.check_unique_username(name):
            raise UserAlreadyExistsError("This Username is already taken")

        user = User(role=role, name=name)
        self.users["users_by_id"][str(user.uid)] = {
            "role": role.value,
            "name": name,
        }

        with open("users.json", "w") as f:
            json.dump(self.users, f, indent=4)

        return user


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "home-page"}


@app.get("/users")
def get_by_role(user_role: Optional[str] = None):
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
        if not user_role:
            return data
        elif user_role not in [i.value for i in UserType]:
            return {"DataError": "user_role provided does not exists"}
        else:
            user_by_role = {
                user_id: user_info
                for user_id, user_info in data["users_by_id"].items()
                if user_info["role"] == user_role
            }
            return user_by_role
    except FileNotFoundError:
        return {"error": "File not found"}


@app.get("/users/{user_uuid}")
def get_user_by_uuid(user_uuid: str):
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "File not found"}

    if user_uuid in data["users_by_id"]:
        return {
            user_id: user_info
            for user_id, user_info in data["users_by_id"].items()
            if user_id == user_uuid
        }
    else:
        return ({"error": "User not found"},)


@app.post("/users", response_model=uuid.UUID)
def create_user(user: User):
    manager = UserManager()
    try:
        new_user = manager.add_user(user.role, user.name)
        return new_user.uid
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/users")
def delete_user(user_id: str):
    with open("users.json", "r") as f:
        data = json.load(f)
    if user_id not in data["users_by_id"]:
        raise HTTPException(status_code=400, detail=str("ID does not exists."))

    del data["users_by_id"][user_id]
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)


# https://docs.python.org/fr/3/library/uuid.html
# https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
