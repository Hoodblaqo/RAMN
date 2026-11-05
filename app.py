import os
import sqlite3
import secrets
import hashlib
import hmac
import urllib.request
import urllib.error
import json
from functools import wraps
from flask import Flask, request, redirect, url_for, session, render_template_string, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get("RAMN_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True,
    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 7,
)

DB_PATH = os.environ.get("RAMN_DB_PATH", "ramn.sqlite3")
OWNER_PASSWORD = os.environ.get("RAMN_OWNER_PASSWORD", "")
CHAT_MODEL = os.environ.get("RAMN_CHAT_MODEL", "auto:smart")
AI_ENDPOINT = "https://api.llmfaucet.dev/v1/chat/completions"

PAGE = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAMN â Personal AI</title>
<style>
:root{color-scheme:dark;--bg:#070b14;--panel:#101a2b;--line:#203653;--blue:#56c8ff;--muted:#91a6bd;--red:#ff647c}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -15%,#15385c 0,transparent 55%),var(--bg);color:#eaf5ff;font:16px system-ui,-apple-system,sans-serif;min-height:100vh}
header{display:flex;justify-content:space-between;align-items:center;padding:18px max(20px,calc((100% - 980px)/2));border-bottom:1px solid #203653;background:#08101ddd;position:sticky;top:0;backdrop-filter:blur(14px)}
.brand{font-weight:900;letter-spacing:.24em;color:var(--blue)}a{color:var(--blue);text-decoration:none}main{max-width:900px;margin:38px auto;padding:0 18px}
.card{background:#101a2beF;border:1px solid var(--line);border-radius:18px;padding:22px;margin:16px 0;box-shadow:0 18px 60px #0005}
h1{font-size:clamp(30px,7vw,54px);margin:0 0 8px;letter-spacing:.08em}h2{margin-top:0}.muted{color:var(--muted)}.status{color:#6ce5bb;font-size:12px;letter-spacing:.16em}
input,textarea,button{font:inherit;border-radius:10px;border:1px solid #294563;padding:12px;background:#081321;color:#eff8ff;width:100%;margin:6px 0}
textarea{min-height:100px;resize:vertical}button{background:#12385a;border-color:#2874a8;color:#fff;font-weight:700;cursor:pointer}button:hover{background:#18517d}.danger{background:#4c1c2a;border-color:#a23a55}.inline{display:flex;gap:10px;align-items:center}.inline>*{flex:1}
.chatlog{white-space:pre-wrap;line-height:1.55;max-height:45vh;overflow:auto}.msg{padding:12px 14px;border-radius:12px;margin:10px 0;background:#0a1422;border:1px solid #1c3048}.user{border-left:3px solid var(--blue)}.ramn{border-left:3px solid #6ce5bb}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
small{color:var(--muted)}.flash{padding:12px;border-radius:10px;background:#172b42;margin:10px 0}.badge{color:#ff9aa9}.nav{display:flex;gap:14px;align-items:center}.nav form{margin:0}
@media(max-width:600px){header{padding:14px 16px}.inline{flex-direction:column}.card{padding:16px}}
</style></head><body>
<header><a class="brand" href="/">R A M N</a><nav class="nav">
{% if user %}<span class="muted">{{ user }}</span><a href="/owner">OWNER</a><form method="post" action="/logout"><button>Logout</button></form>{% else %}<a href="/login">Login</a><a href="/register">Register</a>{% endif %}
</nav></header>
<main>
{% with messages=get_flashed_messages() %}{% for m in messages %}<div class="flash">{{m}}</div>{% endfor %}{% endwith %}
{% if page == 'home' %}
<section class="card"><div class="status">PERSONAL AI SYSTEM Â· ONLINE</div><h1>RAMN</h1><p class="muted">A personal AI assistant. Sign in to start a conversation.</p>
{% if user %}<form method="post" action="/chat"><textarea name="message" placeholder="Ask RAMN anything..." required maxlength="4000"></textarea><button>Send to RAMN â</button></form>
<div class="chatlog">{% for m in history %}<div class="msg {{m.role}}"><b>{{'YOU' if m.role=='user' else 'RAMN'}}</b><br>{{m.text}}</div>{% endfor %}</div>
{% if not configured %}<p class="muted">RAMN uses a free community AI gateway. Responses may be rate-limited or temporarily unavailable.</p>{% endif %}
{% else %}<div class="inline"><a href="/register">Create account</a><a href="/login">Sign in</a></div>{% endif %}
</section><p class="muted"><small>RAMN is an independent project. Do not submit passwords, payment details or sensitive information to the AI.</small></p>
{% elif page == 'login' or page == 'register' %}
<section class="card"><h2>{{'Create account' if page=='register' else 'Sign in'}}</h2><form method="post"><input name="username" placeholder="Username" minlength="3" maxlength="24" pattern="[A-Za-z0-9_]+" required><input name="password" type="password" placeholder="Password" minlength="8" required><button>{{'Register' if page=='register' else 'Login'}}</button></form></section>
{% elif page == 'owner_login' %}
<section class="card"><h2>Owner access</h2><p class="muted">Private administration area.</p><form method="post"><input name="password" type="password" placeholder="Owner password" required><button>Unlock owner panel</button></form></section>
{% elif page == 'owner' %}
<section class="card"><div class="status">RESTRICTED ACCESS</div><h1>OWNER</h1><p class="muted">User moderation console</p><p>Total accounts: <b>{{ users|length }}</b> Â· Banned: <b>{{ banned|length }}</b></p>
<table><tr><th>Username</th><th>Status</th><th>Action</th></tr>{% for u in users %}<tr><td>{{u.username}}</td><td>{% if u.banned %}<span class="badge">BANNED</span>{% else %}Active{% endif %}</td><td>{% if u.username.lower() != 'ramn' %}<form method="post" action="/owner/toggle"><input type="hidden" name="username" value="{{u.username}}"><button class="{{'danger' if not u.banned else ''}}">{{'Unban' if u.banned else 'Ban user'}}</button></form>{% else %}â{% endif %}</td></tr>{% endfor %}</table>
<form method="post" action="/owner/logout"><button class="danger">Lock owner panel</button></form></section>
{% endif %}
</main></body></html>
"""

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            banned INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        if OWNER_PASSWORD:
            exists = con.execute("SELECT 1 FROM users WHERE username=?", ("Ramn",)).fetchone()
            if not exists:
                con.execute("INSERT INTO users(username,password_hash) VALUES(?,?)",
                            ("Ramn", hash_password(OWNER_PASSWORD)))

def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240000)
    return salt.hex() + "$" + digest.hex()

def check_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 240000)
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False

def current_user():
    name = session.get("username")
    if not name:
        return None
    with db() as con:
        row = con.execute("SELECT username,banned FROM users WHERE username=?", (name,)).fetchone()
    if not row or row["banned"]:
        session.clear()
        return None
    return row["username"]

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def owner_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("owner_ok"):
            return redirect(url_for("owner_login"))
        return fn(*args, **kwargs)
    return wrapped

def page(name, **kwargs):
    return render_template_string(PAGE, page=name, user=current_user(),
                                  configured=True,
                                  history=session.get("history", []), **kwargs)

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/")
def home():
    return page("home")

@app.route("/health")
def health():
    return {"status": "ok", "app": "RAMN"}

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not (3 <= len(username) <= 24) or not username.replace("_", "").isalnum():
            flash("Username: 3â24 letters, numbers or underscores.")
        elif username.lower() == "ramn":
            flash("That username is reserved for the site owner.")
        elif len(password) < 8:
            flash("Password must have at least 8 characters.")
        else:
            try:
                with db() as con:
                    con.execute("INSERT INTO users(username,password_hash) VALUES(?,?)",
                                (username, hash_password(password)))
                session.clear()
                session["username"] = username
                session.permanent = True
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("That username is already taken.")
    return page("register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with db() as con:
            row = con.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if row and check_password(password, row["password_hash"]):
            if row["banned"]:
                flash("This account has been suspended.")
            else:
                session.clear()
                session["username"] = username
                session.permanent = True
                return redirect(url_for("home"))
        else:
            flash("Invalid username or password.")
    return page("login")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    message = request.form.get("message", "").strip()
    if not message or len(message) > 4000:
        flash("Message is empty or too long.")
        return redirect(url_for("home"))
    history = session.get("history", [])
    messages = [{"role": "system", "content": "You are RAMN, a helpful, calm personal AI assistant. Reply in the user's language, German by default. Be honest about actions and capabilities."}]
    for item in history[-10:]:
        role = "assistant" if item.get("role") in ("ramn", "assistant") else "user"
        messages.append({"role": role, "content": item.get("content", item.get("text", ""))})
    messages.append({"role": "user", "content": message})
    body = json.dumps({"model": CHAT_MODEL, "messages": messages, "temperature": 0.7}).encode()
    req = urllib.request.Request(AI_ENDPOINT, data=body,
        headers={"Authorization": "Bearer free", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
        answer = result["choices"][0]["message"]["content"]
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as error:
        flash("Free AI is busy or unavailable right now. Try again in a moment. " + str(error)[:120])
        return redirect(url_for("home"))
    history.extend([{"role": "user", "text": message, "content": message},
                    {"role": "ramn", "text": answer, "content": answer}])
    session["history"] = history[-12:]
    return redirect(url_for("home"))

@app.route("/owner", methods=["GET"])
@owner_required
def owner():
    with db() as con:
        users = con.execute("SELECT username,banned FROM users ORDER BY created_at DESC").fetchall()
    return page("owner", users=users, banned=[u for u in users if u["banned"]])

@app.route("/owner/login", methods=["GET", "POST"])
def owner_login():
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if not OWNER_PASSWORD:
            flash("Owner login is disabled. Set RAMN_OWNER_PASSWORD in Render environment variables first.")
        elif hmac.compare_digest(supplied, OWNER_PASSWORD):
            session["owner_ok"] = True
            session.permanent = True
            return redirect(url_for("owner"))
        else:
            flash("Incorrect owner password.")
    return page("owner_login")

@app.route("/owner/toggle", methods=["POST"])
@owner_required
def owner_toggle():
    username = request.form.get("username", "").strip()
    if username.lower() in ("owner", "ramn"):
        abort(400)
    with db() as con:
        row = con.execute("SELECT banned FROM users WHERE username=?", (username,)).fetchone()
        if row:
            con.execute("UPDATE users SET banned=? WHERE username=?",
                        (0 if row["banned"] else 1, username))
    return redirect(url_for("owner"))

@app.route("/owner/logout", methods=["POST"])
@owner_required
def owner_logout():
    session.pop("owner_ok", None)
    return redirect(url_for("home"))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
