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

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
