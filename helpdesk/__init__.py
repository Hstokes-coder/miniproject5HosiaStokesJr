# INF601 - Advanced Programming in Python
# Hosia Stokes Jr
# Mini Project 5

import os

from flask import Flask, render_template


def create_app(test_config=None):
    """Application factory: builds, configures, and returns the Flask app."""
    # instance_relative_config=True tells Flask that config files and the
    # database live in the "instance" folder, which is kept out of Git.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # SECRET_KEY signs the session cookie. "dev" is fine locally;
        # a real deployment would use a long random value.
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "helpdesk.sqlite"),
    )

    if test_config is None:
        # Load instance/config.py if it exists (optional overrides).
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Used later for testing with a temporary database.
        app.config.from_mapping(test_config)

    # Make sure the instance folder exists so SQLite can create the file.
    os.makedirs(app.instance_path, exist_ok=True)

    # Register database helpers and the init-db command.
    from . import db
    db.init_app(app)

    # Register the authentication blueprint (register, login, logout).
    from . import auth
    app.register_blueprint(auth.bp)

    # Register the tickets blueprint (list, create, view).
    from . import tickets
    app.register_blueprint(tickets.bp)

    @app.route("/")
    def index():
        """GET: show the public homepage with the 'How it works' modal."""
        return render_template("index.html")

    return app
