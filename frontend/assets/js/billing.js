let billingTaxRate = 0;

document.addEventListener("DOMContentLoaded", () => {
  if (!getToken()) {
    location.href = "../auth/login.html";
    return;
  }
  if (document.getElementById("billingTableBody")) loadBills();
  if (document.getElementById("paymentsTableBody")) loadPayments();
  if (document.getElementById("invoiceForm")) {
    loadEligible();
    loadTaxSettingsForBilling();
    document
      .getElementById("invoiceForm")
      .addEventListener("submit", createInvoice);
    ["roomCharge", "serviceCharge"].forEach((id) =>
      document
        .getElementById(id)
        .addEventListener("input", calculateInvoiceTax),
    );
  }
  if (document.getElementById("paymentForm")) {
    loadBillForPayment();
    loadPaymentSettingsForBilling();
    document
      .getElementById("paymentForm")
      .addEventListener("submit", makePayment);
  }
  if (document.getElementById("invoiceDetails")) loadInvoice();
});


function bEsc(v) {
  const e = document.createElement("div");
  e.textContent = v ?? "";
  return e.innerHTML;
}


function money(v) {
  return `₹ ${Number(v || 0).toFixed(2)}`;
}


async function billApi(url, o = {}) {
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
    throw new Error(d || j.message || "Request failed");
  }
  return j.data;
}


function err(id, e) {
  const x = document.getElementById(id);
  if (x) x.textContent = e.message;
}


async function loadPaymentSettingsForBilling() {
  try {
    const s = await billApi(`${API_BASE_URL}/settings`),
      select = document.getElementById("paymentMethod"),
      enabled = { Cash: s.cash, UPI: s.upi, Card: s.card };
    [...select.options].forEach((o) => {
      if (o.value && !enabled[o.value]) o.remove();
    });
    if (select.options.length === 1)
      throw new Error("No payment methods are enabled in Settings");
  } catch (e) {
    err("paymentError", e);
  }
}


async function loadTaxSettingsForBilling() {
  try {
    const s = await billApi(`${API_BASE_URL}/settings`);
    billingTaxRate = Number(s.gst) + Number(s.service_tax);
    tax.readOnly = true;
    calculateInvoiceTax();
  } catch (e) {
    err("invoiceError", e);
  }
}


function calculateInvoiceTax() {
  const subtotal =
    Number(roomCharge.value || 0) + Number(serviceCharge.value || 0);
  tax.value = ((subtotal * billingTaxRate) / 100).toFixed(2);
  total();
}


async function loadBills() {
  const t = document.getElementById("billingTableBody");
  try {
    const a = await billApi(`${API_BASE_URL}/billing`);
    t.innerHTML = a.length
      ? a
          .map(
            (x) =>
              `<tr><td>${bEsc(x.invoice_no)}</td><td>${bEsc(x.guest_name)}</td><td>${bEsc(x.room_number)}</td><td>${money(x.amount)}</td><td>${money(x.balance)}</td><td><span class="badge ${x.payment_status === "Paid" ? "badge-success" : "badge-warning"}">${bEsc(x.payment_status)}</span></td><td><a class="btn btn-primary btn-sm" href="view.html?id=${x.id}">View</a> ${x.balance > 0 ? `<a class="btn btn-success btn-sm" href="payment.html?id=${x.id}">Pay</a>` : ""}</td></tr>`,
          )
          .join("")
      : '<tr><td colspan="7" class="empty-state">No invoices found.</td></tr>';
  } catch (e) {
    t.innerHTML = `<tr><td colspan="7" class="empty-state operation-error">${bEsc(e.message)}</td></tr>`;
  }
}


