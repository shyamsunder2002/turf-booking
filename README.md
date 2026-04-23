# TurfBook — Football Turf Booking Web Application

A secure web application for booking football turfs in Dublin, built with Python Flask and SQLite.

## Project Overview
TurfBook allows users to browse available football turfs, make bookings, and manage their reservations. 
The application demonstrates secure web development practices by intentionally starting with common 
vulnerabilities and progressively implementing security fixes.

## Features
- User registration and login
- Browse available football turfs
- Book, view and cancel reservations
- Admin panel to manage turfs and view all bookings
- Two user roles: customer and admin

## Security Improvements
1. **SQL Injection Prevention** — Replaced raw string SQL queries with parameterized queries
2. **Password Hashing** — Implemented bcrypt hashing for all passwords instead of plaintext storage
3. **Secure Session Configuration** — Added HttpOnly cookies, SameSite policy and 30 minute timeout

## Technology Stack
- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML, Bootstrap 5
- **Security:** Flask-Bcrypt

## Project Structure
- `app.py` — Main Flask application and all routes
- `database.py` — Database setup and connection helper
- `templates/` — HTML pages
- `static/` — CSS styles

## Setup and Installation
1. Clone the repository:
   `git clone https://github.com/shyamsunder2002/turf-booking.git`
2. Navigate into the folder:
   `cd turf-booking`
3. Create virtual environment:
   `python -m venv venv`
4. Activate virtual environment:
   `venv\Scripts\activate`
5. Install dependencies:
   `pip install flask flask-bcrypt`
6. Run the application:
   `python app.py`
7. Open browser and go to:
   `http://127.0.0.1:5000`

## Default Admin Login
- Username: `admin`
- Password: `admin123`

## Security Requirements Table
| ID | Requirement | Status | Completion |
|----|-------------|--------|------------|
| 1 | Parameterized queries to prevent SQL injection | Completed | 100% |
| 2 | Password hashing using bcrypt | Completed | 100% |
| 3 | Secure session configuration | Completed | 100% |
| 4 | Role-based access control | Completed | 100% |
| 5 | Input validation on registration | Completed | 100% |

## Testing
- Functional testing performed manually on all routes
- SQL injection tested by attempting bypass on login page
- Password hashing verified by checking database values
- Session timeout verified after 30 minutes of inactivity

## References
- Flask Documentation: https://flask.palletsprojects.com
- Flask-Bcrypt: https://flask-bcrypt.readthedocs.io
- OWASP Top 10: https://owasp.org/www-project-top-ten
- Bootstrap 5: https://getbootstrap.com

## Running Security Tests

To run Bandit SAST scan on the project:
pip install bandit
bandit -r app.py database.py

To test SQL injection manually:
1. Switch to the vulnerable branch: git checkout vulnerable
2. Run the app: python app.py
3. Go to login page and enter: ' OR '1'='1 as username
4. Observe authentication bypass
5. Switch back to main: git checkout main
6. Repeat - observe it is blocked