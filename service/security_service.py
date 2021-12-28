import jwt

key = "key"

class Token:
    def __init__(self):
        pass

    def authenticate(self, username: str, password: str):
        encoded = jwt.encode({"user": username}, key, algorithm="HS256")
        return encoded