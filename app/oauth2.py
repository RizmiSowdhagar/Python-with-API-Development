from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db


def get_current_user(db: Session = Depends(get_db)) -> models.User:
    """
    For assignments: ensure there is at least one user and return it.
    """
    user = db.query(models.User).first()
    if user is None:
        # Create a simple dummy user
        user = models.User(
            email="test@example.com",
            hashed_password="fakehashedpassword",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
