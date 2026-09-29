# ✈ SkyShield - Aviation Incident Reporting & Safety Management System

**SkyShield** is a web-based aviation safety incident tracking platform developed with **Django** and powered by **MySQL**. It enables flight crews, safety officers, and ground operations to log, review, and investigate operational occurrences, safety hazards, and technical issues.

---

## 🚀 Features

- **Incident Reporting Form**: A clean and intuitive form for pilots and aviation staff to report incidents with validation. Automatically links reports to the authenticated user.
- **Incident Registry (List Page)**: Displays all recorded safety incidents with real-time safety KPI counters (Total, Active/Investigating, Critical), keyword search, and filters (by category, severity, and status).
- **Incident Detail Page**: Comprehensive incident review including full event narrative, aircraft details, occurrence timestamp, location, and reporter metadata.
- **User Authentication**: Complete login, logout, and registration flow with user badges.
- **Django Admin Integration**: Fully configured admin dashboard with search fields, list filters, ordering, and date hierarchy for safety auditors.
- **MySQL Database Backend**: Configured for MySQL using `pymysql` as the database connector with environment-based configuration via `.env`.
- **Sample Data Seeder**: Built-in management command to seed realistic aviation incident records.

---

## 📋 Data Model (`Incident`)

The `Incident` model inside the `incidents` app captures the following fields:

| Field | Type | Description / Choices |
| :--- | :--- | :--- |
| `title` | `CharField(max_length=200)` | Summary of the incident |
| `description` | `TextField` | Detailed event narrative |
| `date_time` | `DateTimeField` | Date & time when the incident took place |
| `location` | `CharField(max_length=200)` | Airport code, waypoint, or airspace coordinates |
| `aircraft_type` | `CharField(max_length=100)` | Aircraft model (e.g. *Boeing 737-800*, *Airbus A320*) |
| `category` | `CharField(max_length=50)` | `bird_strike`, `technical_fault`, `weather`, `human_error`, `other` |
| `severity` | `CharField(max_length=20)` | `low`, `medium`, `high`, `critical` |
| `status` | `CharField(max_length=20)` | `reported`, `under_review`, `investigating`, `closed` |
| `reported_by` | `ForeignKey(User)` | Reference to the user who filed the report |
| `created_at` | `DateTimeField(auto_now_add=True)`| System timestamp when the report was logged |

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:
- **Python**: Version 3.10 or higher
- **MySQL Server**: MySQL 8.0+, MariaDB 10.5+, or via XAMPP / Docker

---

## ⚙️ Setup & Installation

### 1. Navigate to the Project Directory
```bash
cd "path/to/SkyShield"
```

### 2. (Recommended) Create and Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the MySQL Database
Log into your MySQL CLI or use a database management tool (MySQL Workbench, phpMyAdmin, DBeaver):

```sql
CREATE DATABASE skyshield_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables (`.env`)
A `.env` file is included in the project root. Update the database credentials to match your MySQL setup:

```ini
# SkyShield Environment Configuration
DB_ENGINE=mysql
DB_NAME=skyshield_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Switch to True if running tests without a live MySQL instance
USE_SQLITE=False

SECRET_KEY=django-insecure-ebvu!8z@k(4-)g&_x@5cpw#$4jsplgigs5o*%0#s)h93&)v2hk
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 6. Apply Database Migrations
Run the migrations to create the database tables in MySQL:
```bash
python manage.py migrate
```

### 7. Create a Superuser / Admin Account
To access the Django admin portal:
```bash
python manage.py createsuperuser
```
Follow the prompts to specify a username, email, and password.

### 8. (Optional) Seed Sample Aviation Incidents
Populate your database with realistic demo incidents and a test reporter account (`demo_pilot` / `Pilot1234!`):
```bash
python manage.py seed_incidents
```

### 9. Start the Development Server
```bash
python manage.py runserver
```

The application will be live at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🗺️ Application Routes

| URL | View | Purpose |
| :--- | :--- | :--- |
| `/` | `incident_list` | Incident registry, search, filters & safety metrics |
| `/incidents/report/` | `incident_create` | Form page to submit a new incident (requires login) |
| `/incidents/<id>/` | `incident_detail` | Detailed view of an individual incident |
| `/login/` | `LoginView` | Pilot / User login page |
| `/logout/` | `user_logout` | Safe logout endpoint |
| `/register/` | `register` | Self-service registration for new reporting personnel |
| `/admin/` | `admin.site.urls` | Django administrative interface |

---

## 🧪 Running Automated Tests

A comprehensive test suite covering models, views, forms, search/filtering, and authentication is included. Run the tests with:

```bash
python manage.py test
```
*(Note: You can pass `$env:USE_SQLITE="True"` or set `USE_SQLITE=True` in `.env` to execute tests against an in-memory database).*

---

## 📁 Project Structure

```
SkyShield/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── README.md
├── skyshield/
│   ├── __init__.py        # PyMySQL MySQLdb installation hook
│   ├── settings.py        # Django settings with MySQL backend & .env support
│   ├── urls.py            # Global routing
│   ├── wsgi.py
│   └── asgi.py
├── incidents/
│   ├── admin.py           # IncidentAdmin with filters, search, and hierarchy
│   ├── apps.py
│   ├── forms.py           # IncidentForm & UserRegisterForm
│   ├── models.py          # Incident model with categories, severities, and statuses
│   ├── tests.py           # Unit and integration test suite
│   ├── urls.py            # App-level routing
│   ├── views.py           # List, detail, create, register, logout views
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── management/
│       └── commands/
│           └── seed_incidents.py
├── static/
│   └── css/
│       └── style.css      # Custom aviation-themed stylesheet
└── templates/
    ├── base.html          # Base layout with navigation and flash alerts
    ├── incidents/
    │   ├── incident_list.html
    │   ├── incident_detail.html
    │   └── incident_form.html
    └── registration/
        ├── login.html
        └── register.html
```
