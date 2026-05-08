import os
import jwt

from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

# 🔑 Secret key
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError(
        "❌ SECRET_KEY must be at least 32 characters long"
    )

# JWT settings
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = (
    60 * 24 * 7
)  # 7 days

# 🔒 Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ✅ Verify password
def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ✅ Hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# ✅ Create JWT token
def create_access_token(
    data: dict,
    expires_delta: timedelta = None,
    token_type: str = "access"
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire,
        "type": token_type
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ✅ Decode token
def decode_token(
    token: str,
    expected_type: str = "access"
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != expected_type:
            raise jwt.InvalidTokenError(
                "Invalid token type"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")

    except jwt.PyJWTError:
        raise Exception("Invalid token")