let revenueChartInstance = null,
  occupancyChartInstance = null;
document.addEventListener("DOMContentLoaded", () => {
  if (!getToken()) {
    location.href = "../auth/login.html";
    return;
  }
  if (document.getElementById("totalRooms")) {
    loadDashboard();
    loadRevenueChart();
  }
  if (document.getElementById("revenueReportChart")) {
    setReportDates();
    loadRevenueReport();
  }
  if (document.getElementById("occupancyChart")) loadOccupancyReport();
});


async function reportApi(url) {
  const r = await fetch(url, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  const j = await r.json();
  if (r.status === 401) {
    redirectToLogin();
    throw new Error("Session expired");
  }
  if (!r.ok || !j.success)
    throw new Error(j.detail || j.message || "Unable to load report");
  return j.data;
}


function reportError(e) {
  const x = document.getElementById("reportError");
  if (x) x.textContent = e.message;
}


async function loadDashboard() {
  try {
    const d = await reportApi(`${API_BASE_URL}/reports/dashboard`);
    totalRooms.textContent = d.total_rooms;
    availableRooms.textContent = d.available_rooms;
    occupiedRooms.textContent = d.occupied_rooms;
    totalRevenue.textContent = `₹ ${Number(d.total_revenue).toFixed(2)}`;
  } catch (e) {
    reportError(e);
  }
}


function chart(canvas, type, labels, data, label, old) {
  if (typeof Chart === "undefined")
    throw new Error("Chart library could not be loaded");
  if (old) old.destroy();
  return new Chart(canvas, {
    type,
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          backgroundColor: ["#d4af37", "#183b65", "#94a3b8"],
          borderColor: "#183b65",
          borderWidth: 2,
        },
      ],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
}


async function loadRevenueChart() {
  try {
    const d = await reportApi(`${API_BASE_URL}/reports/revenue`);
    revenueChartInstance = chart(
      document.getElementById("revenueChart"),
      "bar",
      d.months,
      d.amounts,
      "Collected revenue",
      revenueChartInstance,
    );
  } catch (e) {
    reportError(e);
  }
}


function setReportDates() {
  const now = new Date(),
    start = new Date(now.getFullYear(), now.getMonth() - 5, 1),
    from = document.getElementById("fromDate"),
    to = document.getElementById("toDate");
  from.value = start.toISOString().slice(0, 10);
  to.value = now.toISOString().slice(0, 10);
  to.max = now.toISOString().slice(0, 10);
}


async function loadRevenueReport() {
  try {
    const from = document.getElementById("fromDate"),
      to = document.getElementById("toDate");
    if (!from.value || !to.value) throw new Error("Select both dates");
    const d = await reportApi(
      `${API_BASE_URL}/reports/revenue?from=${encodeURIComponent(from.value)}&to=${encodeURIComponent(to.value)}`,
    );
    document.getElementById("revenueTotal").textContent =
      `₹ ${Number(d.total).toFixed(2)}`;
    revenueChartInstance = chart(
      document.getElementById("revenueReportChart"),
      "line",
      d.months,
      d.amounts,
      "Collected revenue",
      revenueChartInstance,
    );
    reportError({ message: "" });
  } catch (e) {
    reportError(e);
  }
}


async function loadOccupancyReport() {
  try {
    const d = await reportApi(`${API_BASE_URL}/reports/occupancy`);
    document.getElementById("occupancySummary").textContent =
      `${d.occupied} occupied · ${d.available} available · ${d.maintenance} unavailable`;
    occupancyChartInstance = chart(
      document.getElementById("occupancyChart"),
      "doughnut",
      ["Occupied", "Available", "Maintenance / Inactive"],
      [d.occupied, d.available, d.maintenance],
      "Rooms",
      occupancyChartInstance,
    );
  } catch (e) {
    reportError(e);
  }
}
