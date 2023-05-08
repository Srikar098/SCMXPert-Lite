from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configuration.configuration import SETTING
from models.models import User
from routers.user_auth_api import get_current_user_from_cookie, navigation_links

# Load environment variables from the .env file
load_dotenv()

app = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

# Connect to MongoDB
CLIENT = SETTING.CLIENT
DEVICE_DATA = SETTING.DEVICE_DATA_COLLECTION


# Get request for Device Data Stream and display the data
@app.get("/device_data_stream", response_class=HTMLResponse)
async def data_stream(request: Request,current_user: User = Depends(get_current_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login")
    
    if current_user["Role"] !="Admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    links = navigation_links(current_user["Role"])
    try:
        device_details = DEVICE_DATA.find({})
        context = {
            "user": current_user,
            "request": request,
            "links": links,
            "data_streaming": device_details
        }
        return TEMPLATES.TemplateResponse("devicedata.html", context)
    except Exception as e:
        print(e)
