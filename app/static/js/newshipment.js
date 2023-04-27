// Defining a function to display error message
function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
};

// Setting the current date
const currentDate = new Date();
const deliveryDate = document.getElementById("Expected_Delivery_Date");
deliveryDate.value= currentDate.toISOString().slice(0,10);
deliveryDate.min = currentDate.toISOString().slice(0,10);


// Defining a function to validate shipment form 
function validateShipment() {

    // var shipmentNumber = document.shipmentForm.shipmentNumber.value;
    // var containerNumber = document.shipmentForm.containerNumber.value;
    // var routeDetails = document.shipmentForm.routeDetails.value;
    // var goodsType = document.shipmentForm.goodsType.value;
    // var device = document.shipmentForm.device.value;
    // var poNumber = document.shipmentForm.poNumber.value;
    // var deliveryNumber = document.shipmentForm.deliveryNumber.value;
    // var ndcNumber = document.shipmentForm.ndcNumber.value;
    // var batchId = document.shipmentForm.batchId.value;
    // var numberOfGoods = document.shipmentForm.numberOfGoods.value;
    // var description = document.shipmentForm.description.value;

    var shipmentNumber = document.querySelector('#Shipment_Number').value;
    var containerNumber = document.querySelector('#Container_Number').value;
    var routeDetails = document.querySelector('#Route_Details').value;
    var goodsType = document.querySelector('#Goods_Type').value;
    var device = document.querySelector('#Device').value;
    // var deliveryDate = document.querySelector('#Expected_Delivery_Date').value;
    var poNumber = document.querySelector('#PO_Number').value;
    var deliveryNumber = document.querySelector('#Delivery_Number').value;
    var ndcNumber = document.querySelector('#NDC_Number').value;
    var batchId = document.querySelector('#Batch_Id').value;
    var numberOfGoods = document.querySelector('#Serial_Number_Of_Goods').value;
    var description = document.querySelector('#Description').value;

    var shipmentNumberErr = true;       //type number
    var containerNumberErr = true;      //type number
    var routeDetailsErr = true;         //type options
    var goodsTypeErr = true;            //type options
    var deviceErr = true;               //type options
    // var deliveryDateErr = true;         //type date
    var poNumberErr = true;             //type number
    var deliveryNumberErr = true;       //type number
    var ndcNumberErr = true;            //type number
    var batchIdErr = true;              //type number
    var numberOfGoodsErr = true;        //type number
    var descriptionErr = true;          //type textarea

    //Validate shipment number
    if(!shipmentNumber){
        printError("shipmentNumberErr", "* Please enter shipment number");
    } else if(shipmentNumber <= 0 ){
        printError("shipmentNumberErr", "* Please enter valid shipment number");
    } else {
        printError("shipmentNumberErr", "");
        shipmentNumberErr = false;
    }

    //Validate container number
    if(!containerNumber){
        printError("containerNumberErr", "* Please enter container number");
    } else if(containerNumber <= 0){
        printError("containerNumberErr", "* Please enter valid container number");
    } else {
        printError("containerNumberErr", "");
        containerNumberErr = false;
    }

    //Validate route details
    if(routeDetails == "" || routeDetails == "select"){
        printError("routeDetailsErr", "* Please select a route");
    } else {
        printError("routeDetailsErr", "");
        routeDetailsErr = false;
    }

    //Validate goods type
    if(goodsType == "" || goodsType == "select"){
        printError("goodsTypeErr", "* Please select a goods type");
    } else {
        printError("goodsTypeErr", "");
        goodsTypeErr = false;
    }

    //Validate device
    if(device == "" || device == "select"){
        printError("deviceErr", "* Please select a device");
    } else {
        printError("deviceErr", "");
        deviceErr = false;
    }

    //Validate po number 
    if(!poNumber){
        printError("poNumberErr", "* Please enter po number");
    } else if(poNumber <= 0){
        printError("poNumberErr", "* Please enter valid po number");
    } else {
        printError("poNumberErr", "");
        poNumberErr = false;
    }

    //Validate delivery number
    if(!deliveryNumber){
        printError("deliveryNumberErr", "* Please enter delivery number");
    } else if(deliveryNumber <= 0){
        printError("deliveryNumberErr", "* Please enter valid delivery number");
    } else {
        printError("deliveryNumberErr", "");
        deliveryNumberErr = false;
    }
    
    //Validate ndc number
    if(!ndcNumber){
        printError("ndcNumberErr", "* Please enter ndc number");
    } else if(ndcNumber <= 0){
        printError("ndcNumberErr", "* Please enter valid ndc number");
    } else {
        printError("ndcNumberErr", "");
        ndcNumberErr = false;
    }

    //Validate batch id
    if(!batchId){
        printError("batchIdErr", "* Please enter batch Id");
    } else if(batchId <= 0){
        printError("batchIdErr", "* Please enter valid batch Id");
    } else {
        printError("batchIdErr", "");
        batchIdErr = false;
    }

    //Validate serial number of goods
    if(!numberOfGoods){
        printError("numberOfGoodsErr", "* Please enter serial number of goods");
    } else if(numberOfGoods <= 0){
        printError("numberOfGoodsErr", "* Please enter valid serial number");
    } else {
        printError("numberOfGoodsErr", "");
        numberOfGoodsErr = false;
    }

    //Validate description
    if(description == ""){
        printError("descriptionErr","* Please enter shipment description");
    } else {
        var regex = /^[a-zA-Z0-9.,_\s]+$/;
        if(regex.test(description) === false){
            printError("descriptionErr","* Please enter a valid description");
        } else {
            printError("descriptionErr", "");
            descriptionErr = false;
        }
    }


    if((shipmentNumberErr || containerNumberErr || routeDetailsErr || goodsTypeErr || deviceErr || poNumberErr || deliveryNumberErr || ndcNumberErr || batchIdErr || numberOfGoodsErr || descriptionErr) == true ){
        return false;
    } else {
        document.getElementById("shipmentForm").submit();
    }
};

