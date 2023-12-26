from fastapi import FastAPI
from routers import users,templates, respuestas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your front-end's actual origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Routers
app.include_router(users.router)
app.include_router(templates.router)
app.include_router(respuestas.router)