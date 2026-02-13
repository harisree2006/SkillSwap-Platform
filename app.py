from flask import Flask, render_template, request, redirect, session, flash
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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_id INTEGER,
            skill TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # NEW: Table to store chat messages
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create default admin (only once)
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
            return redirect("/login")
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
            session["user_id"], session["role"] = user["id"], user["role"]
            return redirect("/admin_dashboard" if user["role"] == "admin" else "/dashboard")
        flash("Invalid credentials!")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session: return redirect("/login")
    if session.get("role") == "admin": return redirect("/admin_dashboard")

    conn = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        if "give_skill" in request.form:
            conn.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (user_id, request.form["give_skill"]))
        if "want_skill" in request.form:
            conn.execute("INSERT INTO requests (requester_id, skill) VALUES (?, ?)", (user_id, request.form["want_skill"]))
        if "match_user_id" in request.form:
            if request.form["direction"] == "right":
                # Save the match by recording the user ID in the skill field for easy lookup
                conn.execute("INSERT INTO requests (requester_id, skill, status) VALUES (?, ?, ?)", 
                             (user_id, "Match:" + request.form["match_user_id"], "Accepted"))
        conn.commit()
        return redirect("/dashboard")

    # Discovery logic to find users who teach what you want to learn
    my_wants = [r['skill'] for r in conn.execute("SELECT skill FROM requests WHERE requester_id=?", (user_id,)).fetchall()]
    card = None
    if my_wants:
        placeholders = ', '.join(['?'] * len(my_wants))
        query = f"SELECT u.id, u.username, s.skill as offering FROM users u JOIN skills s ON u.id = s.user_id WHERE u.id != ? AND s.skill IN ({placeholders}) ORDER BY RANDOM() LIMIT 1"
        card = conn.execute(query, (user_id, *my_wants)).fetchone()
    
    conn.close()
    return render_template("dashboard.html", card=card)

# ---------------- MATCHES & MESSAGING ---------------- #

@app.route("/matches")
def matches():
    if "user_id" not in session: return redirect("/login")
    conn = get_db()
    uid = session["user_id"]
    # Find users where you swiped right and a match was created
    my_matches = conn.execute("""
        SELECT DISTINCT u.id, u.username 
        FROM users u 
        JOIN requests r ON r.skill LIKE 'Match:' || u.id
        WHERE r.requester_id = ? AND r.status = 'Accepted'
    """, (uid,)).fetchall()
    conn.close()
    return render_template("matches.html", matches=my_matches)

@app.route("/chat/<int:receiver_id>", methods=["GET", "POST"])
def chat(receiver_id):
    if "user_id" not in session: return redirect("/login")
    conn = get_db()
    uid = session["user_id"]

    if request.method == "POST":
        msg = request.form.get("message")
        if msg:
            conn.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)", (uid, receiver_id, msg))
            conn.commit()

    # Fetch message history between these two users
    messages = conn.execute("""
        SELECT * FROM messages 
        WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?) 
        ORDER BY timestamp ASC
    """, (uid, receiver_id, receiver_id, uid)).fetchall()
    
    receiver = conn.execute("SELECT username FROM users WHERE id=?", (receiver_id,)).fetchone()
    conn.close()
    return render_template("chat.html", messages=messages, receiver=receiver, receiver_id=receiver_id)

# ---------------- ADMIN DASHBOARD ---------------- #

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin": return redirect("/")
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    requests_list = conn.execute("SELECT * FROM requests").fetchall()
    
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_requests = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    total_matches = conn.execute("SELECT COUNT(*) FROM requests WHERE status='Accepted'").fetchone()[0]
    
    conn.close()
    return render_template("admin_dashboard.html", users=users, requests=requests_list, 
                           total_users=total_users, total_requests=total_requests, total_matches=total_matches)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)