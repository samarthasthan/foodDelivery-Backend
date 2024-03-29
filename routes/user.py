from typing import List

import database, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from schemas import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.get('/getuser/{user_id}', response_model=user.ShowOrders)
async def get_user_by(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.index == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Account with the id {user_id} is not available")
    return user


@router.get('/getusers', response_model=List[user.ShowUser])
async def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@router.get('/search')
async def search(search_term:str,db:Session = Depends(get_db)):
    search_query = db.query(models.Items).filter(models.Items.name.contains(search_term)).all()
    return {"results" : search_query}
