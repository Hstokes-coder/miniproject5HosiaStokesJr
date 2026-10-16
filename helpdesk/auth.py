# INF601 - Advanced Programming in Python
# Hosia Stokes Jr
# Mini Project 5

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from helpdesk.db import get_db

# A blueprint groups related routes. Every route here starts with /auth.
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """GET shows the sign-up form; POST validates it and creates the user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        error = None

        # Input validation: check every rule before touching the database.
        if not username:
            error = "Username is required."
        elif len(username) > 30:
            error = "Username must be 30 characters or fewer."
        elif not password:
            error = "Password is required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm:
            error = "Passwords do not match."

        if error is None:
            db = get_db()
            try:
                # The ? placeholders let sqlite3 insert values safely,
                # which prevents SQL injection.
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The UNIQUE rule on username rejected a duplicate.
                error = f"Username '{username}' is already taken."
            else:
                flash("Account created! Please log in.", "success")
                return redirect(url_for("auth.login"))

        flash(error, "danger")

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """GET shows the login form; POST checks the credentials."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        # Same message for both cases, so attackers can't tell
        # which usernames exist.
        if user is None or not check_password_hash(user["password"], password):
            flash("Incorrect username or password.", "danger")
        else:
            # Start a fresh session that remembers who logged in.
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Welcome, {user['username']}!", "success")
            return redirect(url_for("index"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Forget the logged-in user and return to the homepage."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    """Before every request, load the logged-in user (if any) into g.user."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


def login_required(view):
    """Decorator: send logged-out visitors to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
