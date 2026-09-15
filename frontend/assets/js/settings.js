document.addEventListener("DOMContentLoaded", async () => {
  if (!getToken()) {
    location.href = "../auth/login.html";
    return;
  }
  const forms = {
    hotelProfileForm: [loadProfile, saveProfile],
    roomSettingForm: [null, saveRoomSetting],
    taxForm: [loadTax, saveTax],
    paymentSettingForm: [loadPaymentSettings, savePaymentSettings],
  };
  for (const [id, [load, save]] of Object.entries(forms)) {
    const f = document.getElementById(id);
    if (f) {
      f.addEventListener("submit", save);
      if (load) await load();
    }
  }
});


async function settingApi(url, o = {}) {
  o.headers = { ...(o.headers || {}), Authorization: `Bearer ${getToken()}` };
  const r = await fetch(url, o);
  const j = await r.json();
  if (r.status === 401) {
    redirectToLogin();
    throw new Error("Session expired");
  }
  if (!r.ok || !j.success) {
    const d = Array.isArray(j.detail)
      ? j.detail.map((x) => x.msg).join(", ")
      : j.detail;
    throw new Error(d || j.message || "Settings request failed");
  }
  return j.data;
}


function settingError(e) {
  const x = document.getElementById("settingsError");
  if (x) x.textContent = e.message;
}


function busy(id, on) {
  const b = document.getElementById(id);
  if (b) b.disabled = on;
}


async function getSettings() {
  return settingApi(`${API_BASE_URL}/settings`);
}


async function loadProfile() {
  try {
    const d = await getSettings();
    hotelName.value = d.name;
    hotelPhone.value = d.phone;
    hotelEmail.value = d.email;
    hotelAddress.value = d.address;
  } catch (e) {
    settingError(e);
  }
}


async function saveProfile(e) {
  e.preventDefault();
  busy("saveSettingsButton", true);
  try {
    await settingApi(`${API_BASE_URL}/settings`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: hotelName.value.trim(),
        phone: hotelPhone.value.trim(),
        email: hotelEmail.value.trim(),
        address: hotelAddress.value.trim(),
      }),
    });
    location.href = "index.html";
  } catch (x) {
    settingError(x);
    busy("saveSettingsButton", false);
  }
}


async function saveRoomSetting(e) {
  e.preventDefault();
  busy("saveRoomSettingButton", true);
  try {
    await settingApi(`${API_BASE_URL}/settings/rooms`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        room_type: roomType.value.trim(),
        price: Number(roomPrice.value),
        capacity: Number(roomCapacity.value),
      }),
    });
    location.href = "../room_types/index.html";
  } catch (x) {
    settingError(x);
    busy("saveRoomSettingButton", false);
  }
}


async function loadTax() {
  try {
    const d = await getSettings();
    gstPercentage.value = d.gst;
    serviceTax.value = d.service_tax;
  } catch (e) {
    settingError(e);
  }
}


async function saveTax(e) {
  e.preventDefault();
  busy("saveTaxButton", true);
  try {
    await settingApi(`${API_BASE_URL}/settings/tax`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gst: Number(gstPercentage.value),
        service_tax: Number(serviceTax.value),
      }),
    });
    location.href = "index.html";
  } catch (x) {
    settingError(x);
    busy("saveTaxButton", false);
  }
}


async function loadPaymentSettings() {
  try {
    const d = await getSettings();
    cashPayment.checked = d.cash;
    upiPayment.checked = d.upi;
    cardPayment.checked = d.card;
  } catch (e) {
    settingError(e);
  }
}


async function savePaymentSettings(e) {
  e.preventDefault();
  busy("savePaymentSettingButton", true);
  try {
    await settingApi(`${API_BASE_URL}/settings/payment`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cash: cashPayment.checked,
        upi: upiPayment.checked,
        card: cardPayment.checked,
      }),
    });
    location.href = "index.html";
  } catch (x) {
    settingError(x);
    busy("savePaymentSettingButton", false);
  }
}
