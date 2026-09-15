document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("staffForm");
    const table = document.getElementById("staffTableBody");
    if (form) form.addEventListener("submit", createStaff);
    if (table) loadStaff();
    const editForm = document.getElementById("editStaffForm");
    if (editForm) {
        editForm.addEventListener("submit", updateStaff);
        loadStaffForEdit();
    }
});


function escapeHtml(value) {
    const element = document.createElement("div");
    element.textContent = value ?? "";
    return element.innerHTML;
}


async function fetchRoles(selectedRoleId = "") {
    const response = await fetch(`${API_BASE_URL}/users/roles`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    const result = await response.json();
    if (!response.ok || !result.success) throw new Error(result.detail || result.message || "Unable to load roles");
    return '<option value="">Select a role</option>' + result.data.map(role =>
        `<option value="${escapeHtml(role.id)}" ${role.id === selectedRoleId ? "selected" : ""}>${escapeHtml(role.name.replaceAll("_", " "))}</option>`
    ).join("");
}


async function loadStaffForEdit() {
    const errorBox = document.getElementById("editStaffError");
    const staffId = new URLSearchParams(window.location.search).get("id");
    if (!staffId) {
        errorBox.textContent = "Missing staff account ID";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/staff/${encodeURIComponent(staffId)}`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message);
        const staff = result.data;
        document.getElementById("editName").value = staff.name;
        document.getElementById("editEmail").value = staff.email;
        document.getElementById("editUsername").value = staff.username || "";
        document.getElementById("editRole").innerHTML = await fetchRoles(staff.role_id);
        document.getElementById("editRole").disabled = false;
        document.getElementById("editStatus").value = String(staff.is_active);
    } catch (error) {
        errorBox.textContent = error.message || "Unable to load staff account";
    }
}


async function updateStaff(event) {
    event.preventDefault();
    const staffId = new URLSearchParams(window.location.search).get("id");
    const button = document.getElementById("updateStaffButton");
    const errorBox = document.getElementById("editStaffError");
    errorBox.textContent = "";
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Updating...';

    try {
        const response = await fetch(`${API_BASE_URL}/staff/${encodeURIComponent(staffId)}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                name: document.getElementById("editName").value.trim(),
                email: document.getElementById("editEmail").value.trim(),
                username: document.getElementById("editUsername").value.trim(),
                role_id: document.getElementById("editRole").value,
                is_active: document.getElementById("editStatus").value === "true"
            })
        });
        const result = await response.json();
        if (!response.ok || !result.success) throw new Error(result.detail || result.message || "Unable to update staff");
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message;
        button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Update Staff';
    }
}


async function loadStaff() {
    const table = document.getElementById("staffTableBody");
    if (!table) return;

    try {
        const response = await fetch(`${API_BASE_URL}/staff`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            throw new Error(result.detail || result.message || "Unable to load staff");
        }

        table.innerHTML = result.data.length
            ? result.data.map(staff => `
                <tr>
                    <td>${escapeHtml(staff.name)}</td>
                    <td>${escapeHtml(staff.username || "—")}</td>
                    <td>${escapeHtml(staff.email)}</td>
                    <td>${escapeHtml(staff.role.replaceAll("_", " "))}</td>
                    <td><span class="badge ${staff.is_active ? "badge-success" : "badge-danger"}">${escapeHtml(staff.status)}</span></td>
                    <td>
                        <a href="edit.html?id=${encodeURIComponent(staff.id)}" class="btn btn-primary btn-sm">Edit</a>
                    </td>
                </tr>`).join("")
            : '<tr><td colspan="6" class="text-center">No staff accounts found.</td></tr>';
    } catch (error) {
        table.innerHTML = `<tr><td colspan="6" class="text-center">${escapeHtml(error.message)}</td></tr>`;
    }
}


async function createStaff(event) {
    event.preventDefault();

    const button = document.getElementById("createStaffButton");
    const errorBox = document.getElementById("staffFormError");
    errorBox.textContent = "";
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Creating...';

    const payload = {
        name: document.getElementById("staffName").value.trim(),
        email: document.getElementById("staffEmail").value.trim(),
        username: document.getElementById("staffUsername").value.trim(),
        password: document.getElementById("staffPassword").value,
        role_id: document.getElementById("staffRole").value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/staff`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            const validationMessage = Array.isArray(result.detail)
                ? result.detail.map(item => item.msg).join(", ")
                : result.detail;
            throw new Error(validationMessage || result.message || "Unable to create staff");
        }

        if (window.Toast) Toast.success(result.message);
        window.location.href = "index.html";
    } catch (error) {
        errorBox.textContent = error.message;
        button.disabled = false;
        button.innerHTML = '<i class="fa-solid fa-user-plus"></i> Create Staff';
    }
}
