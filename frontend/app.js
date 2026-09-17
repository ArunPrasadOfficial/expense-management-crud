// ================== CONFIG ==================
const API_BASE_URL = "http://127.0.0.1:8000/api/expenses/";

// ================== DOM ELEMENTS ==================
const form = document.getElementById("expenseForm");
const formTitle = document.getElementById("formTitle");
const expenseIdInput = document.getElementById("expenseId");
const titleInput = document.getElementById("title");
const amountInput = document.getElementById("amount");
const categoryInput = document.getElementById("category");
const dateInput = document.getElementById("date");
const paymentInput = document.getElementById("payment_method");
const descriptionInput = document.getElementById("description");

const submitBtn = document.getElementById("submitBtn");
const cancelEditBtn = document.getElementById("cancelEditBtn");

const searchInput = document.getElementById("searchInput");
const filterCategory = document.getElementById("filterCategory");
const filterDateFrom = document.getElementById("filterDateFrom");
const filterDateTo = document.getElementById("filterDateTo");
const applyFilterBtn = document.getElementById("applyFilterBtn");
const clearFilterBtn = document.getElementById("clearFilterBtn");

const tableBody = document.getElementById("expenseTableBody");
const emptyMsg = document.getElementById("emptyMsg");
const alertBox = document.getElementById("alertBox");
const totalAmountEl = document.getElementById("totalAmount");

// Set default date to today, and max date to today (no future dates)
const todayStr = new Date().toISOString().split("T")[0];
dateInput.value = todayStr;
dateInput.max = todayStr;

// ================== INIT ==================
document.addEventListener("DOMContentLoaded", () => {
  loadExpenses();
});

form.addEventListener("submit", handleFormSubmit);
cancelEditBtn.addEventListener("click", resetForm);
applyFilterBtn.addEventListener("click", () => loadExpenses());
clearFilterBtn.addEventListener("click", clearFilters);

// ================== ALERT HELPERS ==================
function showAlert(message, type = "success") {
  alertBox.textContent = message;
  alertBox.className = `alert alert-${type}`;
  alertBox.classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
  setTimeout(() => alertBox.classList.add("hidden"), 4000);
}

// ================== CLIENT-SIDE VALIDATION ==================
function clearFieldErrors() {
  ["title", "amount", "category", "date"].forEach((f) => {
    document.getElementById(`err-${f}`).textContent = "";
  });
}

function validateForm() {
  clearFieldErrors();
  let isValid = true;

  if (!titleInput.value.trim()) {
    document.getElementById("err-title").textContent = "Title is required.";
    isValid = false;
  }

  const amountVal = parseFloat(amountInput.value);
  if (isNaN(amountVal) || amountVal <= 0) {
    document.getElementById("err-amount").textContent = "Enter a valid amount greater than 0.";
    isValid = false;
  }

  if (!categoryInput.value) {
    document.getElementById("err-category").textContent = "Please select a category.";
    isValid = false;
  }

  if (!dateInput.value) {
    document.getElementById("err-date").textContent = "Date is required.";
    isValid = false;
  } else if (dateInput.value > todayStr) {
    document.getElementById("err-date").textContent = "Date cannot be in the future.";
    isValid = false;
  }

  return isValid;
}

// ================== FORM SUBMIT (CREATE / UPDATE) ==================
async function handleFormSubmit(e) {
  e.preventDefault();

  if (!validateForm()) return;

  const payload = {
    title: titleInput.value.trim(),
    amount: parseFloat(amountInput.value),
    category: categoryInput.value,
    date: dateInput.value,
    payment_method: paymentInput.value,
    description: descriptionInput.value.trim(),
  };

  const id = expenseIdInput.value;
  const isEdit = !!id;
  const url = isEdit ? `${API_BASE_URL}${id}/` : API_BASE_URL;
  const method = isEdit ? "PUT" : "POST";

  submitBtn.disabled = true;

  try {
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (response.ok) {
      showAlert(data.message || (isEdit ? "Expense updated." : "Expense created."), "success");
      resetForm();
      loadExpenses();
    } else {
      showServerErrors(data);
    }
  } catch (err) {
    console.error(err);
    showAlert("Could not connect to the server. Make sure the backend is running.", "error");
  } finally {
    submitBtn.disabled = false;
  }
}

