from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configuration.configuration import SETTING
from models.models import User
from routers.user_auth_api import get_current_user_from_cookie, navigation_links

load_dotenv()

app = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

CLIENT = SETTING.CLIENT
DEVICE_DATA = SETTING.DEVICE_DATA_COLLECTION

@app.get("/device_data_stream", response_class=HTMLResponse)
async def data_stream(request: Request,current_user: User = Depends(get_current_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login")
    
    links = navigation_links(current_user["Role"])
    # d_links = dashboard_links(current_user["Role"])
    try:
        data_streaming = []
        device_details = DEVICE_DATA.find({})
        for i in device_details:
            data_streaming.append(i)
        context = {
            "user": current_user,
            "request": request,
            "links": links,
            "data_streaming":data_streaming
            # "d_links": d_links
        }
        return TEMPLATES.TemplateResponse("devicedata.html", context)
    except Exception as e:
        print(e)
