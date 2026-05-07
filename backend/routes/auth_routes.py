from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer
from models.user_schemas import UserCreate, UserLogin, Token, UserResponse
from database.db import users_collection
from services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
    SECRET_KEY,
    ALGORITHM
)
from services.email_service import send_verification_email
from bson import ObjectId
import jwt
from datetime import datetime, timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# 🚀 REGISTER USER
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):

    # ✅ Check existing email
    existing_user = users_collection.find_one({
        "email": user.email
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 🔐 Hash password
    hashed_password = get_password_hash(user.password)

    # 📦 Store user in MongoDB
    user_dict = {
        "email": user.email,
        "name": user.name,
        "password": hashed_password,
        "is_verified": False,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_dict)
    verification_token = create_access_token(
        data={"sub": str(result.inserted_id)},
        expires_delta=timedelta(hours=1),
        token_type="email_verify"
    )
    send_verification_email(user.email, verification_token)

    # ✅ Return response
    return {
        "id": str(result.inserted_id),
        "email": user.email,
        "name": user.name
    }


# 🚀 LOGIN USER
@router.post("/login", response_model=Token)
def login_user(user: UserLogin):

    db_user = users_collection.find_one({
        "email": user.email
    })

    # ❌ Invalid credentials
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # ❌ Wrong password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not db_user.get("is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address is not verified"
        )

    # ✅ Create JWT token
    access_token = create_access_token(
        data={"sub": str(db_user["_id"])}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 🔐 GET CURRENT USER
def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token, expected_type="access")

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    return user_id


@router.get("/me", response_model=UserResponse)
def read_current_user(user_id: str = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"]
    }


@router.get("/verify-email")
def verify_email(token: str = Query(...)):
    try:
        payload = decode_token(token, expected_type="email_verify")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )

        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_verified": True}}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification failed or already verified"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {"message": "Email verified successfully"}


# 🔓 OPTIONAL USER
def get_optional_user(
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/login",
            auto_error=False
        )
    )
):

    if not token:
        return None

    try:
        payload = decode_token(token, expected_type="access")
        return payload.get("sub")

    except Exception:
        return None