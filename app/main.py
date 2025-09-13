from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, auth, session_manager

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/private")
def private_page(user=Depends(auth.get_current_user)):
    return {
        "message": f"Hello {user['name']}, your phone is {user.get('phone_number', 'N/A')}"
    }


@app.post("/login")
def login(
    device_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)
):
    success, data = session_manager.add_session(db, user["sub"], device_id)
    if not success:
        return {
            "error": "Too many devices logged in",
            "sessions": [s.device_id for s in data],
        }
    return {"status": "logged_in", "device_id": data.device_id}


@app.post("/logout")
def logout(
    device_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)
):
    session_manager.remove_session(db, device_id)
    return {"status": "logged_out"}
