from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
# from models import User
from db.dummy_generator import generate_dummy_data_for_user
from sqlmodel import Session, select
from db.connection import engine
from db.models import User, Business
from routers.auth import get_current_user_id


router = APIRouter()

@router.post("/")
def generate_my_dummy_data(user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        business_id = generate_dummy_data_for_user(user, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "success", "business_id": business_id}
