from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret"

# ---------------- DATABASE CONNECTION ---------------- #

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE TABLES ---------------- #

def create_tables():
    conn = get_db()
    # User table with role
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.execute("CREATE TABLE IF NOT EXISTS skills (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, skill TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, requester_id INTEGER, skill TEXT, status TEXT DEFAULT 'Pending')")
    conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id INTEGER, receiver_id INTEGER, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    # CREATE ADMIN ACCOUNT (Username: admin, Password: admin123)
    conn.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, ("admin", "admin123", "admin"))
    conn.commit()
    conn.close()

create_tables()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username exists!")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"] # Storing role for security
            
            # Redirecting based on role
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        flash("Invalid credentials!")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session: return redirect(url_for("login"))
    # Admin regular dashboard kaananda ennu veykanamengil:
    if session.get("role") == "admin": return redirect(url_for("admin_dashboard"))

    conn = get_db()
    user_id = session["user_id"]
    if request.method == "POST":
        if "give_skill" in request.form:
            conn.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (user_id, request.form["give_skill"]))
        if "want_skill" in request.form:
            conn.execute("INSERT INTO requests (requester_id, skill) VALUES (?, ?)", (user_id, request.form["want_skill"]))
        if "match_user_id" in request.form and request.form["direction"] == "right":
            conn.execute("INSERT INTO requests (requester_id, skill, status) VALUES (?, ?, ?)", 
                         (user_id, "Match:" + request.form["match_user_id"], "Accepted"))
        conn.commit()
        return redirect(url_for("dashboard"))

    # Discovery Logic
    my_wants = [r['skill'] for r in conn.execute("SELECT skill FROM requests WHERE requester_id=?", (user_id,)).fetchall()]
    card = None
    if my_wants:
        placeholders = ', '.join(['?'] * len(my_wants))
        query = f"SELECT u.id, u.username, s.skill as offering FROM users u JOIN skills s ON u.id = s.user_id WHERE u.id != ? AND s.skill IN ({placeholders}) AND u.id NOT IN (SELECT CAST(REPLACE(skill, 'Match:', '') AS INTEGER) FROM requests WHERE requester_id = ? AND skill LIKE 'Match:%') ORDER BY RANDOM() LIMIT 1"
        card = conn.execute(query, (user_id, *my_wants, user_id)).fetchone()
    conn.close()
    return render_template("dashboard.html", card=card)

# ---------------- SECURE ADMIN MODULE ---------------- #

@app.route("/admin_dashboard")
def admin_dashboard():
    # SECURITY CHECK: Role 'admin' aayirunnal mathrame ee page kaanikkoo
    if session.get("role") != "admin":
        flash("Access Denied: Only Admins can enter here.")
        return redirect(url_for("home"))
    
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_matches = conn.execute("SELECT COUNT(*) FROM requests WHERE status='Accepted' AND skill LIKE 'Match:%'").fetchone()[0]
    conn.close()
    return render_template("admin_dashboard.html", users=users, total_users=total_users, total_matches=total_matches)

@app.route("/admin/delete_user/<int:user_id>")
def delete_user(user_id):
    if session.get("role") != "admin": return redirect(url_for("home"))
    
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.execute("DELETE FROM skills WHERE user_id=?", (user_id,))
    conn.execute("DELETE FROM requests WHERE requester_id=?", (user_id,))
    conn.commit()
    conn.close()
    flash(f"User #{user_id} deleted.")
    return redirect(url_for("admin_dashboard"))

# ---------------- MATCHES & LOGOUT ---------------- #

@app.route("/matches")
def matches():
    if "user_id" not in session: return redirect(url_for("login"))
    conn = get_db()
    uid = session["user_id"]
    query = "SELECT u.id, u.username FROM users u WHERE u.id IN (SELECT CAST(REPLACE(skill, 'Match:', '') AS INTEGER) FROM requests WHERE requester_id = ? AND status = 'Accepted') AND ? IN (SELECT CAST(REPLACE(skill, 'Match:', '') AS INTEGER) FROM requests WHERE requester_id = u.id AND status = 'Accepted')"
    my_matches = conn.execute(query, (uid, uid)).fetchall()
    conn.close()
    return render_template("matches.html", matches=my_matches)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)