function showServerErrors(data) {
  if (data.errors) {
    Object.keys(data.errors).forEach((field) => {
      const el = document.getElementById(`err-${field}`);
      if (el) el.textContent = Array.isArray(data.errors[field]) ? data.errors[field][0] : data.errors[field];
    });
    showAlert(data.message || "Please fix the highlighted errors.", "error");
  } else {
    showAlert(data.detail || "Something went wrong.", "error");
  }
}

// ================== RESET FORM ==================
function resetForm() {
  form.reset();
  expenseIdInput.value = "";
  dateInput.value = todayStr;
  paymentInput.value = "Cash";
  formTitle.textContent = "Add Expense";
  submitBtn.textContent = "Add Expense";
  cancelEditBtn.classList.add("hidden");
  clearFieldErrors();
}

// ================== LOAD / FILTER EXPENSES ==================
function buildQueryParams() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.append("search", searchInput.value.trim());
  if (filterCategory.value) params.append("category", filterCategory.value);
  if (filterDateFrom.value) params.append("date_from", filterDateFrom.value);
  if (filterDateTo.value) params.append("date_to", filterDateTo.value);
  params.append("page_size", 100);
  return params.toString();
}

async function loadExpenses() {
  try {
    const query = buildQueryParams();
    const response = await fetch(`${API_BASE_URL}?${query}`);
    const data = await response.json();

    // DRF pagination wraps list in "results"; handle both cases
    const expenses = Array.isArray(data) ? data : data.results || [];
    renderExpenses(expenses);
  } catch (err) {
    console.error(err);
    showAlert("Failed to load expenses. Is the Django server running on port 8000?", "error");
  }
}

function clearFilters() {
  searchInput.value = "";
  filterCategory.value = "";
  filterDateFrom.value = "";
  filterDateTo.value = "";
  loadExpenses();
}

// ================== RENDER TABLE ==================
function renderExpenses(expenses) {
  tableBody.innerHTML = "";
  let total = 0;

  if (!expenses.length) {
    emptyMsg.classList.remove("hidden");
    totalAmountEl.textContent = "Total: ₹0.00";
    return;
  }
  emptyMsg.classList.add("hidden");

  expenses.forEach((exp) => {
    total += parseFloat(exp.amount);

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${escapeHtml(exp.title)}</td>
      <td>₹${parseFloat(exp.amount).toFixed(2)}</td>
      <td><span class="category-tag">${escapeHtml(exp.category)}</span></td>
      <td>${exp.date}</td>
      <td>${escapeHtml(exp.payment_method)}</td>
      <td>${escapeHtml(exp.description || "-")}</td>
      <td>
        <button class="btn-sm btn-edit" onclick="editExpense(${exp.id})">Edit</button>
        <button class="btn-sm btn-delete" onclick="deleteExpense(${exp.id})">Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });

  totalAmountEl.textContent = `Total: ₹${total.toFixed(2)}`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

// ================== EDIT ==================
async function editExpense(id) {
  try {
    const response = await fetch(`${API_BASE_URL}${id}/`);
    if (!response.ok) throw new Error("Not found");
    const exp = await response.json();

    expenseIdInput.value = exp.id;
    titleInput.value = exp.title;
    amountInput.value = exp.amount;
    categoryInput.value = exp.category;
    dateInput.value = exp.date;
    paymentInput.value = exp.payment_method;
    descriptionInput.value = exp.description || "";

    formTitle.textContent = "Edit Expense";
    submitBtn.textContent = "Update Expense";
    cancelEditBtn.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    showAlert("Could not load expense for editing.", "error");
  }
}

// ================== DELETE ==================
async function deleteExpense(id) {
  if (!confirm("Are you sure you want to delete this expense?")) return;

  try {
    const response = await fetch(`${API_BASE_URL}${id}/`, { method: "DELETE" });
    const data = await response.json().catch(() => ({}));

    if (response.ok) {
      showAlert(data.message || "Expense deleted successfully.", "success");
      loadExpenses();
    } else {
      showAlert("Failed to delete expense.", "error");
    }
  } catch (err) {
    showAlert("Could not connect to the server.", "error");
  }
}
