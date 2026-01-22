# Fly Tau - Flight Management System

**Information Systems Engineering Course Project**
**Tel Aviv University, Group 16**

Fly Tau is a comprehensive web-based flight management application designed to streamline the experience for both passengers and airline managers. Built with Python (Flask) and MySQL, it offers a robust platform for searching flights, booking seats, and managing airline operations.

## Features

### For Customers & Guests:
*   **Flight Search:** Advanced search by source, destination, date, and number of passengers.
*   **Interactive Booking:** Visual seat map for selecting Economy or Business class seats.
*   **Booking Management:** View booking history (Upcoming vs. Past flights) and cancel active bookings (subject to 36-hour cancellation policy).
*   **Guest Access:** Book flights without a prior account (Guest Login).

### For Managers:
*   **Dashboard:** High-level overview of airline operations.
*   **Flight Management:** Schedule new flights, assign aircraft, and cancel flights (up to 72 hours before departure).
*   **Crew Management:** Add and manage pilots and flight attendants, checking for training and availability.
*   **Reports:** detailed analytical reports including:
    *   Monthly occupancy rates.
    *   Revenue analysis by airplane model and class.
    *   Employee flight hours.
    *   Most popular routes ("Dominant Routes").
    *   Cancellation statistics.

## Tech Stack

*   **Backend:** Python 3.x, Flask
*   **Database:** MySQL (Connector/Python)
*   **Frontend:** HTML5, CSS3, Jinja2 Templates
*   **Session Management:** Flask-Session (Filesystem)
*   **Deployment:** Ready for PythonAnywhere (Linux) & Localhost (Windows/Mac)

## Installation & Setup

### Prerequisites
*   Python 3.8+
*   MySQL Server installed locally (or a cloud instance).

### 1. Clone the Repository
```bash
git clone https://github.com/Shira-Levy/Project_Group16.git
cd Project_Group16
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
The project includes a SQL dump file `fly_tau_creation.sql` to initialize the database schema and sample data.
1.  Open your MySQL client (Workbench, CLI, etc.).
2.  Import `fly_tau_creation.sql`.
3.  Ensure the database `flytau_db` (or `ShiraLevy$flytau_db` on PythonAnywhere) is created.

### 4. Configuration
The application is pre-configured to detect your environment automatically!

*   **Localhost:**
    *   Connects to `localhost`
    *   User: `root`
    *   Password: `rootroot`
    *   Database: `flytau_db`
    
    *Note: If your local DB credentials differ, you can update the `else` block in the `db_curr()` function in `main.py`.*

*   **PythonAnywhere (Production):**
    *   Automatically detects the `PYTHONANYWHERE_DOMAIN` environment variable.
    *   Connects using configured production credentials.

## Running the Application

Run the application locally:
```bash
python main.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure

*   `main.py`: Core application logic, routes, and database handling (Single-file architecture).
*   `templates/`: HTML templates for all pages.
*   `static/`: CSS stylesheets and images.
*   `fly_tau_creation.sql`: Database schema export.
*   `flask_session_data/`: Server-side session storage (auto-generated).

## Security & Optimization

*   **SQL Injection Protection:** All queries use parameterized inputs.
*   **Environment Awareness:** Code adapts seamlessly between Dev and Prod environments.
*   **Transactional Integrity:** Critical actions (like booking or cancelling) use database transactions to ensure data consistency.
*   **Cross-OS Compatibility:** Path handling uses `os.path` to support both Windows and Linux file systems.

---
© 2026 Fly Tau. All Rights Reserved.
