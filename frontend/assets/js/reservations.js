document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "../auth/login.html"; return; }
    setReservationDateLimits();
    if (document.getElementById("reservationTableBody")) loadReservations();
    if (document.getElementById("reservationDetails")) loadReservationView();
    const createForm = document.getElementById("reservationForm");
    if (createForm) {
        createForm.addEventListener("submit", createReservation);
        await Promise.all([loadGuests(), loadRooms("roomId")]);
    }
    const editForm = document.getElementById("editReservationForm");
    if (editForm) {
        editForm.addEventListener("submit", updateReservation);
        await loadReservationForEdit();
    }
});


function reservationEscape(value) { const el = document.createElement("div"); el.textContent = value ?? ""; return el.innerHTML; }

async function reservationApi(url, options = {}) {
    options.headers = { ...(options.headers || {}), Authorization: `Bearer ${getToken()}` };
    const response = await fetch(url, options);
    let result;
    try { result = await response.json(); } catch (_) { throw new Error("The server returned an invalid response"); }
    if (!response.ok || !result.success) {
        const detail = Array.isArray(result.detail) ? result.detail.map(x => x.msg).join(", ") : result.detail;
        throw new Error(detail || result.message || "Reservation request failed");
    }
    return result.data;
}


function setReservationDateLimits() {
    const today = new Date().toISOString().slice(0, 10);
    const createCheckIn = document.getElementById("checkIn");
    if (createCheckIn) createCheckIn.min = today;
    [["checkIn", "checkOut"], ["editCheckIn", "editCheckOut"]].forEach(([startId, endId]) => {
        const start = document.getElementById(startId), end = document.getElementById(endId);
        if (!start || !end) return;
        start.addEventListener("change", () => { end.min = start.value; if (end.value && end.value <= start.value) end.value = ""; });
    });
}


async function loadGuests() {
    const select = document.getElementById("guestId");
    try {
        const guests = await reservationApi(`${API_BASE_URL}/guests`);
        select.innerHTML = '<option value="">Select a guest</option>' + guests.map(x => `<option value="${x.id}">${reservationEscape(x.name)} - ${reservationEscape(x.phone)}</option>`).join("");
    } catch (error) { showFormError("reservationFormError", error); }
}


async function loadRooms(selectId, selectedId = "") {
    const select = document.getElementById(selectId);
    const rooms = await reservationApi(`${API_BASE_URL}/rooms`);
    select.innerHTML = '<option value="">Select a room</option>' + rooms.filter(x => x.is_active).map(x => `<option value="${x.id}" ${x.id === selectedId ? "selected" : ""}>${reservationEscape(x.room_number)} - ${reservationEscape(x.room_type)}</option>`).join("");
}


function reservationPayload(prefix = "") {
    const get = name => document.getElementById(prefix ? prefix + name : name.charAt(0).toLowerCase() + name.slice(1));
    return { room_id: get("RoomId").value, check_in: get("CheckIn").value, check_out: get("CheckOut").value,
        adults: Number(get("Adults").value), children: Number(get("Children").value), special_request: get("SpecialRequest").value.trim() };
}


async function createReservation(event) {
    event.preventDefault(); const button = document.getElementById("saveReservationButton");
    const data = reservationPayload(""); data.guest_id = document.getElementById("guestId").value;
    button.disabled = true; button.textContent = "Saving...";
    try { await reservationApi(`${API_BASE_URL}/reservations`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }); location.href = "index.html"; }
    catch (error) { showFormError("reservationFormError", error); button.disabled = false; button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Reservation'; }
}


async function loadReservationForEdit() {
    const id = new URLSearchParams(location.search).get("id");
    if (!id) { showFormError("editReservationError", new Error("Missing reservation ID")); return; }
    try {
        const item = await reservationApi(`${API_BASE_URL}/reservations/${encodeURIComponent(id)}`);
        await loadRooms("editRoomId", item.room_id);
        document.getElementById("editCheckIn").value = item.check_in;
        document.getElementById("editCheckOut").value = item.check_out;
        document.getElementById("editCheckOut").min = item.check_in;
        document.getElementById("editAdults").value = item.adults;
        document.getElementById("editChildren").value = item.children;
        document.getElementById("editSpecialRequest").value = item.special_request;
        document.getElementById("editStatus").value = item.status;
        document.getElementById("bookingReference").textContent = `${item.booking_id} · ${item.guest_name}`;
    } catch (error) { showFormError("editReservationError", error); }
}


async function updateReservation(event) {
    event.preventDefault(); const id = new URLSearchParams(location.search).get("id"); const button = document.getElementById("updateReservationButton");
    const data = reservationPayload("edit"); data.status = document.getElementById("editStatus").value;
    button.disabled = true; button.textContent = "Saving...";
    try { await reservationApi(`${API_BASE_URL}/reservations/${encodeURIComponent(id)}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }); location.href = "index.html"; }
    catch (error) { showFormError("editReservationError", error); button.disabled = false; button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes'; }
}


async function loadReservations() {
    const table = document.getElementById("reservationTableBody");
    try { const items = await reservationApi(`${API_BASE_URL}/reservations`); table.innerHTML = items.length ? items.map(x => `<tr><td>${reservationEscape(x.booking_id)}</td><td>${reservationEscape(x.guest_name)}</td><td>${reservationEscape(x.room_number)}</td><td>${x.check_in}</td><td>${x.check_out}</td><td><span class="badge ${x.status === "Cancelled" ? "badge-danger" : "badge-success"}">${reservationEscape(x.status)}</span></td><td><a href="view.html?id=${encodeURIComponent(x.id)}" class="btn btn-primary btn-sm">View</a> <a href="edit.html?id=${encodeURIComponent(x.id)}" class="btn btn-warning btn-sm">Edit</a> <button class="btn btn-danger btn-sm" onclick="cancelReservation('${x.id}')">Cancel</button></td></tr>`).join("") : '<tr><td colspan="7">No reservations found.</td></tr>'; }
    catch (error) { table.innerHTML = `<tr><td colspan="7">${reservationEscape(error.message)}</td></tr>`; }
}


async function loadReservationView() {
    const id = new URLSearchParams(location.search).get("id"), container = document.getElementById("reservationDetails");
    try { const x = await reservationApi(`${API_BASE_URL}/reservations/${encodeURIComponent(id)}`); container.innerHTML = `<p><strong>Booking ID:</strong> ${reservationEscape(x.booking_id)}</p><p><strong>Guest:</strong> ${reservationEscape(x.guest_name)}</p><p><strong>Room:</strong> ${reservationEscape(x.room_number)}</p><p><strong>Check In:</strong> ${x.check_in}</p><p><strong>Check Out:</strong> ${x.check_out}</p><p><strong>Guests:</strong> ${x.adults} adults, ${x.children} children</p><p><strong>Status:</strong> ${reservationEscape(x.status)}</p>`; }
    catch (error) { container.textContent = error.message; }
}


async function cancelReservation(id) { if (!confirm("Cancel this reservation?")) return; try { await reservationApi(`${API_BASE_URL}/reservations/${encodeURIComponent(id)}/cancel`, { method: "PUT" }); loadReservations(); } catch (error) { alert(error.message); } }
function showFormError(id, error) { const box = document.getElementById(id); if (box) box.textContent = error.message; }
