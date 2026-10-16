# INF601 - Advanced Programming in Python
# Hosia Stokes Jr
# Mini Project 5

from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)

from helpdesk.auth import login_required
from helpdesk.db import get_db

# url_prefix means every route in this file starts with /tickets.
bp = Blueprint("tickets", __name__, url_prefix="/tickets")

# Allowed values, matching the CHECK rules in schema.sql.
PRIORITIES = ("Low", "Medium", "High")


def get_ticket(ticket_id):
    """Fetch one ticket, or stop with an error if it's missing or not yours."""
    # JOIN uses the foreign key to pull in the owner's username too.
    ticket = get_db().execute(
        "SELECT t.id, t.user_id, t.created, t.title, t.description,"
        " t.priority, t.status, u.username"
        " FROM ticket t JOIN user u ON t.user_id = u.id"
        " WHERE t.id = ?",
        (ticket_id,),
    ).fetchone()

    if ticket is None:
        abort(404, f"Ticket #{ticket_id} doesn't exist.")
    if ticket["user_id"] != g.user["id"]:
        abort(403)  # Forbidden: it belongs to someone else.
    return ticket


@bp.route("/")
@login_required
def index():
    """List the logged-in user's tickets, newest first."""
    tickets = get_db().execute(
        "SELECT id, created, title, priority, status FROM ticket"
        " WHERE user_id = ? ORDER BY created DESC, id DESC",
        (g.user["id"],),
    ).fetchall()
    return render_template("tickets/index.html", tickets=tickets)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """GET shows the new-ticket form; POST validates and saves it."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "")
        error = None

        if not title:
            error = "Title is required."
        elif len(title) > 100:
            error = "Title must be 100 characters or fewer."
        elif not description:
            error = "Description is required."
        elif len(description) > 2000:
            error = "Description must be 2000 characters or fewer."
        elif priority not in PRIORITIES:
            # Checked on the server too, in case someone edits the HTML.
            error = "Please choose a valid priority."

        if error is None:
            db = get_db()
            cursor = db.execute(
                "INSERT INTO ticket (user_id, title, description, priority)"
                " VALUES (?, ?, ?, ?)",
                (g.user["id"], title, description, priority),
            )
            db.commit()
            flash("Ticket submitted!", "success")
            # lastrowid is the id SQLite gave the new ticket.
            return redirect(url_for("tickets.detail", ticket_id=cursor.lastrowid))

        flash(error, "danger")

    return render_template("tickets/create.html", priorities=PRIORITIES)


@bp.route("/<int:ticket_id>")
@login_required
def detail(ticket_id):
    """Show one ticket. <int:ticket_id> captures the number from the URL."""
    ticket = get_ticket(ticket_id)
    return render_template("tickets/detail.html", ticket=ticket)
