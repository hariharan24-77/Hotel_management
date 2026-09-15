document.addEventListener("DOMContentLoaded", () => {
    if (!getToken()) {
        window.location.href = "../auth/login.html";
        return;
    }
    if (document.getElementById("roomTableBody")) loadRooms();
    const form = document.getElementById("roomForm");
    if (form) {
        form.addEventListener("submit", createRoom);
        loadRoomTypes();
    }
    const editForm = document.getElementById("editRoomForm");
    if (editForm) {
        editForm.addEventListener("submit", updateRoom);
        loadRoomForEdit();
    }
});


function roomEscape(value) {
    const element = document.createElement("div");
    element.textContent = value ?? "";
    return element.innerHTML;
}


async function loadRoomTypes() {
    const dropdown = document.getElementById("roomType");
    if (!dropdown) return;
    try {
        const response = await fetch(`${API_BASE_URL}/room-types`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message);
        const activeTypes = result.data.filter(item => item.is_active);
        dropdown.innerHTML = '<option value="">Select a room type</option>' + activeTypes.map(item =>
            `<option value="${roomEscape(item.id)}">${roomEscape(item.name)} — ${formatCurrency(item.base_price)}</option>`
        ).join("");
        dropdown.disabled = activeTypes.length === 0;
        if (!activeTypes.length) throw new Error("Create an active room type before adding a room");
    } catch (error) {
        dropdown.innerHTML = '<option value="">No room types available</option>';
        document.getElementById("roomFormError").textContent = error.message;
    }
}


async function loadRooms() {
    const table = document.getElementById("roomTableBody");
    try {
        const response = await fetch(`${API_BASE_URL}/rooms`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message);
        table.innerHTML = result.data.length ? result.data.map(room => `
            <tr>
                <td>${roomEscape(room.room_number)}</td>
                <td>${room.floor}</td>
                <td>${roomEscape(room.room_type)}</td>
                <td><span class="badge ${room.status === "Available" ? "badge-success" : "badge-warning"}">${roomEscape(room.status)}</span></td>
                <td><a href="edit.html?id=${encodeURIComponent(room.id)}" class="btn btn-primary btn-sm">Edit</a></td>
            </tr>`).join("") : '<tr><td colspan="5" class="text-center">No rooms found. Use “Add Room” to create one.</td></tr>';
    } catch (error) {
        table.innerHTML = `<tr><td colspan="5" class="text-center">${roomEscape(error.message || "Unable to load rooms")}</td></tr>`;
    }
}


async function createRoom(event) {
    event.preventDefault();
    const errorBox = document.getElementById("roomFormError");
    const button = document.getElementById("saveRoomButton");
    errorBox.textContent = "";
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
    try {
        const response = await fetch(`${API_BASE_URL}/rooms`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${getToken()}` },
            body: JSON.stringify({
                room_number: document.getElementById("roomNumber").value.trim(),
                floor: Number(document.getElementById("floor").value),
                room_type_id: document.getElementById("roomType").value
            })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            const detail = Array.isArray(result.detail) ? result.detail.map(item => item.msg).join(", ") : result.detail;
            throw new Error(detail || result.message || "Unable to save room");
        }
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message;
        button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Room';
    }
}


async function roomApi(url, options = {}) {
    options.headers = { ...(options.headers || {}), "Authorization": `Bearer ${getToken()}` };
    const response = await fetch(url, options);
    const result = await response.json();
    if (response.status === 401) { redirectToLogin(); throw new Error("Session expired"); }
    if (!response.ok || !result.success) {
        const detail = Array.isArray(result.detail) ? result.detail.map(item => item.msg).join(", ") : result.detail;
        throw new Error(detail || result.message || "Room request failed");
    }
    return result.data;
}


async function loadEditRoomTypes(selectedId) {
    const dropdown = document.getElementById("editRoomType");
    const types = await roomApi(`${API_BASE_URL}/room-types`);
    const activeTypes = types.filter(item => item.is_active || item.id === selectedId);
    dropdown.innerHTML = '<option value="">Select a room type</option>' + activeTypes.map(item =>
        `<option value="${roomEscape(item.id)}" ${item.id === selectedId ? "selected" : ""}>${roomEscape(item.name)} - ${formatCurrency(item.base_price)}</option>`
    ).join("");
    dropdown.disabled = false;
}


async function loadRoomForEdit() {
    const roomId = new URLSearchParams(location.search).get("id");
    const errorBox = document.getElementById("editRoomError");
    if (!roomId) { errorBox.textContent = "Missing room ID"; return; }
    try {
        const room = await roomApi(`${API_BASE_URL}/rooms/${encodeURIComponent(roomId)}`);
        document.getElementById("editRoomNumber").value = room.room_number;
        document.getElementById("editFloor").value = room.floor;
        document.getElementById("editRoomStatus").value = room.status;
        await loadEditRoomTypes(room.room_type_id);
    } catch (error) { errorBox.textContent = error.message; }
}


async function updateRoom(event) {
    event.preventDefault();
    const roomId = new URLSearchParams(location.search).get("id");
    const errorBox = document.getElementById("editRoomError");
    const button = document.getElementById("updateRoomButton");
    errorBox.textContent = ""; button.disabled = true; button.textContent = "Saving...";
    try {
        await roomApi(`${API_BASE_URL}/rooms/${encodeURIComponent(roomId)}`, {
            method: "PUT", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                room_number: document.getElementById("editRoomNumber").value.trim(),
                floor: Number(document.getElementById("editFloor").value),
                room_type_id: document.getElementById("editRoomType").value,
                status: document.getElementById("editRoomStatus").value
            })
        });
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message; button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
    }
}
