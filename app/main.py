from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from config.config import SETTING
from routers import user_auth_api,shipment_api
from dotenv import load_dotenv
from configuration.configuration import SETTING

load_dotenv()

app = FastAPI(title=SETTING.TITLE, description=SETTING.DESCRIPTION, version=SETTING.PROJECT_VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse("homepage.html", {"request": request})


app.include_router(user_auth_api.app)
app.include_router(shipment_api.app)
