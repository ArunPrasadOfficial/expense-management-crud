# Expense Management System

A full-stack CRUD web application to track personal expenses, built as a college mini-project.

**Stack:** HTML/CSS/JavaScript (frontend) · Django + Django REST Framework (backend) · SQLite (database)

---

## Features

- Create, Read, Update, Delete expenses
- Search by title/description
- Filter by category and date range
- Client-side AND server-side validation
- Success/error alert messages
- Responsive UI (mobile + desktop)
- REST API tested via Postman

## Expense Fields

| Field          | Type    | Notes                                   |
|----------------|---------|------------------------------------------|
| id             | integer | auto-generated                          |
| title          | string  | required                                |
| amount         | decimal | required, must be > 0                   |
| category       | string  | Food, Transport, Education, Shopping, Bills, Health, Entertainment, Other |
| date           | date    | required, cannot be a future date       |
| payment_method | string  | Cash, Card, UPI, Net Banking, Other      |
| description    | text    | optional                                |

## Folder Structure

```
expense-management-system/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3            (created after migration)
│   ├── expense_system/       # Django project (settings, urls)
│   └── expenses/             # Django app (models, views, serializers, urls, tests)
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── screenshots/
└── README.md
```

---

## Backend Setup (Django + DRF)

```bash
cd backend

# 1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (creates SQLite db.sqlite3)
python manage.py makemigrations
python manage.py migrate

# 4. (Optional) create admin user
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

## Frontend Setup

No build tools needed — plain HTML/CSS/JS.

```bash
cd frontend
# Option 1: just open index.html directly in the browser

# Option 2 (recommended, avoids CORS/file quirks): serve it
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in the browser (with the Django server also running on port 8000).

---

## REST API Endpoints

| Method | Endpoint                | Description              |
|--------|--------------------------|---------------------------|
| POST   | /api/expenses/           | Create a new expense      |
| GET    | /api/expenses/           | List all expenses         |
| GET    | /api/expenses/<id>/      | Retrieve one expense      |
| PUT    | /api/expenses/<id>/      | Full update                |
| PATCH  | /api/expenses/<id>/      | Partial update             |
| DELETE | /api/expenses/<id>/      | Delete an expense          |
| GET    | /api/expenses/summary/   | Total count & sum (extra)  |



## Git / GitHub Commands

```bash
git init
git add .
git commit -m "Initial commit: Expense Management System"
git branch -M main
git remote add origin https://github.com/<your-username>/expense-management-system.git
git push -u origin main
```

---

## Short Project Explanation (for Viva)

This project is an **Expense Management System** that lets a user record daily expenses and manage them fully (CRUD). The **frontend** (HTML/CSS/JS) sends `fetch()` requests to a **Django REST Framework** API. The API validates data (amount > 0, required fields, no future dates, valid category) both while serializing and, on the frontend, before the request is even sent. Data is persisted in **SQLite** via Django's ORM (`Expense` model). Users can filter expenses by category or date range and search by keyword, both handled server-side using `django-filter` and DRF's `SearchFilter`. The UI shows success/error alerts and is responsive using flexbox and media queries.

## Test Cases (for College Activity)

| # | Test Case                              | Expected Result |
|---|------------------------------------------|------------------|
| 1 | Create expense with valid data           | 201 Created, expense saved |
| 2 | Create expense with negative amount      | 400 Bad Request |
| 3 | Create expense with missing title        | 400 Bad Request |
| 4 | Create expense with future date          | 400 Bad Request |
| 5 | Create expense with invalid category     | 400 Bad Request |
| 6 | List all expenses                        | 200 OK, array returned |
| 7 | Retrieve single expense by valid id       | 200 OK |
| 8 | Retrieve expense with invalid id          | 404 Not Found |
| 9 | Update expense (PUT) with valid data      | 200 OK, fields updated |
| 10| Partial update (PATCH) amount only        | 200 OK, only amount changes |



