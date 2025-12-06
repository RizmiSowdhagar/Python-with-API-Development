const API_BASE = "";

// DOM elements
const form = document.getElementById("calc-form");
const idInput = document.getElementById("calc-id");
const opSelect = document.getElementById("operation");
const aInput = document.getElementById("a");
const bInput = document.getElementById("b");
const submitBtn = document.getElementById("submit-btn");
const resetBtn = document.getElementById("reset-btn");
const refreshBtn = document.getElementById("refresh-btn");
const tbody = document.getElementById("calc-tbody");
const errorMsg = document.getElementById("error-msg");
const successMsg = document.getElementById("success-msg");

function clearMessages() {
  errorMsg.textContent = "";
  successMsg.textContent = "";
}

function showError(msg) {
  errorMsg.textContent = msg;
  successMsg.textContent = "";
}

function showSuccess(msg) {
  successMsg.textContent = msg;
  errorMsg.textContent = "";
}

function validateInputs() {
  clearMessages();
  const operation = opSelect.value;
  const a = aInput.value;
  const b = bInput.value;

  if (a === "" || b === "") {
    showError("Both a and b are required.");
    return null;
  }

  const aNum = Number(a);
  const bNum = Number(b);

  if (Number.isNaN(aNum) || Number.isNaN(bNum)) {
    showError("a and b must be numbers.");
    return null;
  }

  if (operation === "divide" && bNum === 0) {
    showError("Cannot divide by zero.");
    return null;
  }

  return { operation, a: aNum, b: bNum };
}

// Normalize a calculation object from API
function normalizeCalc(c) {
  const operation = c.operation || c.type || c.operator || "";
  const a = c.a ?? c.operand1 ?? 0;
  const b = c.b ?? c.operand2 ?? 0;
  return {
    id: c.id,
    operation,
    a,
    b,
    result: c.result ?? null,
    created_at: c.created_at ?? null,
  };
}

async function loadCalculations() {
  clearMessages();
  try {
    const resp = await fetch(`${API_BASE}/calculations`);
    if (!resp.ok) {
      throw new Error(`Failed to load calculations (${resp.status})`);
    }
    const data = await resp.json();
    renderTable(data.map(normalizeCalc));
  } catch (err) {
    console.error(err);
    showError("Failed to load calculations.");
  }
}

function renderTable(calcs) {
  tbody.innerHTML = "";
  for (const c of calcs) {
    const tr = document.createElement("tr");

    const tdId = document.createElement("td");
    tdId.textContent = c.id;
    tr.appendChild(tdId);

    const tdOp = document.createElement("td");
    tdOp.textContent = c.operation;
    tr.appendChild(tdOp);

    const tdA = document.createElement("td");
    tdA.textContent = c.a;
    tr.appendChild(tdA);

    const tdB = document.createElement("td");
    tdB.textContent = c.b;
    tr.appendChild(tdB);

    const tdResult = document.createElement("td");
    tdResult.textContent = c.result ?? "";
    tr.appendChild(tdResult);

    const tdCreated = document.createElement("td");
    tdCreated.textContent = c.created_at ? c.created_at : "";
    tr.appendChild(tdCreated);

    const tdActions = document.createElement("td");
    tdActions.classList.add("actions");

    const editBtn = document.createElement("button");
    editBtn.type = "button";
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () => startEdit(c));
    tdActions.appendChild(editBtn);

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => deleteCalculation(c.id));
    tdActions.appendChild(delBtn);

    tr.appendChild(tdActions);

    tbody.appendChild(tr);
  }
}

function resetForm() {
  idInput.value = "";
  opSelect.value = "add";
  aInput.value = "";
  bInput.value = "";
  submitBtn.textContent = "Create";
  clearMessages();
}

function startEdit(calc) {
  clearMessages();
  idInput.value = calc.id;
  opSelect.value = calc.operation || "add";
  aInput.value = calc.a;
  bInput.value = calc.b;
  submitBtn.textContent = "Update";
}

async function createCalculation(payload) {
  // Ensure both "operation" and "type" are sent so Pydantic passes
  const body = {
    operation: payload.operation,
    type: payload.operation,
    a: payload.a,
    b: payload.b,
  };

  const resp = await fetch(`${API_BASE}/calculations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `Create failed (${resp.status})`);
  }

  return resp.json();
}

async function updateCalculation(id, payload) {
  const body = {
    operation: payload.operation,
    type: payload.operation,
    a: payload.a,
    b: payload.b,
  };

  const resp = await fetch(`${API_BASE}/calculations/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `Update failed (${resp.status})`);
  }

  return resp.json();
}

async function deleteCalculation(id) {
  clearMessages();
  try {
    const resp = await fetch(`${API_BASE}/calculations/${id}`, {
      method: "DELETE",
    });
    if (!resp.ok) {
      throw new Error(`Delete failed (${resp.status})`);
    }
    showSuccess(`Calculation ${id} deleted.`);
    await loadCalculations();
  } catch (err) {
    console.error(err);
    showError("Failed to delete calculation.");
  }
}

form.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  clearMessages();

  const validated = validateInputs();
  if (!validated) return;

  const currentId = idInput.value;

  try {
    if (currentId) {
      await updateCalculation(currentId, validated);
      showSuccess("Calculation updated.");
    } else {
      await createCalculation(validated);
      showSuccess("Calculation created.");
    }
    resetForm();
    await loadCalculations();
  } catch (err) {
    console.error(err);
    showError("Failed to save calculation.");
  }
});

resetBtn.addEventListener("click", (evt) => {
  evt.preventDefault();
  resetForm();
});

refreshBtn.addEventListener("click", (evt) => {
  evt.preventDefault();
  loadCalculations();
});

document.addEventListener("DOMContentLoaded", () => {
  resetForm();
  loadCalculations();
});
