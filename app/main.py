from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
#Setup the DB connection
try:
    conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user ='username', password = 'password', cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print('Database connection successfull!')
except Exception as error:
    print("COnnecting to Database failed")
    print("Error: ", error)
#Setup the DB connection


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
def get_posts():
    return {"data": my_posts}

#function to create post
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}

#function to retrieve an individual post
@app.get("/posts/{id}")
def get_posts(id: int, response: Response):

    post = find_posts(int(id))
    #to let the user know that the id they want does not exist instead of just a null response
    if not post:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found ")
        #response.status_code = status.HTTP_404_NOT_FOUND
       # return { "message": f"post with id: {id} was not found "}
    return{"post_detail": post}

#to delete a post ie a http req
#find the index in the array that has required ID
#my_posts.pop(index) and pass the index

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_post(id:int):
    index = find_index_posts(id)
    
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #check the post's index
    index = find_index_posts(id)
    #check if its available
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    #take the data from  frontend which is stored in post and convert into dict
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}

