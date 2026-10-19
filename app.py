"""Flask login demo with a parameterized SQLite query."""

import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE = "users.db"


def init_db():
    """Initialize the database and insert a demo account if needed."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username TEXT PRIMARY KEY, password TEXT NOT NULL)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "supersecret"),
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    """Display the login form and process submitted credentials."""
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Parameterized query prevents SQL injection through user input.
        cursor.execute(
            "SELECT username FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login berhasil! Selamat datang."
            status_class = "success"
        else:
            message = "Login gagal! Kredensial tidak valid."
            status_class = "danger"

    return render_template(
        "index.html", message=message, status_class=status_class
    )


@app.route("/health", methods=["GET"])
def health():
    """Return a simple health-check response."""
    return {"status": "ok"}, 200



if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)

