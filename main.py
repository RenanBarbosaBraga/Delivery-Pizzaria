from fastapi import FastAPI

app = FastAPI()
# para rodar o código, executar no terminal> uvicorn main:app --reload

from auth_routes import auth_routes
from order_routes import order_routes

app.include_router(auth_routes)
app.include_router(order_routes)



