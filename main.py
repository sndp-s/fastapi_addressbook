"""
Main app - starting point of the application

All the APIs are located here as well
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    """
    hello world example handler
    """
    return "Hello world!"
