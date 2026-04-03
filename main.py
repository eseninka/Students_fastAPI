from fastapi import FastAPI
from routers.students import router_upload, router_student

app = FastAPI()

app.include_router(router_upload)
app.include_router(router_student)
