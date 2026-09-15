const API_BASE_URL = "http://127.0.0.1:8000/api";

document
    .getElementById("loginForm")
    .addEventListener("submit", login);

async function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message || result.detail || "Login Failed");
            return;
        }

        // If using common response wrapper
        const data = result.data || result;

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        localStorage.setItem("role_id", data.role_id);

        alert("Login Successful");

        window.location.href = "../dashboard/dashboard.html";

    } catch (error) {
        console.error(error);
        alert("Unable to connect to the server.");
    }
}