import os

from dotenv import load_dotenv
from fastapi import FastAPI
from passlib.context import CryptContext
from pydantic import deprecated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()
# para rodar o código, executar no terminal> uvicorn main:app --reload

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from auth_routes import auth_routes
from order_routes import order_routes

app.include_router(auth_routes)
app.include_router(order_routes)