async function loadEligible() {
  const s = document.getElementById("reservationId");
  roomCharge.readOnly = true;
  try {
    const a = await billApi(`${API_BASE_URL}/billing/eligible-reservations`);
    s.innerHTML =
      '<option value="">Select completed reservation</option>' +
      a
        .map(
          (x) =>
            `<option value="${x.id}" data-charge="${x.suggested_room_charge}">${bEsc(x.booking_id)} - ${bEsc(x.guest_name)} - Room ${bEsc(x.room_number)} (${x.nights} night${x.nights === 1 ? "" : "s"})</option>`,
        )
        .join("");
    s.disabled = !a.length;
    s.addEventListener("change", () => {
      const o = s.selectedOptions[0];
      roomCharge.value = o?.dataset.charge || "";
      serviceCharge.value = "0.00";
      calculateInvoiceTax();
    });
  } catch (e) {
    err("invoiceError", e);
  }
}


function total() {
  document.getElementById("totalAmount").value = (
    Number(document.getElementById("roomCharge").value || 0) +
    Number(document.getElementById("serviceCharge").value || 0) +
    Number(document.getElementById("tax").value || 0)
  ).toFixed(2);
}


async function createInvoice(e) {
  e.preventDefault();
  const b = document.getElementById("saveInvoiceButton");
  b.disabled = true;
  try {
    await billApi(`${API_BASE_URL}/billing`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        reservation_id: reservationId.value,
        room_charge: Number(roomCharge.value),
        service_charge: Number(serviceCharge.value),
        tax: Number(tax.value),
      }),
    });
    location.href = "index.html";
  } catch (x) {
    err("invoiceError", x);
    b.disabled = false;
  }
}


async function loadBillForPayment() {
  const id = new URLSearchParams(location.search).get("id");
  try {
    const x = await billApi(
      `${API_BASE_URL}/billing/${encodeURIComponent(id)}`,
    );
    document.getElementById("paymentReference").textContent =
      `${x.invoice_no} · ${x.guest_name}`;
    paymentAmount.value = x.balance;
    paymentAmount.max = x.balance;
    document.getElementById("balanceDisplay").value = money(x.balance);
  } catch (e) {
    err("paymentError", e);
  }
}


async function makePayment(e) {
  e.preventDefault();
  const id = new URLSearchParams(location.search).get("id"),
    b = document.getElementById("savePaymentButton");
  b.disabled = true;
  try {
    await billApi(`${API_BASE_URL}/payments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        bill_id: id,
        amount: Number(paymentAmount.value),
        payment_method: paymentMethod.value,
      }),
    });
    location.href = "payments.html";
  } catch (x) {
    err("paymentError", x);
    b.disabled = false;
  }
}


async function loadPayments() {
  const t = document.getElementById("paymentsTableBody");
  try {
    const a = await billApi(`${API_BASE_URL}/payments`);
    t.innerHTML = a.length
      ? a
          .map(
            (x) =>
              `<tr><td>${bEsc(x.payment_no)}</td><td>${bEsc(x.invoice_no)}</td><td>${bEsc(x.guest_name)}</td><td>${money(x.amount)}</td><td>${bEsc(x.payment_method)}</td><td>${new Date(x.date).toLocaleString()}</td></tr>`,
          )
          .join("")
      : '<tr><td colspan="6" class="empty-state">No payments recorded.</td></tr>';
  } catch (e) {
    t.innerHTML = `<tr><td colspan="6" class="empty-state operation-error">${bEsc(e.message)}</td></tr>`;
  }
}



async function loadInvoice() {
  const id = new URLSearchParams(location.search).get("id");
  try {
    const x = await billApi(
      `${API_BASE_URL}/billing/${encodeURIComponent(id)}`,
    );
    invoiceDetails.innerHTML = `<h2>${bEsc(x.invoice_no)}</h2><p><b>Guest:</b> ${bEsc(x.guest_name)}</p><p><b>Booking:</b> ${bEsc(x.booking_id)}</p><p><b>Room:</b> ${bEsc(x.room_number)}</p><hr><p>Room: ${money(x.room_charge)}</p><p>Service: ${money(x.service_charge)}</p><p>Tax: ${money(x.tax)}</p><h3>Total: ${money(x.amount)}</h3><p>Paid: ${money(x.paid_amount)} · Balance: ${money(x.balance)}</p>`;
  } catch (e) {
    invoiceDetails.textContent = e.message;
  }
}


function printInvoice() {
  window.print();
}
