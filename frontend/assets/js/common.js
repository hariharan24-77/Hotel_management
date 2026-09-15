/* ==========================================================
   HOTEL MANAGEMENT SYSTEM

   Common JavaScript Module

   Handles:
   - Component Loading
   - Layout Management
   - Common UI Functions

========================================================== */



// ==========================================================
// LOAD COMPONENTS
// ==========================================================


document.addEventListener(
    "DOMContentLoaded",
    function(){


        loadComponent(
            "sidebar-container",
            "../../components/sidebar.html"
        );


        loadComponent(
            "navbar-container",
            "../../components/navbar.html"
        );


        loadComponent(
            "footer-container",
            "../../components/footer.html"
        );


    }
);






// ==========================================================
// COMPONENT LOADER
// ==========================================================


async function loadComponent(
    elementId,
    filePath
){

    // Support legacy pages that passed (filePath, elementId).
    if (typeof elementId === "string" && elementId.endsWith(".html")) {
        const originalPath = elementId;
        elementId = filePath;
        filePath = originalPath;
    }



    const element =
    document.getElementById(
        elementId
    );



    if(!element){

        return;

    }





    try{


        const response =
        await fetch(filePath);




        if(!response.ok){


            throw new Error(
                "Component loading failed"
            );


        }





        const html =
        await response.text();




        element.innerHTML =
        html;

        document.dispatchEvent(new CustomEvent("componentLoaded", {
            detail: { elementId }
        }));




        setActiveMenuByModule();



    }


    catch(error){



        console.error(

            "Component Error:",
            error

        );


    }



}






// ==========================================================
// ACTIVE MENU
// ==========================================================


function setActiveMenu(){



    const currentPage =
    window.location.pathname;




    const menuItems =
    document.querySelectorAll(
        ".menu-item"
    );




    menuItems.forEach(
        item => {



            const link =
            item.getAttribute(
                "href"
            );



            if(
                link &&
                currentPage.includes(
                    link.replace(
                        "../",
                        ""
                    )
                )
            ){



                item.classList.add(
                    "active"
                );



            }



        }
    );


}






// ==========================================================
// DATE FORMAT
// ==========================================================


function formatDate(
    date
){


    return new Date(date)
    .toLocaleDateString(
        "en-IN",
        {

            day:"2-digit",

            month:"short",

            year:"numeric"

        }
    );


}






// ==========================================================
// CURRENCY FORMAT
// ==========================================================


function formatCurrency(
    amount
){


    return new Intl.NumberFormat(
        "en-IN",
        {

            style:"currency",

            currency:"INR"

        }

    ).format(amount);


}






// ==========================================================
// DELETE CONFIRMATION
// ==========================================================


function confirmDelete(
    message="Are you sure you want to delete?"
){



    return confirm(
        message
    );


}






// ==========================================================
// SHOW ELEMENT
// ==========================================================


function showElement(
    id
){



    const element =
    document.getElementById(id);



    if(element){


        element.style.display =
        "block";


    }


}






// ==========================================================
// HIDE ELEMENT
// ==========================================================


function hideElement(
    id
){



    const element =
    document.getElementById(id);



    if(element){


        element.style.display =
        "none";


    }


}






// ==========================================================
// TOGGLE SIDEBAR
// ==========================================================


function toggleSidebar(){



    const sidebar =
    document.getElementById(
        "sidebar"
    );



    if(sidebar){


        sidebar.classList.toggle(
            "collapsed"
        );


    }


}


// ==========================================================
// FOOTER YEAR
// ==========================================================


function setFooterYear(){


    const yearElement =
    document.getElementById(
        "currentYear"
    );



    if(yearElement){


        yearElement.innerText =
        new Date().getFullYear();


    }


}



document.addEventListener(
    "DOMContentLoaded",
    setFooterYear
);


// ==========================================================
// LOADER CONTROL
// ==========================================================


function showLoader(){


    const loader =
    document.getElementById(
        "globalLoader"
    );


    if(loader){


        loader.style.display =
        "flex";


    }


}





function hideLoader(){


    const loader =
    document.getElementById(
        "globalLoader"
    );


    if(loader){


        loader.style.display =
        "none";


    }


}


// ==========================================================
// TOAST NOTIFICATION
// ==========================================================



function showToast(
    message,
    type="success"
){



    const container =
    document.getElementById(
        "toastContainer"
    );



    if(!container){

        return;

    }





    const toast =
    document.createElement(
        "div"
    );



    toast.className =
    `toast toast-${type}`;



    toast.innerHTML = `

        <span>

            ${message}

        </span>

    `;



    container.appendChild(
        toast
    );




    setTimeout(
        function(){


            toast.remove();


        },

        3000

    );



}

function setActiveMenuByModule() {
    const currentPath = window.location.pathname.replaceAll("\\", "/");
    const currentModule = currentPath.match(/\/pages\/([^/]+)\//)?.[1];
    const currentFile = currentPath.split("/").pop() || "index.html";

    let targetFile = "index.html";
    if (currentModule === "checkin_checkout") targetFile = currentFile === "checkout.html" ? "checkout.html" : "checkin.html";
    if (currentModule === "billing") targetFile = currentFile === "payments.html" ? "payments.html" : "index.html";
    if (currentModule === "reports") targetFile = "dashboard.html";

    let activeAssigned = false;
    document.querySelectorAll(".sidebar-menu .menu-item").forEach(item => {
        item.classList.remove("active");
        const href = (item.getAttribute("href") || "").replaceAll("\\", "/");
        const linkModule = href.match(/\.\.\/([^/]+)\//)?.[1];
        const linkFile = href.split("/").pop();
        if (!activeAssigned && currentModule && linkModule === currentModule && linkFile === targetFile) {
            item.classList.add("active");
            activeAssigned = true;
        }
    });
}
