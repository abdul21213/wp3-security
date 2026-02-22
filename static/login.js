console.log("Javascript werkt");

document.getElementById("loginbtn").addEventListener("click", function(event) {
event.preventDefault();

let email = document.getElementById("user").value;
let password = document.getElementById("pass").value;

let dummyemail = "student@test.nl"
let dummypassword = "test123"

let errordiv = document.getElementById("errormessage");


if (email === dummyemail && password === dummypassword) {
    errordiv.textContent = "";
    console.log("Login gelukt!");}
else {
    errordiv.textContent = "Ongeldige inloggegevens.";}

});