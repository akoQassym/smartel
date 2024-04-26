# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

from fastapi import FastAPI

app = FastAPI(
    title= "Smartel API",
    description= "This is an API for Smartel System",
    docs_url= "/",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

