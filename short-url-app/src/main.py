from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from src.routers.AdminRouter import AdminRouter
from src.routers.MainRouter import MainRouter
from src.models.BaseModel import init
from src.configs.Environment import get_environment_variables
import uvicorn
# Application Environment Configuration
env = get_environment_variables()

app = FastAPI(title=env.APP_NAME)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

    
# Add Routers
app.include_router(AdminRouter)
app.include_router(MainRouter)


init()

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=env.APP_PORT, reload=True)