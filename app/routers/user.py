from .. import models, schema, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.User)
def create_user(user: schema.UserCreate,db: Session = Depends(get_db)):
    #hash the password
    hashed_password=utils.hashpassword(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)#works similar to returning *
    return new_user

@router.get("/{id}",response_model=schema.User)
def  get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user_details=db.query(models.User).filter(models.User.id==id).first()#stops after finding first instance of matching
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} was not found")
    return user_details