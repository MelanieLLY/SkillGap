from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from server.auth import deps, models, schemas, utils
from server.core.config import settings
from server.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """
    Register a new user in the system.

    Args:
        user_in (schemas.UserCreate): The user creation payload containing email and password.
        db (Session): The synchronous database session.

    Returns:
        models.User: The newly created user instance.

    Raises:
        HTTPException: If the email is already registered.
    """
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = utils.get_password_hash(user_in.password)
    db_user = models.User(email=user_in.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authenticate a user and return an access token.

    Args:
        db (Session): The synchronous database session.
        form_data (OAuth2PasswordRequestForm): The form data containing username (email) and password.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the email or password is incorrect.
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = utils.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(deps.get_current_active_user)) -> models.User:
    """
    Retrieve the current authenticated user's profile information.

    Args:
        current_user (models.User): The currently authenticated user instance.

    Returns:
        models.User: The profile information of the current user.
    """
    return current_user
