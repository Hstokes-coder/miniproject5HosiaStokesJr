# INF601 - Advanced Programming in Python
# Hosia Stokes Jr
# Mini Project 5

import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    """Return the database connection for the current request, opening it if needed."""
    # `g` is a per-request storage object. Storing the connection there means
    # every function in the same request reuses one connection.
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Row objects let us access columns by name: row["title"]
        g.db.row_factory = sqlite3.Row
        # SQLite ignores foreign keys unless this is switched on per connection.
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Close the connection at the end of the request, if one was opened."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Clear any existing data and create fresh tables from schema.sql."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Terminal command: flask --app helpdesk init-db"""
    init_db()
    click.echo("Initialized the database.")


# Convert TIMESTAMP columns from text into Python datetime objects.
sqlite3.register_converter(
    "timestamp", lambda value: datetime.fromisoformat(value.decode())
)


def init_app(app):
    """Register the database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
