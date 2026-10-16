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
STATUSES = ("Open", "In Progress", "Closed")


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


def validate_ticket_form(form):
    """Clean and check the shared ticket fields.

    Returns (title, description, priority, error). error is None when valid.
    Used by both create() and update() so the rules live in one place.
    """
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    priority = form.get("priority", "")
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

    return title, description, priority, error


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
        title, description, priority, error = validate_ticket_form(request.form)

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



@bp.route("/<int:ticket_id>/update", methods=("GET", "POST"))
@login_required
def update(ticket_id):
    """GET shows the edit form filled in; POST validates and saves changes."""
    ticket = get_ticket(ticket_id)  # also blocks other users with 403

    if request.method == "POST":
        title, description, priority, error = validate_ticket_form(request.form)
        status = request.form.get("status", "")
        if error is None and status not in STATUSES:
            error = "Please choose a valid status."

        if error is None:
            db = get_db()
            db.execute(
                "UPDATE ticket SET title = ?, description = ?, priority = ?, status = ?"
                " WHERE id = ?",
                (title, description, priority, status, ticket_id),
            )
            db.commit()
            flash("Ticket updated.", "success")
            return redirect(url_for("tickets.detail", ticket_id=ticket_id))

        flash(error, "danger")

    return render_template(
        "tickets/update.html", ticket=ticket, priorities=PRIORITIES, statuses=STATUSES
    )


@bp.route("/<int:ticket_id>/delete", methods=("POST",))
@login_required
def delete(ticket_id):
    """Delete a ticket. POST only, so a plain link can't trigger it by accident."""
    get_ticket(ticket_id)  # 404 if missing, 403 if not yours
    db = get_db()
    db.execute("DELETE FROM ticket WHERE id = ?", (ticket_id,))
    db.commit()
    flash(f"Ticket #{ticket_id} deleted.", "info")
    return redirect(url_for("tickets.index"))
