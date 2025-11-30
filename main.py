from fastapi import FastAPI,Response,Depends

from src.core.config import settings,Settings

app=FastAPI(description="What to Eat API")



#路由引入
@app.get("/")
def read_root(settings:Settings=settings):
    return {"message":"Welcome to What to Eat API","app_name":settings.app_name,
            "app_version":settings.app_version,"database_url":settings.database_url,"jwt_secret":settings.jwt_secret}


@app.get("/health")
async def health_check(response:Response):
    response.status_code=200
    return {"status":"ok"}