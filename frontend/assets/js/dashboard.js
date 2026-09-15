/* ==========================================================
   HOTEL MANAGEMENT SYSTEM

   Dashboard Module

   Handles:
   - Authentication Check
   - User Information
   - Dashboard Statistics

========================================================== */



// ==========================================================
// PAGE LOAD
// ==========================================================


document.addEventListener(
    "DOMContentLoaded",
    function(){


        checkAuthentication();


        loadUserDetails();


        loadDashboardData();


    }
);

document.addEventListener("componentLoaded", function () {
    const user = getCurrentUser();
    if (!user) return;
    const navbarName = document.getElementById("navbarUserName");
    const navbarRole = document.getElementById("navbarUserRole");
    if (navbarName) navbarName.innerText = user.name;
    if (navbarRole) navbarRole.innerText = user.role;
});






// ==========================================================
// AUTHENTICATION CHECK
// ==========================================================


function checkAuthentication(){



    const token =
    getToken();



    if(!token){



        window.location.href =
        "../auth/login.html";



    }


}






// ==========================================================
// LOAD USER DETAILS
// ==========================================================


async function loadUserDetails(){



    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) return;
        const user = result.data;
        const storage = localStorage.getItem("access_token") ? localStorage : sessionStorage;
        storage.setItem("user", JSON.stringify(user));




    if(user){



        const welcome =
        document.getElementById(
            "welcomeText"
        );



        if(welcome){


            welcome.innerText =
            `Welcome back, ${user.name} (${user.role})`;


        }

        const navbarName = document.getElementById("navbarUserName");
        const navbarRole = document.getElementById("navbarUserRole");
        if (navbarName) navbarName.innerText = user.name;
        if (navbarRole) navbarRole.innerText = user.role;



    }

    } catch (error) {
        console.error("User loading error:", error);
    }


}






// ==========================================================
// LOAD DASHBOARD SUMMARY
// ==========================================================


async function loadDashboardData(){



    try{



        const token =
        getToken();




        const response =
        await fetch(

            `${API_BASE_URL}/dashboard/summary`,

            {


                method:"GET",



                headers:{


                    "Authorization":
                    `Bearer ${token}`


                }


            }

        );





        const data =
        await response.json();





        if(response.ok){



            updateDashboardCards(data.data);



        }


        else{


            console.error(
                data.message
            );


        }



    }


    catch(error){



        console.error(

            "Dashboard Loading Error:",
            error

        );


    }



}






// ==========================================================
// UPDATE CARDS
// ==========================================================


function updateDashboardCards(
    data
){



    const totalRooms =
    document.getElementById(
        "totalRooms"
    );



    const availableRooms =
    document.getElementById(
        "availableRooms"
    );



    const occupiedRooms =
    document.getElementById(
        "occupiedRooms"
    );



    const reservations =
    document.getElementById(
        "reservations"
    );






    if(totalRooms){


        totalRooms.innerText =
        data.total_rooms || 0;


    }




    if(availableRooms){


        availableRooms.innerText =
        data.available_rooms || 0;


    }




    if(occupiedRooms){


        occupiedRooms.innerText =
        data.occupied_rooms || 0;


    }




    if(reservations){


        reservations.innerText =
        data.today_reservations || 0;


    }



}
