document.addEventListener("DOMContentLoaded", () => {
    if (!getToken()) { window.location.href = "../auth/login.html"; return; }
    setDobLimits();
    if (document.getElementById("guestTableBody")) loadGuests();
    const createForm = document.getElementById("guestForm");
    if (createForm) createForm.addEventListener("submit", event => saveGuest(event, false));
    const editForm = document.getElementById("editGuestForm");
    if (editForm) {
        editForm.addEventListener("submit", event => saveGuest(event, true));
        loadGuestForEdit();
    }
});


function guestEscape(value) {
    const element = document.createElement("div"); element.textContent = value ?? ""; return element.innerHTML;
}

function setDobLimits() {
    const today = new Date();
    const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1);
    const earliest = new Date(today); earliest.setFullYear(today.getFullYear() - 120);
    document.querySelectorAll('input[type="date"][data-dob]').forEach(input => {
        input.max = yesterday.toISOString().slice(0, 10);
        input.min = earliest.toISOString().slice(0, 10);
    });
}

async function apiGuest(url, options = {}) {
    options.headers = { ...(options.headers || {}), "Authorization": `Bearer ${getToken()}` };
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    let response;
    try {
        response = await fetch(url, { ...options, signal: controller.signal });
    } catch (error) {
        if (error.name === "AbortError") throw new Error("The server took too long to respond. Please try again.");
        throw new Error("Cannot reach the hotel server. Check that the backend is running, then try again.");
    } finally {
        clearTimeout(timeout);
    }
    if (response.status === 401) {
        redirectToLogin();
        throw new Error("Your session expired. Please sign in again.");
    }
    let result;
    try { result = await response.json(); }
    catch (_) { throw new Error("The server returned an invalid response. Please try again."); }
    if (!response.ok || !result.success) {
        const detail = Array.isArray(result.detail) ? result.detail.map(item => item.msg).join(", ") : result.detail;
        throw new Error(detail || result.message || "Guest request failed");
    }
    return result.data;
}


async function loadGuests() {
    const table = document.getElementById("guestTableBody");
    try {
        const guests = await apiGuest(`${API_BASE_URL}/guests`);
        table.innerHTML = guests.length ? guests.map(guest => `<tr>
            <td>${guestEscape(guest.name)}</td><td>${guestEscape(guest.phone)}</td>
            <td>${guestEscape(guest.email)}</td><td>${guestEscape(guest.id_proof)}</td>
            <td><a href="edit.html?id=${encodeURIComponent(guest.id)}" class="btn btn-primary btn-sm">Edit</a>
            <button type="button" class="btn btn-danger btn-sm" onclick="deleteGuest('${guest.id}')">Delete</button></td>
        </tr>`).join("") : '<tr><td colspan="5" class="text-center">No guests found.</td></tr>';
    } catch (error) { table.innerHTML = `<tr><td colspan="5" class="text-center">${guestEscape(error.message)}</td></tr>`; }
}


function guestPayload(prefix = "") {
    const id = name => document.getElementById(prefix + name);
    return {
        name: id("GuestName").value.trim(), phone: id("GuestPhone").value.trim(),
        email: id("GuestEmail").value.trim(), gender: id("GuestGender").value,
        dob: id("GuestDob").value, address: id("GuestAddress").value.trim(),
        id_proof_type: id("IdProofType").value, id_proof_number: id("IdProofNumber").value.trim()
    };
}

async function saveGuest(event, editing) {
    event.preventDefault();
    const prefix = editing ? "edit" : "guest";
    const errorBox = document.getElementById(editing ? "editGuestError" : "guestFormError");
    const button = document.getElementById(editing ? "updateGuestButton" : "saveGuestButton");
    const guestId = new URLSearchParams(location.search).get("id");
    errorBox.textContent = ""; button.disabled = true; button.textContent = editing ? "Updating..." : "Saving...";
    try {
        await apiGuest(`${API_BASE_URL}/guests${editing ? `/${encodeURIComponent(guestId)}` : ""}`, {
            method: editing ? "PUT" : "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify(guestPayload(prefix))
        });
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message; button.disabled = false;
        button.innerHTML = editing ? '<i class="fa-solid fa-floppy-disk"></i> Update Guest' : '<i class="fa-solid fa-floppy-disk"></i> Save Guest';
    }
}


async function loadGuestForEdit() {
    const id = new URLSearchParams(location.search).get("id");
    const errorBox = document.getElementById("editGuestError");
    if (!id) { errorBox.textContent = "Missing guest ID"; return; }
    try {
        const guest = await apiGuest(`${API_BASE_URL}/guests/${encodeURIComponent(id)}`);
        const values = { GuestName: guest.name, GuestPhone: guest.phone, GuestEmail: guest.email,
            GuestGender: guest.gender, GuestDob: guest.dob, GuestAddress: guest.address,
            IdProofType: guest.id_proof_type, IdProofNumber: guest.id_proof_number };
        Object.entries(values).forEach(([name, value]) => { document.getElementById(`edit${name}`).value = value; });
    } catch (error) { errorBox.textContent = error.message; }
}


async function deleteGuest(id) {
    if (!confirm("Delete this guest?")) return;
    try { await apiGuest(`${API_BASE_URL}/guests/${encodeURIComponent(id)}`, { method: "DELETE" }); loadGuests(); }
    catch (error) { alert(error.message); }
}
