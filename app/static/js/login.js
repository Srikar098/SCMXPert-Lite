// Defining a function to display error message
function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
};

// Defining a function to validate login form 
function validateLogin() {
    // Retrieving the values of form elements 
    var email = document.loginForm.username.value;
    var password = document.loginForm.password.value;
    // var recaptcha = document.loginForm.recaptcha;

    var response = grecaptcha.getResponse();

    // var recaptcha = response;

    // Defining error variables with a default value
    var emailErr = passErr = true;
    var recaptchaErr = true;

    //Validate email
    if(email == ""){
        printError("emailErr", "* Please enter your email address");
    }    else {
        // Regular expression for basic email validation
        var regex = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if(regex.test(email) === false) {
            printError("emailErr", "* Please enter a valid email address");
        } else{
            printError("emailErr", "");
            emailErr = false;
        }
    }

    //Validate password
    if(password == ""){
        printError("passErr", "* Please enter your password");
    }else if(password.length < 8) {
        printError("passErr", "* Password length must be at least 8 characters");
    }else if(password.length >16) {
        printError("passErr", "* Password length must not exceed 16 characters");
    } else { 
        printError("passErr", "");
        passErr = false;
    }

    if(response.length == 0){
        printError("recaptchaErr", "* Please confirm recaptcha");
    } else {
        printError("recaptchaErr", "");
        recaptchaErr = false;
    }

    // Prevent the form from being submitted if there are any errors
    if((emailErr || passErr || recaptchaErr) == true ){
        return false;
    } else {
        document.getElementById("loginForm").submit();
    }
    
};

function validateSignup() {


    // Retrieving the values of form elements 
    var fullName = document.signupForm.Full_Name.value;
    var email = document.signupForm.Email.value;
    var password = document.signupForm.Password.value;
    var rePassword = document.signupForm.cPassword.value;

    // var fullName = document.querySelector('#fullName').value;
    // var email = document.querySelector('#signup-email').value;
    // var newPassword = document.querySelector('#new-password').value;
    // var cPassword = document.querySelector('#confirm-password').value;

    // Defining error variables with a default value
    var fullNameErr = true;
    var emailAddErr = true;
    var newPassErr = true;
    var rePassErr = true;

    //Validate full name
    if(fullName == "") {
        printError("fullNameErr", "* Please enter your name");
    } else {
        var regex = /^[a-zA-Z\s]+$/;                
        if(regex.test(fullName) === false) {
            printError("fullNameErr", "* Please enter a valid name");
        } else {
            printError("fullNameErr", "");
            fullNameErr = false;
        }
    }

    //Validate email
    if(email == ""){
        printError("emailAddErr", "* Please enter your email address");
    } else {
        // Regular expression for basic email validation
        var regex = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if(regex.test(email) === false) {
            printError("emailAddErr", "* Please enter a valid email address");
        } else{
            printError("emailAddErr", "");
            emailAddErr = false;
        }
    }

    //Validate password
    if(password == ""){
        printError("newPassErr", "* Please enter your password");
    } else if(password.length < 8) {
        printError("newPassErr", "* Password length must be at least 8 characters");
    } else if(password.length > 16) {
        printError("newPassErr", "* Password length must not exceed 16 characters");
    } else { 
        printError("newPassErr", "");
        newPassErr = false;
    }

    //Validate confirm password
    if(rePassword == ""){
        printError("rePassErr", "* Please enter your password");
    }else if(rePassword != password){
        printError("rePassErr", "* Password doesn't match")
    } else{
        printError("rePassErr", "");
        rePassErr = false;
    }

    if((fullNameErr || emailAddErr || newPassErr || rePassErr) == true ){
        return false;
    }
    else {
        document.getElementById("signupForm").submit();
    }

};

