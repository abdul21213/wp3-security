console.log("Javascript werkt");

let studentbtn = document.getElementById("loginbtn");

if (studentbtn) {
    studentbtn.addEventListener("click", function(event) {
        event.preventDefault();

        let email = document.getElementById("user").value;
        let password = document.getElementById("pass").value;

        let dummyemail = "student@test.nl"
        let dummypassword = "student123"

        let errordiv = document.getElementById("errormessage");


        if (email === dummyemail && password === dummypassword) {
            errordiv.textContent = "";
            window.location.href = "/set-role/student";
        } else {
            errordiv.textContent = "Ongeldige inloggegevens.";
        }
    });
}

let docentbtn = document.getElementById("loginbtn-docent");

if (docentbtn) {
    docentbtn.addEventListener("click", function(event) {
        event.preventDefault();

        let email = document.getElementById("user").value;
        let password = document.getElementById("pass").value;

        let dummyemail = "docent@test.nl"
        let dummypassword = "docent123";

        let errordiv = document.getElementById("errormessage");

        if (email === dummyemail && password === dummypassword) {
            errordiv.textContent = "";
            window.location.href = "/set-role/docent";
        } else {
            errordiv.textContent = "Ongeldige inloggegevens!";
        }
    });
}