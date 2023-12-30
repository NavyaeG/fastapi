from .. import models, schema, oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user),limit: int=10,search: Optional[str]=""):#limit,search is a query parameter here
    #cursor.execute("""select* from posts""")
    #posts=cursor.fetchall()
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all() #returns only the number of posts specififed in limit as ?limit=1. default limit value is 10. It also returns posts which have the exact search word in them
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.PostO)
def create_posts(posts: schema.PostCreate,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):#dependency created which forces users to be logged in before creating post
    # """
    # This code is wrong as it opend you to injection attacks
    # #cursor.execute(f"insert into posts (title, content, published) values ({posts.title},{posts.content},{posts.published})")
    # """
    # #this code sanitises the inputs so the second field makes sure there are no weird sql commands
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * """,(posts.title,posts.content,posts.published))
    # new_post=cursor.fetchone()
    # #commit the changes made
    # conn.commit()

    #new_post=models.Post(title=posts.title,content=posts.content,published=posts.published)
    new_post=models.Post(owner_id=current_user.id,**posts.dict()) #works the same as above code, but here it is easier and we dont have to pass every field, ** unpacks the dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#works similar to returning *
    return new_post

@router.get("/{id}",response_model=schema.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id=%s""",(str(id)))
    # post=cursor.fetchone()

    #post=db.query(models.Post).filter(models.Post.id==id).first()#stops after finding first instance of matching
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id=%s returning *""",(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)
    deleted_post=post_query.first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    if deleted_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    
@router.put("/{id}",response_model=schema.PostO)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    if updated_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorised to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()