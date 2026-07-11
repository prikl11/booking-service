from typing import Annotated
from fastapi import Form

class UserFormData:
    def __init__(
            self,
            first_name: Annotated[str, Form()],
            last_name: Annotated[str, Form()],
            email: Annotated[str, Form(json_schema_extra={"example": "example@example.com"})],
            phone: Annotated[str, Form(json_schema_extra={"example": "+7 (000) 000 00-00"})],
            password: Annotated[str, Form()],
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
        }
    

class UserUpdateFormData:
    def __init__(
            self,
            first_name: Annotated[str | None, Form()] = None,
            last_name: Annotated[str | None, Form()] = None,
            email: Annotated[str | None, Form(json_schema_extra={"example": "example@example.com"})] = None,
            phone: Annotated[str | None, Form(json_schema_extra={"example": "+7 (000) 000 00-00"})] = None,
            password: Annotated[str | None, Form()] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
        }