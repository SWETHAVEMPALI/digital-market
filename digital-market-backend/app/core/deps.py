"""Dependencies for protected endpoints."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import decode_access_token


# This tells FastAPI where to get tokens from
# tokenUrl is the endpoint that issues tokens (we'll create /login next)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current logged-in user from the JWT token.

    Use this as a dependency in any endpoint that needs authentication:

        @app.get("/protected")
        def protected_route(user: User = Depends(get_current_user)):
            return {"hello": user.email}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Get the user_id from the token payload
    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Look up the user in the database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role. Use for admin-only endpoints."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user