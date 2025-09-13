from sqlalchemy.orm import Session
from . import models
import os

MAX_DEVICES = int(os.getenv("MAX_DEVICES", 3))


def add_session(db: Session, user_id: str, device_id: str):
    # Check how many sessions user already has
    sessions = db.query(models.Session).filter(models.Session.user_id == user_id).all()
    if len(sessions) >= MAX_DEVICES:
        return False, sessions  # too many devices
    # Add new session
    new_session = models.Session(user_id=user_id, device_id=device_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return True, new_session


def remove_session(db: Session, device_id: str):
    db.query(models.Session).filter(models.Session.device_id == device_id).delete()
    db.commit()
