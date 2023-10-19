from fastapi import FastAPI
from enum import Enum
import uuid
from pydantic import BaseModel, Field
import json

class UserType(Enum):
    ADMIN = "admin"
    GUEST = "visitor"


class User(BaseModel):
    role: UserType
    name: str
    uid: uuid.UUID = Field(default_factory=uuid.uuid4)


class UserManager:
    def __init__(self, users: dict) -> None:
        self.users = users

    def add_user(self, role: UserType, name: str) -> User:
        user = User(role=role, name=name)
        while True:
            if user.uid not in self.users:
                self.users[str(user.uid)] = {"role": role.value, "name": name}
                break
            else:
                user = User(role=role, name=name)
        with open("users.json", "r") as f:
            data = json.load(f)
        data.update(self.users)
        with open("users.json", "w") as f:
            try:
                json.dump(data, f, indent=4)
            except FileNotFoundError as e:
                raise FileNotFoundError("file not found!")
        return user


app = FastAPI()


# https://docs.python.org/fr/3/library/uuid.html
