import os
from uuid import UUID
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException, status
from fastapi_users.jwt import decode_jwt
from fastapi_users.authentication import JWTStrategy
from fastapi.security import OAuth2PasswordBearer
from app.db import get_db
from app.models import UserProfile

load_dotenv()
print("========== AUTH.PY LOADED ==========")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


if not SECRET_KEY:
    raise RuntimeError("JWT KEY is not configured")

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")

def hash_password(password:str)->str:
    return password_hash.hash(password)


def verify_password(password: str,password_hash_value: str)-> bool:
    return password_hash.verify(password,password_hash_value)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret = SECRET_KEY,lifetime_seconds = 3600)

print("========== DEFINING GET CURRENT USER ==========")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("========== GET CURRENT USER CALLED ==========")
    print("TOKEN RECEIVED:", bool(token))
    print("SECRET LOADED:", bool(SECRET_KEY))

    try:
        print("BEFORE JWT DECODE")

        payload = decode_jwt(
            token,
            SECRET_KEY,
            ["fastapi-users:auth"],
            algorithms=["HS256"]
        )

        print("AFTER JWT DECODE")
        print("JWT PAYLOAD:", payload)

        user_id = payload.get("sub")

        if not user_id:
            print("NO SUB IN TOKEN")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        print("USER ID FROM TOKEN:", user_id)

        try:
            profile_id = UUID(user_id)
        except ValueError:
            print("INVALID UUID")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID token"
            )

        user = db.query(UserProfile).filter(
            UserProfile.profile_id == profile_id
        ).first()

        print("USER FOUND:", user is not None)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user not found"
            )

        return user

    except HTTPException:
        raise

    except Exception as e:
        print("JWT ERROR TYPE:", type(e).__name__)
        print("JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )