from typing import Optional
from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# req GET method url: "/"

my_posts = [{"title":"title of post 1","content": "conntent of post 1","id": 1}, {"title": "favourite foods", "content": "I like Pizza", "id": 2}]

def find_posts(id):
    for p in my_posts:
        if p ["id"] == id:
            return p

@app.get("/")
def root():  
    return {"message": "Hello World"}

#CRUD
#function to get post
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#function to create post
@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}

#function to get an individual post
@app.get("/posts/{id}")
def get_posts(id: int, response: Response):

    post = find_posts(int(id))
    if not post:
        response.status_code = 404
    return{"post_detail": post}
