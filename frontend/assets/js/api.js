// ===============================
// Hotel Management System
// API Configuration
// ===============================

// Change this URL according to your FastAPI server
const BASE_URL = "http://127.0.0.1:8000/api";
const API_BASE_URL = BASE_URL;

// API Endpoints
const API = {
    LOGIN: `${BASE_URL}/auth/login`,
    LOGOUT: `${BASE_URL}/auth/logout`,
    PROFILE: `${BASE_URL}/auth/profile`,

    DASHBOARD: `${BASE_URL}/dashboard`,

    ROOM_TYPES: `${BASE_URL}/room-types`,
    ROOMS: `${BASE_URL}/rooms`,

    GUESTS: `${BASE_URL}/guests`,

    RESERVATIONS: `${BASE_URL}/reservations`,

    CHECKIN: `${BASE_URL}/checkin`,
    CHECKOUT: `${BASE_URL}/checkout`,

    BILLING: `${BASE_URL}/billing`,
    PAYMENTS: `${BASE_URL}/payments`,

    STAFF: `${BASE_URL}/staff`,

    REPORTS: `${BASE_URL}/reports`
};


async function apiGet(url) {

    Loader.show();

    try {

        const headers = {};

        const token = getToken();

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            headers: headers
        });

        return await response.json();

    } finally {

        Loader.hide();

    }
}



async function apiPost(url, data) {

    Loader.show();

    try {

        const headers = {
            "Content-Type": "application/json"
        };

        const token = getToken();

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data)
        });

        return await response.json();

    } finally {

        Loader.hide();

    }
}
