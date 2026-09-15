document.addEventListener("DOMContentLoaded", () => {
    if (!getToken()) { location.href = "../auth/login.html"; return; }
    if (document.getElementById("checkinTableBody")) loadPendingCheckins();
    if (document.getElementById("checkoutTableBody")) loadActiveCheckouts();
});

function operationEscape(value) { const el=document.createElement("div"); el.textContent=value??""; return el.innerHTML; }
async function operationData(url, options={}) {
    options.headers={...(options.headers||{}), Authorization:`Bearer ${getToken()}`};
    const response=await fetch(url,options); let result;
    try { result=await response.json(); } catch (_) { throw new Error("Server returned an invalid response"); }
    if (response.status === 401) {
        redirectToLogin();
        throw new Error("Your session expired. Please sign in again.");
    }
    if(!response.ok||!result.success) throw new Error(result.detail||result.message||"Request failed");
    return result.data;
}


function operationMessage(message,type) { if(typeof showToast==="function") showToast(message,type); else alert(message); }

async function loadPendingCheckins() {
    const table=document.getElementById("checkinTableBody");
    try { const items=await operationData(`${API_BASE_URL}/checkins/pending`);
        table.innerHTML=items.length?items.map(x=>`<tr><td>${operationEscape(x.booking_id)}</td><td>${operationEscape(x.guest_name)}</td><td>${operationEscape(x.room_number)}</td><td>${operationEscape(x.check_in)}</td><td><button type="button" class="btn btn-success btn-sm" onclick="checkInGuest('${x.id}',this)"><i class="fa-solid fa-right-to-bracket"></i> Check in</button></td></tr>`).join(""):'<tr><td colspan="5" class="empty-state">No guests are waiting to check in.</td></tr>';
    } catch(error) { table.innerHTML=`<tr><td colspan="5" class="empty-state operation-error">${operationEscape(error.message)}</td></tr>`; }
}

async function checkInGuest(id,button) {
    if(!confirm("Has the guest ID been verified? Confirm check-in?")) return;
    button.disabled=true; button.textContent="Checking in...";
    try { await operationData(`${API_BASE_URL}/checkins`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({reservation_id:id,id_proof_verified:true})}); operationMessage("Guest checked in successfully","success"); await loadPendingCheckins(); }
    catch(error) { operationMessage(error.message,"danger"); button.disabled=false; button.textContent="Check in"; }
}

async function loadActiveCheckouts() {
    const table=document.getElementById("checkoutTableBody");
    try { const items=await operationData(`${API_BASE_URL}/checkouts/pending`);
        table.innerHTML=items.length?items.map(x=>`<tr><td>${operationEscape(x.booking_id)}</td><td>${operationEscape(x.guest_name)}</td><td>${operationEscape(x.room_number)}</td><td>${operationEscape(x.check_in)}</td><td><button type="button" class="btn btn-danger btn-sm" onclick="checkoutGuest('${x.id}',this)"><i class="fa-solid fa-right-from-bracket"></i> Checkout</button></td></tr>`).join(""):'<tr><td colspan="5" class="empty-state">No checked-in guests are waiting for checkout.</td></tr>';
    } catch(error) { table.innerHTML=`<tr><td colspan="5" class="empty-state operation-error">${operationEscape(error.message)}</td></tr>`; }
}

async function checkoutGuest(id,button) {
    if(!confirm("Confirm checkout? The room will become available.")) return;
    button.disabled=true; button.textContent="Checking out...";
    try { await operationData(`${API_BASE_URL}/checkouts`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({reservation_id:id})}); operationMessage("Checkout completed and room released","success"); await loadActiveCheckouts(); }
    catch(error) { operationMessage(error.message,"danger"); button.disabled=false; button.textContent="Checkout"; }
}
