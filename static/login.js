console.log("Javascript werkt");

document.getElementById("loginbtn").addEventListener("click", function(event) {
event.preventDefault();

let email = document.getElementById("user").value;
let password = document.getElementById("pass").value;

console.log(email, password)
});