// Defining a function to display error message
function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
};

const forgotPasswordForm = document.getElementById("forgot-password-form");
const otpForm = document.getElementById("otp-form");
const resetPasswordForm = document.getElementById("reset-password-form");

// forgotPasswordForm.addEventListener("submit", (event) => {
    
//     event.preventDefault();

//     const email = document.getElementById("Email").value;
//         fetch("/forgot_password", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ email })
//         })
//         .then(response => response.json())
//         .then(data => {
//         //   errorMessage.style.display = "none";
//           otpForm.style.display = "block";
//           forgotPasswordForm.style.display = "none";
//         })
//     // otpForm.style.display = "block";
//     // forgotPasswordForm.style.display = "none";
// });

// otpForm.addEventListener("submit", (event) => {
//     event.preventDefault();
//     otpForm.style.display = "none";
//     resetPasswordForm.style.display = "block";
// });



function validateEmail(){
    var email = document.forgotPasswordForm.Email.value;

    var emailErr = true;

    if(email == ""){
        printError("emailErr", "* Please enter your email address");
    }
    else {
        // Regular expression for basic email validation
        var regex = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if(regex.test(email) === false) {
            printError("emailErr", "* Please enter a valid email address");
        } else{
            printError("emailErr", "");
            emailErr = false;
        }
    }

    if(emailErr == true){
        return false;
    } else {
        document.getElementById("forgotPasswordForm").submit();
    }

};

function validateOTP(){
    var otp = document.otpForm.otp.value;
    var otpErr = true;

    if(!otp){
        printError("otpErr", "* Please enter your OTP");
    } else if(otp.length < 6 || otp.length > 6 ){
        printError("otpErr", "* Please enter valid OTP");
    } else {
        printError("otpErr", "");
        otpErr = false;
    }

    if(otpErr == true){
        return false;
    } else {
        document.getElementById("otpForm").submit();
    }

};

function validatePassword(){
    var password = document.resetPasswordForm.Password.value;
    var cPassword = document.resetPasswordForm.cPassword.value;

    var passwordErr = true;
    var cPasswordErr = true;

    if(password == ""){
        printError("passwordErr", "* Please enter your password");
    } else if(password.length < 8) {
        printError("passwordErr", "* Password length must be at least 8 characters");
    } else if(password.length > 16) {
        printError("passwordErr", "* Password length must not exceed 16 characters");
    } else { 
        printError("passwordErr", "");
        passwordErr = false;
    }

    //Validate confirm password
    if(cPassword == ""){
        printError("cPasswordErr", "* Please enter your password");
    }else if(cPassword != password){
        printError("cPasswordErr", "* Password doesn't match")
    } else{
        printError("cPasswordErr", "");
        cPasswordErr = false;
    }

    if((passwordErr || cPasswordErr) == true ){
        return false;
    }
    else {
        document.getElementById("resetPasswordForm").submit();
    }
};

