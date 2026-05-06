from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from models.user_schemas import UserCreate, UserLogin, Token, UserResponse
from database.db import users_collection
from services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from services.email_service import send_verification_email
import jwt
from datetime import datetime, timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# 🚀 REGISTER USER
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔐 Hash password
    hashed_password = get_password_hash(user.password)

    # 🔑 Generate verification token
    verification_token = jwt.encode(
        {
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # 📦 Store user
    user_dict = {
        "email": user.email,
        "name": user.name,
        "password": hashed_password,
        "is_verified": False,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_dict)

    # 📧 Send verification email
    send_verification_email(user.email, verification_token)

    return {
        "id": str(result.inserted_id),
        "email": user.email,
        "name": user.name
    }


# 🚀 LOGIN USER
@router.post("/login", response_model=Token)
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})

    # ❌ Wrong credentials
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # 🚨 EMAIL VERIFICATION CHECK (THIS IS STEP 4)
    if not db_user.get("is_verified", False):
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please check your email."
        )

    # ✅ Create token if everything is OK
    access_token = create_access_token(data={"sub": str(db_user["_id"])})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 🚀 VERIFY EMAIL API
@router.get("/verify-email")
def verify_email(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        users_collection.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )

        return {"message": "✅ Email verified successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")

    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


# 🔐 GET CURRENT USER (Protected routes)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    return user_id


# 🔓 OPTIONAL USER (for public routes)
def get_optional_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False))
):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None