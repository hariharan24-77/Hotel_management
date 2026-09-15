let roomTypes = [];

function checkAuthentication() {
    if (!getToken()) window.location.href = "../auth/login.html";
}


function roomTypeEscape(value) {
    const element = document.createElement("div");
    element.textContent = value ?? "";
    return element.innerHTML;
}


async function loadRoomTypes() {
    const table = document.getElementById("roomTypeTableBody");
    if (!table) return;
    table.innerHTML = '<tr><td colspan="7" class="text-center">Loading...</td></tr>';
    try {
        const response = await fetch(`${API_BASE_URL}/room-types`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message);
        roomTypes = result.data;
        renderRoomTypes(roomTypes);
    } catch (error) {
        table.innerHTML = `<tr><td colspan="7" class="text-center">${roomTypeEscape(error.message || "Unable to load room types")}</td></tr>`;
    }
}


function renderRoomTypes(items) {
    const table = document.getElementById("roomTypeTableBody");
    table.innerHTML = items.length ? items.map((item, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${roomTypeEscape(item.name)}</td>
            <td>${formatCurrency(item.base_price)}</td>
            <td>${item.capacity}</td>
            <td>${roomTypeEscape(item.bed_type)}</td>
            <td><span class="badge ${item.is_active ? "badge-success" : "badge-danger"}">${item.status}</span></td>
            <td><a class="btn btn-primary btn-sm" href="edit.html?id=${encodeURIComponent(item.id)}">Edit</a></td>
        </tr>`).join("") : '<tr><td colspan="7" class="text-center">No room types found. Use “Add Room Type” to create one.</td></tr>';
}


function applyRoomTypeFilters() {
    const query = (document.getElementById("searchRoomType")?.value || "").toLowerCase();
    const status = document.getElementById("statusFilter")?.value || "";
    renderRoomTypes(roomTypes.filter(item =>
        item.name.toLowerCase().includes(query) && (!status || item.status === status)
    ));
}


function searchRoomTypes() { 
    applyRoomTypeFilters(); 
}


function filterRoomTypes() { 
    applyRoomTypeFilters(); 
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("roomTypeForm");
    if (form) form.addEventListener("submit", createRoomType);
    const editForm = document.getElementById("editRoomTypeForm");
    if (editForm) {
        editForm.addEventListener("submit", updateRoomType);
        loadRoomTypeForEdit();
    }
});


async function createRoomType(event) {
    event.preventDefault();
    const button = document.getElementById("saveRoomTypeButton");
    const errorBox = document.getElementById("roomTypeFormError");
    errorBox.textContent = "";
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
    try {
        const response = await fetch(`${API_BASE_URL}/room-types`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${getToken()}` },
            body: JSON.stringify({
                name: document.getElementById("roomTypeName").value.trim(),
                base_price: Number(document.getElementById("basePrice").value),
                capacity: Number(document.getElementById("capacity").value),
                bed_type: document.getElementById("bedType").value,
                description: document.getElementById("description").value.trim() || null
            })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            const detail = Array.isArray(result.detail) ? result.detail.map(item => item.msg).join(", ") : result.detail;
            throw new Error(detail || result.message || "Unable to save room type");
        }
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message;
        button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Room Type';
    }
}


async function loadRoomTypeForEdit() {
    const errorBox = document.getElementById("editRoomTypeError");
    const roomTypeId = new URLSearchParams(window.location.search).get("id");
    if (!roomTypeId) {
        errorBox.textContent = "Missing room type ID";
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/room-types/${encodeURIComponent(roomTypeId)}`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message);
        const item = result.data;
        document.getElementById("editRoomTypeName").value = item.name;
        document.getElementById("editBasePrice").value = item.base_price;
        document.getElementById("editCapacity").value = item.capacity;
        document.getElementById("editBedType").value = item.bed_type;
        document.getElementById("editDescription").value = item.description || "";
        document.getElementById("editRoomTypeStatus").value = String(item.is_active);
    } catch (error) {
        errorBox.textContent = error.message || "Unable to load room type";
    }
}


async function updateRoomType(event) {
    event.preventDefault();
    const roomTypeId = new URLSearchParams(window.location.search).get("id");
    const errorBox = document.getElementById("editRoomTypeError");
    const button = document.getElementById("updateRoomTypeButton");
    errorBox.textContent = "";
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Updating...';
    try {
        const response = await fetch(`${API_BASE_URL}/room-types/${encodeURIComponent(roomTypeId)}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${getToken()}` },
            body: JSON.stringify({
                name: document.getElementById("editRoomTypeName").value.trim(),
                base_price: Number(document.getElementById("editBasePrice").value),
                capacity: Number(document.getElementById("editCapacity").value),
                bed_type: document.getElementById("editBedType").value.trim(),
                description: document.getElementById("editDescription").value.trim() || null,
                is_active: document.getElementById("editRoomTypeStatus").value === "true"
            })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            const detail = Array.isArray(result.detail) ? result.detail.map(item => item.msg).join(", ") : result.detail;
            throw new Error(detail || result.message || "Unable to update room type");
        }
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message;
        button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Update Room Type';
    }
}
