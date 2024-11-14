from uuid import uuid4
import os
from dotenv import load_dotenv


load_dotenv()

class Autent():
    api_key = str(uuid4())
    user = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    @classmethod
    def get_key(cls, username:str, password:str) -> str:
            if username == cls.user and password == cls.password: 
                return Autent.api_key
            else:
                print("incorrect username or password.")
                return None

