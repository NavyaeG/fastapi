from fastapi import FastAPI
from random import randrange
from .database import engine,get_db
from .routers import post,user,auth,vote
from . import models
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=[""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

"""
@gfg_decorator
def hello_decorator():
    print("Gfg")

Above code is equivalent to -

def hello_decorator():
    print("Gfg")
    
hello_decorator = gfg_decorator(hello_decorator)

In the above code, gfg_decorator is a callable function, that will add some code on the top of some another callable function, 
hello_decorator function and return the wrapper function.
"""

@app.get("/")#Decorator: to turn function into path operation
def root():
    return {"message": "Hello World!!"}