
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo.errors import PyMongoError
from models.models import Shipment, User
from routers.user_auth_api import get_current_user_from_cookie, navigation_links
from dotenv import load_dotenv
from configuration.configuration import SETTING

# Load environment variables from the .env file
load_dotenv()

app = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

# Connect to MongoDB
CLIENT = SETTING.CLIENT
SHIPMENT_COLLECTION = SETTING.SHIPMENT_COLLECTION



# Requests when admin is logged
@app.get("/admin/myShipment", response_class=HTMLResponse)
async def admin_my_shipments(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login")

    if current_user["Role"] !="Admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:        
        links = navigation_links(current_user["Role"])
        data = SHIPMENT_COLLECTION.find()
    
        if data:
            context = {
                "user": current_user,
                "request": request,
                "data": data,
                "links": links
            }
            return TEMPLATES.TemplateResponse("myShipment_Admin.html", context)
        # raise HTTPException(status_code=404, detail="No data found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

#Post Request to find shipment details by email and device id
@app.post("/admin/myShipment/email")
def find_shipments_by_email(request: Request, Email: str = Form(...), Device: str = Form(...), current_user: dict = Depends(get_current_user_from_cookie) ):
    if current_user is None:
        return RedirectResponse(url="/login")
        
    if current_user["Role"] !="Admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
                
    try:
        links = navigation_links(current_user["Role"])
        data = SHIPMENT_COLLECTION.find({"Email_Id":Email,"Device":Device})
        data_list = [item for item in data]
        if not data_list:
            context = {
                "user": current_user,
                "request": request,
                "links": links,
                "message":"No Data Found"
            }
            return TEMPLATES.TemplateResponse("myShipment_Admin.html", context)
        else:
            context = {
                "user": current_user,
                "request": request,
                "links": links,
                "data": data_list
            }
            return TEMPLATES.TemplateResponse("myShipment_Admin.html", context)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid input. Please check your input values.") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


# Get Request for user shipments
@app.get("/myShipment", response_class=HTMLResponse)
async def my_shipments(request: Request, current_user: dict = Depends(get_current_user_from_cookie) ):
    # user = get_current_user_from_cookie(request)
    if current_user is None:
        return RedirectResponse(url="/login")
    
    if current_user["Role"] !="User":
        raise HTTPException(status_code=401, detail="Unauthorized")
         
    try:         
        links = navigation_links(current_user["Role"])
        data = SHIPMENT_COLLECTION.find({"Email_Id":current_user["Email"]})
    
        if data:
            context = {
                "user": current_user,
                "request": request,
                "data": data,
                "links": links     
            }
            return TEMPLATES.TemplateResponse("myshipment.html", context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


# Get Request for Create shipment
@app.get("/createShipment", response_class=HTMLResponse)
def get_shipment_page(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            return RedirectResponse(url="/login")
        
        links = navigation_links(current_user["Role"])
        
        context = {
            "user": current_user,
            "request": request,
            "links":links
        }
        return TEMPLATES.TemplateResponse("createshipment.html", context)   
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


# Post Request for Create shipment
@app.post("/createShipment", response_class=HTMLResponse)
async def create_new_shipment(request: Request, Shipment_Number: int = Form(...), Container_Number: int = Form(...), Route_Details: str = Form(...), Goods_Type: str = Form(...), Device: str = Form(...), Expected_Delivery_Date: str = Form(...), PO_Number: int = Form(...), Delivery_Number: int = Form(...), NDC_Number: int = Form(...), Batch_Id: int = Form(...), Serial_Number_Of_Goods: int = Form(...), Description: str = Form(...), current_user: dict = Depends(get_current_user_from_cookie)):                            
    # user = get_current_user_from_cookie(request)
    try:
        if current_user is None:
            return RedirectResponse(url="/login")
        
        links = navigation_links(current_user["Role"])
        new_shipment = Shipment(Email_Id = current_user["Email"],Shipment_Number=Shipment_Number, Container_Number=Container_Number, Route_Details=Route_Details, Goods_Type=Goods_Type, Device=Device, Expected_Delivery_Date=Expected_Delivery_Date, PO_Number=PO_Number, Delivery_Number=Delivery_Number, NDC_Number=NDC_Number, Batch_Id=Batch_Id, Serial_Number_Of_Goods=Serial_Number_Of_Goods, Description=Description)
        
        data = SHIPMENT_COLLECTION.find_one({"Shipment_Number":Shipment_Number})
    
        if not data:
            SHIPMENT_COLLECTION.insert_one(new_shipment.dict())
            return TEMPLATES.TemplateResponse("createshipment.html", {"request": request, "links":links,"user":current_user, "message": " Your shipment has been created successfully"})
        return TEMPLATES.TemplateResponse("createshipment.html", {"request": request, "links":links,"user":current_user, "message": "*Shipment Number already exists"})
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid input. Please check your input values.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(exception)}") from exception
