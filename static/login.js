console.log("Javascript werkt");

document.getElementById("loginbtn").addEventListener("click", function(event) {
event.preventDefault();

let email = document.getElementById("user").value;
let password = document.getElementById("pass").value;

let dummyemail = "student@test.nl"
let dummypassword = "test123"

if (email === dummyemail && password === dummypassword) {
    console.log("Login gelukt!");}
else {
    console.log("Login mislukt!")}

});