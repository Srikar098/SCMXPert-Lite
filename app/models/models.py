from pydantic import BaseModel

# User Model
class User(BaseModel):
    Full_Name: str
    Email: str
    Password: str
    Role: str


# New Shipment Model
class Shipment(BaseModel):
    Email_Id: str
    Shipment_Number: int
    Container_Number: int
    Route_Details: str
    Goods_Type: str
    Device: str
    Expected_Delivery_Date: str
    PO_Number: int
    Delivery_Number: int
    NDC_Number: int
    Batch_Id: int
    Serial_Number_Of_Goods: int
    Description: str