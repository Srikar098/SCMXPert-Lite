from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.models import User
from datetime import datetime, timedelta
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from configuration.configuration import SETTING
from fastapi.exceptions import HTTPException

# Load environment variables from the .env file
load_dotenv()

app = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

# Connect to MongoDB
CLIENT = SETTING.CLIENT
USERS_COLLECTION = SETTING.USERS_COLLECTION


# Get Request for Login 
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return TEMPLATES.TemplateResponse("login.html", {"request": request})


#Post Request for User SignUp
@app.post("/signup", response_class=HTMLResponse)
def user_signup(request: Request, Full_Name: str = Form(...), Email: str = Form(...), Password: str = Form(...), cPassword: str = Form(...)):
    
    hashed_password = hash_password(Password)
    user = User(Full_Name=Full_Name, Email=Email, Password=hashed_password,cPassword=hashed_password, Role="User")
    data = USERS_COLLECTION.find_one({"Email":Email})
    try:
        if not data and (Password == cPassword):
            USERS_COLLECTION.insert_one(user.dict())
            return TEMPLATES.TemplateResponse("login.html", {"request":request, "message":"Successfully Registered! You can Login Now."})
        return TEMPLATES.TemplateResponse("login.html", {"request":request, "message":"Email already exists"})
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing parameter: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


#User Authentication 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Function for hashing password
def hash_password(password: str):
    return PWD_CONTEXT.hash(password)

#Function to verify given password and hashed password
def verify_password(password: str, hashed_password: str):
    return PWD_CONTEXT.verify(password, hashed_password)

#Function to check whether is email is present in database or not
def get_user(email: str):
    user = USERS_COLLECTION.find_one({"Email":email})
    if user:
        return user
    return None

#Function to verify user login details
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['Password']):
        return False
    return user


#Post Request for User Login
@app.post("/login", response_class=HTMLResponse)
async def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=400, detail="Missing username")
    email = form_data.username
    password = form_data.password
    user = authenticate_user(email, password)
    try: 
        if not user:
            return TEMPLATES.TemplateResponse("login.html", {"request": request, "message":"Invalid Email or Password"})
        access_token = create_access_token(data={"sub": user["Email"], "Role": user["Role"]})
        response = Response()
        response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
        response.set_cookie(key=SETTING.COOKIE_NAME, value=access_token, httponly=True)
        return response
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing parameter: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
            


#Function to generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=SETTING.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTING.SECRET_KEY, algorithm=SETTING.ALGORITHM)
    return encoded_jwt

#Function to decode the JWT Token
def decode_access_token(token: str):
    
    try:
        payload = jwt.decode(token, SETTING.SECRET_KEY, algorithms=[SETTING.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

#Function to check user and return the details of user
def get_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    if not token:
        return None
    
    payload = decode_access_token(token) 
    username = payload.get("sub")
    role = payload.get("Role")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if user["Role"] != role:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user

def get_current_user_from_cookie(request: Request) -> User:
    token = request.cookies.get(SETTING.COOKIE_NAME)
    user = get_user_from_token(token)
    return user

#Function for displaying navigation bar based on role
def navigation_links(current_user_role):
    if current_user_role == "Admin":
        return [{"name": "Dashboard", "url": "/dashboard", "icon":"bx bxs-grid-alt"}, {"name": "My Account", "url": "/myAccount", "icon":"bx bxs-user"}, {"name": "My Shipment", "url": "/admin/myShipment", "icon":"bx bx-file"}, {"name": "New Shipment", "url": "/createShipment", "icon":"bx bxs-truck"}, {"name": "Device Data", "url": "/device_data_stream", "icon":"bx bxs-server"}, {"name": "Logout", "url": "/logout", "icon":"bx bx-log-out"}]
    elif current_user_role == "User":
        return [{"name": "Dashboard", "url": "/dashboard", "icon":"bx bxs-grid-alt"}, {"name": "My Account", "url": "/myAccount", "icon":"bx bxs-user"}, {"name": "My Shipment", "url": "/myShipment", "icon":"bx bx-file"}, {"name": "New Shipment", "url": "/createShipment", "icon":"bx bxs-truck"}, {"name": "Logout", "url": "/logout", "icon":"bx bx-log-out"}]
    else:
        return None

#Function for displaying dashboard based on role
def dashboard_links(current_user_role):
    if current_user_role == "Admin":
        return [{"url":"/admin/myShipment"}]
    elif current_user_role == "User":
        return [{"url":"/myShipment"}]
    else:
        return None

#Get Request for Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    
    if current_user is None:
        # raise HTTPException(status_code=401, detail="You must be logged in to access this page.")
        return RedirectResponse(url="/login")
    
    try:   
        links = navigation_links(current_user["Role"])
        d_links = dashboard_links(current_user["Role"])
        context = {
            "user": current_user,
            "request": request,
            "links": links,
            "d_links": d_links
        }
        return TEMPLATES.TemplateResponse("dashboard.html", context)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception


#Get Request for My Account
@app.get("/myAccount", response_class=HTMLResponse)
async def my_account(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            # raise HTTPException(status_code=401, detail="You must be logged in to access this page.")
            return RedirectResponse(url="/login")
        
        links = navigation_links(current_user["Role"])
        # user = get_current_user_from_cookie(request)   
        data = USERS_COLLECTION.find_one({"Email":current_user["Email"]})
        if data: 
            context = {
                "user": current_user,
                "request": request,
                "data":data,
                "links":links
            }
            return TEMPLATES.TemplateResponse("myaccount.html", context)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
    
#Function for logout
@app.get("/logout", response_class=HTMLResponse)
def logout_get(response: Response):
    try:
        response = RedirectResponse(url="/login")
        response.delete_cookie(SETTING.COOKIE_NAME)
        return response
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception


#Get Request for Forgot Password
@app.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    return TEMPLATES.TemplateResponse("forgotpassword.html",{"request": request})


#Post Request for Forgot Password
@app.post("/forgot_password",response_class=HTMLResponse)
def forgot_password_auth(request: Request, Email: str = Form(...), Password: str = Form(...), cPassword: str = Form(...)):
    hashed_password = hash_password(Password)
    data = USERS_COLLECTION.find_one({"Email":Email})
    try:
        if not data:
            return TEMPLATES.TemplateResponse("forgotpassword.html", {"request":request, "message":"Invalid Email Address"})
        else:
            old_password = data["Password"]
            if verify_password(Password, old_password):
                return TEMPLATES.TemplateResponse("forgotpassword.html",{"request": request, 'message': 'Old password cannot be a new password.'})
            USERS_COLLECTION.update_one({"Email":Email},{"$set": {"Password": hashed_password}})
            return TEMPLATES.TemplateResponse("forgotpassword.html", {"request":request, "message":"Successfully Reset Password"})
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception