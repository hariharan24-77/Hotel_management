/* ==========================================================
   HOTEL MANAGEMENT SYSTEM

   Authentication Module

   Handles:
   - Administrator Setup
   - User Login
   - JWT Token
   - Session Management
   - Logout

========================================================== */



// ==========================================================
// ADMINISTRATOR SETUP
// ==========================================================


const setupForm = document.getElementById("setupForm");


if(setupForm){


    setupForm.addEventListener(
        "submit",
        async function(event){


            event.preventDefault();



            const name =
            document.getElementById("name").value.trim();


            const email =
            document.getElementById("email").value.trim();


            const username =
            document.getElementById("username").value.trim();


            const password =
            document.getElementById("password").value;


            const confirmPassword =
            document.getElementById("confirmPassword").value;




            if(
                !name ||
                !email ||
                !username ||
                !password ||
                !confirmPassword
            ){

                showError(
                    "All fields are required",
                    "errorMessage"
                );

                return;

            }




            if(password !== confirmPassword){


                showError(
                    "Passwords do not match",
                    "errorMessage"
                );


                return;

            }





            try{


                const response =
                await fetch(
                    `${API_BASE_URL}/auth/setup`,
                    {


                        method:"POST",


                        headers:{


                            "Content-Type":
                            "application/json"


                        },


                        body:JSON.stringify({


                            name,

                            email,

                            username,

                            password


                        })


                    }
                );



                const data =
                await response.json();




                if(response.ok){


                    Toast.success(
                        "Administrator created successfully"
                    );


                    window.location.href =
                    "login.html";


                }

                else{


                    showError(
                        data.message ||
                        "Setup failed",
                        "errorMessage"
                    );


                }




            }


            catch(error){


                showError(
                    "Server connection failed",
                    "errorMessage"
                );


                console.error(error);


            }



        }
    );

}



// ==========================================================
// LOGIN
// ==========================================================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document
            .getElementById("email")
            .value
            .trim();

        const password = document
            .getElementById("password")
            .value
            .trim();

        const remember = document.getElementById("remember")?.checked || false;

        // Validation
        if (!email) {
            showError("Email is required", "loginError");
            return;
        }

        const emailRegex =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            showError("Enter a valid email address", "loginError");
            return;
        }

        if (!password) {
            showError("Password is required", "loginError");
            return;
        }

        const button = document.getElementById("loginButton");

        button.disabled = true;
        button.innerHTML = "Logging in...";

        try {

            const response = await fetch(API.LOGIN, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    email: email,
                    password: password

                })

            });

            const result = await response.json();

            if (response.ok && result.success) {

                saveAuthData(result.data, remember);

                window.location.href = "../dashboard/index.html";

            }
            else {

                showError(
                    result.message || result.detail || "Invalid email or password",
                    "loginError"
                );

            }

        }
        catch (error) {

            console.error(error);

            showError(
                "Unable to connect to server",
                "loginError"
            );

        }
        finally {

            button.disabled = false;
            button.innerHTML = "Login";

        }

    });

}


// ==========================================================
// SAVE AUTH DATA
// ==========================================================


function saveAuthData(data, remember = false) {

    // Never leave an older token in the other storage: getToken must have
    // exactly one authoritative session to read.
    clearAuthStorage();

    const storage = remember
        ? localStorage
        : sessionStorage;

    storage.setItem(
        "access_token",
        data.access_token
    );

    storage.setItem(
        "role",
        data.role
    );

    storage.setItem(
        "role_id",
        data.role_id
    );

    storage.setItem(
        "user",
        JSON.stringify(data.user)
    );

}

// ==========================================================
// TOKEN
// ==========================================================


function getToken(){
    const sessionToken = sessionStorage.getItem("access_token");
    const rememberedToken = localStorage.getItem("access_token");
    const token = sessionToken || rememberedToken;

    if (token && isTokenExpired(token)) {
        clearAuthStorage();
        return null;
    }
    return token;
}

function isTokenExpired(token) {
    try {
        let encoded = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
        encoded += "=".repeat((4 - encoded.length % 4) % 4);
        const payload = JSON.parse(atob(encoded));
        return !payload.exp || payload.exp * 1000 <= Date.now();
    } catch (_) {
        return true;
    }
}

function clearAuthStorage() {
    [localStorage, sessionStorage].forEach(storage => {
        ["access_token", "user", "role", "role_id"].forEach(key => storage.removeItem(key));
    });
}

function redirectToLogin() {
    clearAuthStorage();
    window.location.href = "../auth/login.html?session=expired";
}






function getCurrentUser(){



    const user =


    localStorage.getItem("user")

    ||

    sessionStorage.getItem("user");




    return user
    ? JSON.parse(user)
    : null;


}







// ==========================================================
// LOGOUT
// ==========================================================


function logout(){
    clearAuthStorage();
    window.location.href =
    "../auth/login.html";



}






// ==========================================================
// PASSWORD SHOW / HIDE
// ==========================================================



const togglePassword =
document.getElementById(
    "togglePassword"
);



if(togglePassword){



    togglePassword.addEventListener(
        "click",
        function(){



            const passwordInput =
            document.getElementById(
                "loginPassword"
            );



            const icon =
            togglePassword.querySelector(
                "i"
            );




            if(
                passwordInput.type === "password"
            ){



                passwordInput.type =
                "text";



                icon.classList.remove(
                    "fa-eye"
                );



                icon.classList.add(
                    "fa-eye-slash"
                );



            }


            else{



                passwordInput.type =
                "password";



                icon.classList.remove(
                    "fa-eye-slash"
                );



                icon.classList.add(
                    "fa-eye"
                );


            }




        }
    );



}






// ==========================================================
// ERROR DISPLAY
// ==========================================================


function showError(
    message,
    elementId
){


    const box =
    document.getElementById(
        elementId
    );



    if(box){



        box.innerText =
        message;



        box.style.display =
        "block";


    }


}
