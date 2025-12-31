from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlmodel import Session
from .database import get_session
from .models import User
from .auth import SECRET_KEY, ALGORITHM

async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
):
    # Check for API Key first
    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = session.query(User).filter(User.api_key == api_key).first()
        if user:
            return user
        raise HTTPException(status_code=401, detail="Invalid API Key")
        
    # Check for Bearer Token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username:
                user = session.query(User).filter(User.email == username).first()
                if user:
                    return user
        except JWTError:
           pass
           
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
