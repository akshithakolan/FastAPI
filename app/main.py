from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from . database import engine, get_db

#SessionLocal object is responsible for talking to the db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user ='username', password = 'password', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successfull!')
        break

    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(2)


# req GET method url: "/"

my_posts = [{"title":"title of post 1","content": "conntent of post 1","id": 1}, {"title": "favourite foods", "content": "I like Pizza", "id": 2}]

def find_posts(id):
    for p in my_posts:
        if p ["id"] == id:
            return p

def find_index_posts(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():  
    return {"message": "Hello World"}


#CRUD
#function to get post
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
#    cursor.execute(""" SELECT * FROM posts """)
#    posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return  posts

#function to create post
@app.post("/posts", status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    #create a new post
    new_post = models.Post(**post.dict())
    #add it to the database
    db.add(new_post) 
    #commit the changes
    db.commit()
    #retrieve the changes made and store it back into new_post
    db.refresh(new_post)
    return new_post

#function to retrieve an individual post
@app.get("/posts/{id}")
def get_posts(id: int,db: Session = Depends(get_db)):
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

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_post(id:int,db: Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update posts
@app.put("/posts/{id}")
def update_post(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title =  %s, content = %s, published = %s WHERE id =%s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    
    # updated_post = cursor.fetchone()
    # conn.commit()

    #check if its available
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    # post_query.update({'title': 'hey this is newww!!', 'content': 'Neww is hereee'}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    # return{"data": 'successfull!'}
    #fetches the updated
    return post_query.first()

