from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app import middlewares
from app.routers import base, emoji, mood, user

# API METADATA & DOCS
# You don't have to fill all those fields in order to create an API.
# For example, if you create an App like "app = FastAPI()" it will work normally.
# Another important point is the API Docs like redoc and swagger. In my case,
# these docs are not being protected by the API Authentication, but let's say that
# you need that your API docs can only be accessed by authenticated users, how can you proceed?
# In this article you will find a way to protect you API Docs...
# https://medium.com/data-rebels/fastapi-how-to-add-basic-and-cookie-authentication-a45c85ef47d3
#
# MORE INFO
# Metadata: https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="Fast App",
    description="Fast App it is my first FastAPI app 🚀",
    version="1.0.0",
    contact={
        "name": "Anthony Caliani",
        "url": "https://github.com/avcaliani",
        "email": "anthony@github.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# TODO List
#   - Database (SQL or NoSQL)
#   - Unit Tests
#   - Logging

# 👇 Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# 👇 Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.add_process_time_header)

# 👇 Routers
app.include_router(base.router)
app.include_router(emoji.router)
app.include_router(mood.router)
app.include_router(user.router)
