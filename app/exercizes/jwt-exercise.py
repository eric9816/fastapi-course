from datetime import datetime, timedelta

from jose import jwt


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode, "jkfdghjkdfHJSDG", algorithm="HS256"
    )
    return encoded_jwt

print(create_access_token({'user': 'eric'}))