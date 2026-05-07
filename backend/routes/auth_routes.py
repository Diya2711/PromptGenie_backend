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

import jwt
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login"
)


# 🚀 REGISTER USER
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    from services.email_service import send_verification_email
    from services.auth_service import create_email_token

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
        "is_verified": False,   # Requires email verification
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_dict)

    # 📧 Send verification email
    try:
        verify_token = create_email_token({"sub": user.email})
        send_verification_email(user.email, verify_token)
    except Exception as e:
        print(f"⚠️ Could not send verification email: {e}")

    # ✅ Return response
    return {
        "id": str(result.inserted_id),
        "email": user.email,
        "name": user.name,
        "is_verified": False
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

    # ⚠️ Email not verified
    if not db_user.get("is_verified", False):
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first"
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
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    return user_id


# 🔓 OPTIONAL USER
def get_optional_user(
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl="api/v1/auth/login",
            auto_error=False
        )
    )
):

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except jwt.PyJWTError:
        return None


# ✅ VERIFY EMAIL
@router.get("/verify-email")
def verify_email(token: str):
    from services.auth_service import verify_email_token
    
    email = verify_email_token(token)
    
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification token"
        )
    
    # ✅ Update user in database
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"is_verified": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return {"message": "✅ Email verified successfully!"}