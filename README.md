# IT Help Desk Ticket System

**INF601 - Advanced Programming in Python**
**Hosia Stokes Jr**
**Mini Project 5**

A Flask web application where users create an account, submit IT support tickets, and track them until they are resolved. Each user can view, edit, update the status of, and delete only their own tickets.

## Features

- **User accounts**: register, log in, and log out. Passwords are stored as secure one-way hashes (Werkzeug), never as plain text.
- **Ticket management**: create, list, view, edit, and delete support tickets.
- **Priority and status**: tickets have a priority (Low / Medium / High) and a status (Open / In Progress / Closed), shown as colored badges.
- **Ownership protection**: users can only see and change their own tickets; anyone else gets a 403 Forbidden error.
- **Input validation**: every form checks its input on the server and shows a clear error message instead of crashing.
- **Bootstrap 5 styling** with two working modals: a "How it works" pop-up on the homepage and a delete confirmation on each ticket.

## Technologies

Python 3, Flask, Jinja2 templates, SQLite, Bootstrap 5, HTML/CSS, Git.

## Project Structure

The layout follows the official Flask tutorial (application factory + blueprints).

```
miniproject5HosiaStokesJr/
├── helpdesk/                 # The application package
│   ├── __init__.py           # create_app() application factory
│   ├── db.py                 # Database connection and the init-db command
│   ├── schema.sql            # Table definitions (user, ticket)
│   ├── auth.py               # Blueprint: register, login, logout
│   ├── tickets.py            # Blueprint: ticket list, create, view, edit, delete
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── base.html         # Shared layout: Bootstrap, navbar, flash messages
│       ├── index.html        # Homepage with "How it works" modal
│       ├── auth/
│       │   ├── register.html
│       │   └── login.html
│       └── tickets/
│           ├── _macros.html  # Reusable status/priority badges
│           ├── index.html    # My Tickets
│           ├── create.html   # New Ticket form
│           ├── detail.html   # Ticket detail + delete modal
│           └── update.html   # Edit Ticket form
├── instance/                 # Created automatically; holds the SQLite database (not in Git)
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository** and move into it:
   ```bash
   git clone https://github.com/<your-github-username>/miniproject5HosiaStokesJr.git
   cd miniproject5HosiaStokesJr
   ```

2. **Create and activate a virtual environment:**

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## Initialize the Database

Run this once before starting the app for the first time:

```bash
flask --app helpdesk init-db
```

You should see `Initialized the database.` This creates `instance/helpdesk.sqlite` with the `user` and `ticket` tables.

> **Warning:** running `init-db` again deletes all existing users and tickets and starts with an empty database.

## Run the Development Server

```bash
flask --app helpdesk run --debug
```

Then open **http://127.0.0.1:5000** in your browser. Press `Ctrl + C` in the terminal to stop the server.

## How to Use

1. Click **Register** and create an account (password must be at least 8 characters).
2. **Log In** with that account.
3. Click **New Ticket**, fill in a title, description, and priority, and submit it.
4. Open **My Tickets** to see all of your tickets, and click a title to view it.
5. On a ticket's page, click **Edit** to change its details or status, or **Delete** to remove it (a confirmation modal appears first).

## Pages and Routes

| Method | URL | Page / Action | Login required |
|---|---|---|---|
| GET | `/` | Homepage with "How it works" modal | No |
| GET, POST | `/auth/register` | Show sign-up form / create account | No |
| GET, POST | `/auth/login` | Show login form / check credentials | No |
| GET | `/auth/logout` | Log out and return home | No |
| GET | `/tickets/` | My Tickets list | Yes |
| GET, POST | `/tickets/create` | Show new-ticket form / save ticket | Yes |
| GET | `/tickets/<id>` | Ticket detail | Yes (owner only) |
| GET, POST | `/tickets/<id>/update` | Show edit form / save changes | Yes (owner only) |
| POST | `/tickets/<id>/delete` | Delete ticket (from confirmation modal) | Yes (owner only) |

That is **7 pages**: Home, Register, Log In, My Tickets, New Ticket, Ticket Detail, and Edit Ticket.

## Database

Two tables linked by a foreign key (one user has many tickets):

**user**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| username | TEXT | Unique, required |
| password | TEXT | Hashed password |

**ticket**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | **Foreign key → user.id** |
| created | TIMESTAMP | Set automatically (UTC) |
| title | TEXT | Required, max 100 characters |
| description | TEXT | Required |
| priority | TEXT | Low, Medium, or High |
| status | TEXT | Open, In Progress, or Closed |

## Testing

The application was tested manually in the browser and with automated checks using Flask's test client. Tests covered:

- Every page loading correctly for GET requests
- Valid form submissions (POST) saving data and redirecting
- Empty or invalid form input showing error messages
- Logged-out visitors being redirected to the login page
- Users receiving **403 Forbidden** when trying to view, edit, or delete another user's ticket
- Missing tickets returning **404 Not Found**
- Deletion only being possible through a POST request (a GET returns **405**)

## AI Usage

For Mini Project 5 in my Advanced Programming with Python course, I developed an IT Help Desk Ticket System using Flask, Python, SQLite, HTML, CSS, Bootstrap, and Git. I set up my Python virtual environment, installed Flask, and wrote the initial starter application. With assistance from Claude (Anthropic's AI assistant), I restructured the project to follow the official Flask tutorial and built a website where users can register, log in, create support tickets, view their tickets, update them, and delete them using a Bootstrap confirmation modal. The SQLite database contains two related tables, `user` and `ticket`, connected through a foreign key so that each ticket belongs to the user who created it. Passwords are stored as secure hashes, and users can only view or change their own tickets.

Throughout development, I manually tested registration, login, ticket management, and security restrictions such as blocking other users' tickets. I learned how GET and POST requests work, how Flask routes connect URLs to Python functions, how sessions keep users logged in, and how Git commits track changes. I made six Git commits, exceeding the five required.

Claude wrote most of the application code and ran automated tests. I configured Git and the environment, generated `requirements.txt`, ran and manually tested each feature, reviewed the changes, debugged issues with Claude's guidance, and made every commit myself.
