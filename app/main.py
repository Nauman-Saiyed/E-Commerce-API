from fastapi import FastAPI
from app.core.config import settings
from app.routes import auth , users , products , categories , orders

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router , prefix=settings.API_V1_STR)
app.include_router(users.router , prefix=settings.API_V1_STR)
app.include_router(products.router , prefix=settings.API_V1_STR)
app.include_router(categories.router , prefix=settings.API_V1_STR)
app.include_router(orders.router , prefix=settings.API_V1_STR)