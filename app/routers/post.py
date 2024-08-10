from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database  import get_db
from typing import List

#CRUD - posts
#function to get post

router = APIRouter(
    prefix="/posts",  #/id    /posts/{id} 
    tags=['Posts']
)



@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
#    cursor.execute(""" SELECT * FROM posts """)
#    posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return  posts

#function to create post
@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #create a new post
    #print(current_user.id)
    #print(current_user.email)
    new_post = models.Post(owner__id=current_user.id, **post.dict())
    #add it to the database
    db.add(new_post) 
    #commit the changes
    db.commit()
    #retrieve the changes made and store it back into new_post
    db.refresh(new_post)
    return new_post

#function to retrieve an individual post
@router.get("/{id}",response_model=schemas.Post)
def get_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found ")
        #response.status_code = status.HTTP_404_NOT_FOUND
       # return { "message": f"post with id: {id} was not found "}
    return post

#to delete a post ie a http req
#find the index in the array that has required ID
#my_posts.pop(index) and pass the index

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    if post.owner__id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= f"Not Authorized to perform required action" )
    post_query.delete(synchronize_session=False) 
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update posts
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title =  %s, content = %s, published = %s WHERE id =%s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #check if its available
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    # post_query.update({'title': 'hey this is newww!!', 'content': 'Neww is hereee'}, synchronize_session=False)
    if post.owner__id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform required action")
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    # return{"data": 'successfull!'}
    #fetches the updated
    return post_query.first()




