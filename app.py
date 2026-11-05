import os
import sqlite3
import secrets
import hashlib
import hmac
import urllib.request
import urllib.error
import json
import re
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
CHAT_MODEL = os.environ.get("RAMN_CHAT_MODEL", "auto")
AI_ENDPOINT = "https://vireonix.ai/v1/chat/completions"

PAGE = r"""
<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#080d18"><title>RAMN — AI Workspace</title>
<style>
:root{color-scheme:dark;--bg:#080d18;--panel:#101a2a;--panel2:#0c1422;--line:#22344d;--blue:#65d4ff;--green:#7ce8bd;--muted:#91a4bb;--text:#edf6ff}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -15%,#15385c 0,transparent 52%),var(--bg);color:var(--text);font:15px system-ui,-apple-system,sans-serif;min-height:100vh}header{height:66px;display:flex;align-items:center;justify-content:space-between;padding:0 max(18px,calc((100% - 1120px)/2));border-bottom:1px solid var(--line);background:#080d18eF;position:sticky;top:0;z-index:4;backdrop-filter:blur(16px)}.brand{font-weight:950;letter-spacing:.3em;color:var(--blue);font-size:19px}a{color:var(--blue);text-decoration:none}.nav{display:flex;gap:16px;align-items:center}.nav form{margin:0}.nav button{width:auto;margin:0;padding:7px 12px}main{max-width:1120px;margin:28px auto;padding:0 16px}.layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:18px}.side,.panel,.card{background:linear-gradient(160deg,#121f32,#0d1625);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 60px #0004}.side{padding:16px;height:max-content;position:sticky;top:84px}.side h3{font-size:11px;color:var(--muted);letter-spacing:.16em;margin:12px 8px}.side a,.side button{display:block;width:100%;text-align:left;background:transparent;border:0;color:#d8e8f7;padding:11px;border-radius:10px;margin:3px 0}.side a:hover,.side button:hover{background:#1b3048}.hero{padding:24px 26px;margin-bottom:16px;background:radial-gradient(circle at 85% 0,#174a70 0,transparent 40%),linear-gradient(135deg,#111f33,#0c1422);border:1px solid #254663;border-radius:20px}.eyebrow,.status{font-size:11px;letter-spacing:.18em;color:var(--green);font-weight:800}.hero h1{font-size:clamp(32px,6vw,52px);letter-spacing:.12em;margin:7px 0}.muted,small{color:var(--muted)}.panel{padding:20px;margin:14px 0}.panel h2{margin:0 0 6px;font-size:19px}.chatlog{display:flex;flex-direction:column;gap:12px;max-height:54vh;overflow:auto;padding:6px 2px}.msg{max-width:92%;padding:13px 15px;border-radius:15px;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55;background:#101e30;border:1px solid #263b55}.msg.user{align-self:flex-end;background:#123451;border-color:#275a7b}.msg.ramn{align-self:flex-start}.msghead{font-size:11px;color:var(--green);font-weight:800;letter-spacing:.1em;margin-bottom:6px}.msg.user .msghead{color:var(--blue)}.msg button{width:auto;padding:4px 9px;font-size:12px;margin-top:8px}.composer{display:flex;gap:9px;align-items:flex-end;margin-top:14px}.composer textarea{flex:1;min-height:54px;max-height:150px;resize:vertical}input,textarea,button{font:inherit;border-radius:11px;border:1px solid #2a4563;padding:12px;background:#091321;color:var(--text);width:100%;margin:5px 0}button{background:linear-gradient(135deg,#155078,#17446b);border-color:#347aa5;font-weight:750;cursor:pointer}button:hover{filter:brightness(1.16)}button.secondary{background:#142237;border-color:#30445d}button.mic{width:54px;min-width:54px;height:52px;font-size:19px}button.primary{width:130px;min-width:110px;height:52px}button.danger{background:#4c1c2a;border-color:#a23a55}.toolrow{display:flex;gap:9px;flex-wrap:wrap}.toolrow button{width:auto}.flash{padding:12px 14px;border-radius:12px;background:#1b2e46;border:1px solid #31516f;margin:10px 0}.project{border:1px solid #31516f;border-radius:14px;overflow:hidden;margin-top:16px;background:#070c14}.project iframe{display:block;width:100%;height:420px;border:0;background:white}.projectbar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 13px;background:#111f30}.projectbar button{width:auto;margin:0}.hint{font-size:12px;color:var(--muted)}.auth{max-width:480px;margin:8vh auto}.auth .panel{padding:24px}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.badge{color:#ff91a4}@media(max-width:760px){header{height:58px;padding:0 14px}.layout{grid-template-columns:1fr}.side{position:static;display:flex;gap:6px;overflow:auto;padding:8px}.side h3{display:none}.side a,.side button{white-space:nowrap;width:auto}.side .sidehide{display:none}main{margin:14px auto;padding:0 10px}.hero{padding:20px}.panel{padding:14px}.chatlog{max-height:50vh}.composer{gap:6px}.composer textarea{min-width:0}.msg{max-width:97%}.project iframe{height:360px}}
</style></head><body>
<header><a class="brand" href="/">RAMN</a><nav class="nav">{% if user %}<span class="muted">{{user}}</span><a href="/owner">OWNER</a><form method="post" action="/logout"><button class="secondary">Logout</button></form>{% else %}<a href="/login">Login</a><a href="/register">Register</a>{% endif %}</nav></header><main>
{% with messages=get_flashed_messages() %}{% for m in messages %}<div class="flash">{{m}}</div>{% endfor %}{% endwith %}
{% if page == 'home' %}
{% if user %}<div class="layout"><aside class="side"><h3>WORKSPACE</h3><a href="#chat">◉ Chat</a><a href="#builder">⌘ Game builder</a><a href="#projects">▣ Projects</a><h3>ACCOUNT</h3><a href="/owner">Owner panel</a><p class="hint sidehide">RAMN AI · Free community model</p></aside><section><div class="hero"><div class="eyebrow">PERSONAL AI WORKSPACE · ONLINE</div><h1>RAMN</h1><p class="muted">Talk, ask, create. Your ideas become playable projects.</p><div class="toolrow"><a href="#chat"><button>Start chatting</button></a><a href="#builder"><button class="secondary">Build a game</button></a></div></div>
<section class="panel" id="chat"><h2>Conversation</h2><p class="muted">Write or use the microphone. RAMN can read replies aloud.</p><div class="chatlog" id="chatlog">{% for m in history %}<div class="msg {{m.role}}"><div class="msghead">{{'YOU' if m.role=='user' else 'RAMN'}}</div>{{m.text}}{% if m.role != 'user' %}<button type="button" class="secondary" onclick="speakText(this)">▶ Speak</button>{% endif %}</div>{% endfor %}</div><form class="composer" method="post" action="/chat"><textarea id="message" name="message" placeholder="Message RAMN…" required maxlength="4000" rows="2"></textarea><button type="button" class="mic secondary" onclick="startVoice()" title="Speak">🎙</button><button class="primary">Send ↗</button></form><p class="hint" id="voiceStatus">Voice input depends on browser support. Audio replies use your device's speech voice.</p></section>
<section class="panel" id="builder"><h2>Game & app builder</h2><p class="muted">Describe what you want. RAMN writes a self-contained HTML project and opens a playable preview here.</p><form method="post" action="/build"><textarea name="idea" placeholder="Example: Make a 2D endless runner with coins, obstacles and a restart button…" maxlength="2000" required rows="3"></textarea><button>⌘ Create project</button></form><p class="hint">HTML, CSS and JavaScript projects run inside a restricted preview. No access to your iPhone files or localhost.</p></section>
{% if latest_project %}<section class="panel" id="projects"><h2>Latest project</h2><p class="muted">{{latest_project.title}}</p><div class="project"><div class="projectbar"><span>LIVE PREVIEW</span><a href="/preview/{{latest_project.id}}" target="_blank"><button type="button" class="secondary">Open full screen ↗</button></a></div><iframe title="RAMN project preview" sandbox="allow-scripts" srcdoc="{{latest_project.html|e}}"></iframe></div></section>{% endif %}</section></div>
{% else %}<div class="auth"><section class="panel"><div class="eyebrow">PERSONAL AI WORKSPACE</div><h1>RAMN</h1><p class="muted">Sign in to chat, talk and build projects.</p><div class="toolrow"><a href="/register"><button>Create account</button></a><a href="/login"><button class="secondary">Sign in</button></a></div></section></div>{% endif %}
{% elif page == 'login' or page == 'register' %}<div class="auth"><section class="panel"><h2>{{'Create account' if page=='register' else 'Sign in'}}</h2><form method="post"><input name="username" placeholder="Username" minlength="3" maxlength="24" pattern="[A-Za-z0-9_]+" required><input name="password" type="password" placeholder="Password" minlength="8" required><button>{{'Register' if page=='register' else 'Login'}}</button></form></section></div>
{% elif page == 'owner_login' %}<div class="auth"><section class="panel"><h2>Owner access</h2><form method="post"><input name="password" type="password" placeholder="Owner password" required><button>Unlock owner panel</button></form></section></div>
{% elif page == 'owner' %}<section class="panel"><div class="eyebrow">RESTRICTED ACCESS</div><h1>OWNER</h1><p>Total accounts: <b>{{users|length}}</b> · Banned: <b>{{banned|length}}</b></p><table><tr><th>Username</th><th>Status</th><th>Action</th></tr>{% for u in users %}<tr><td>{{u.username}}</td><td>{% if u.banned %}<span class="badge">BANNED</span>{% else %}Active{% endif %}</td><td>{% if u.username.lower() != 'ramn' %}<form method="post" action="/owner/toggle"><input type="hidden" name="username" value="{{u.username}}"><button class="{{'danger' if not u.banned else ''}}">{{'Unban' if u.banned else 'Ban user'}}</button></form>{% else %}—{% endif %}</td></tr>{% endfor %}</table><form method="post" action="/owner/logout"><button class="danger">Lock owner panel</button></form></section>{% endif %}
</main><script>
function speakText(btn){if(!('speechSynthesis' in window)){alert('Speech output is not supported in this browser.');return;}let box=btn.parentElement.cloneNode(true);box.querySelectorAll('button').forEach(x=>x.remove());let u=new SpeechSynthesisUtterance(box.innerText.replace(/^RAMN\s*/,''));u.lang=document.documentElement.lang==='de'?'de-DE':'en-US';let voices=speechSynthesis.getVoices();let v=voices.find(x=>/male|markus|daniel|thomas|hans/i.test(x.name))||voices.find(x=>x.lang.toLowerCase().startsWith('de'))||voices.find(x=>x.lang.toLowerCase().startsWith('en'));if(v)u.voice=v;speechSynthesis.cancel();speechSynthesis.speak(u);}
function startVoice(){let R=window.SpeechRecognition||window.webkitSpeechRecognition;let s=document.getElementById('voiceStatus');if(!R){s.textContent='Microphone dictation is not supported here. You can still type and use Speak on replies.';return;}let rec=new R();rec.lang='de-DE';rec.interimResults=false;rec.maxAlternatives=1;s.textContent='Listening…';rec.onresult=e=>{document.getElementById('message').value=e.results[0][0].transcript;s.textContent='Speech recognized. Tap Send.';};rec.onerror=e=>s.textContent='Microphone error: '+e.error;rec.onend=()=>{};rec.start();}
let log=document.getElementById('chatlog');if(log)log.scrollTop=log.scrollHeight;
</script></body></html>
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
        con.execute("""CREATE TABLE IF NOT EXISTS projects(
            id TEXT PRIMARY KEY, username TEXT NOT NULL, title TEXT NOT NULL,
            html TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
    latest = None
    if name == "home" and current_user():
        with db() as con:
            latest = con.execute("SELECT id,title,html FROM projects WHERE username=? ORDER BY created_at DESC LIMIT 1", (current_user(),)).fetchone()
    return render_template_string(PAGE, page=name, user=current_user(),
                                  configured=True, latest_project=latest,
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
    messages = [{"role": "system", "content": "You are RAMN, a friendly, capable AI assistant and coding partner. Reply in the user's language, German by default. Give practical answers and working code when asked. Never claim you executed code unless you did."}]
    for item in history[-10:]:
        role = "assistant" if item.get("role") in ("ramn", "assistant") else "user"
        messages.append({"role": role, "content": item.get("content", item.get("text", ""))})
    messages.append({"role": "user", "content": message})
    body = json.dumps({"model": CHAT_MODEL, "messages": messages, "temperature": 0.7}).encode()
    req = urllib.request.Request(AI_ENDPOINT, data=body,
        headers={"Content-Type": "application/json"})
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

@app.route("/build", methods=["POST"])
@login_required
def build_project():
    idea = request.form.get("idea", "").strip()
    if not idea or len(idea) > 2000:
        flash("Please describe a project in 1–2000 characters.")
        return redirect(url_for("home") + "#builder")
    system = "You are RAMN's web game and app builder. Create one complete, polished, self-contained HTML document. Output ONLY the HTML, no markdown fences or explanations. Use inline CSS and JavaScript. Make it responsive and touch-friendly for iPhone. Do not use external libraries, network calls, eval, dynamic imports, browser storage, cookies, forms that submit, or top-level navigation. Do not request device permissions. Keep all game logic inside the page."
    payload = {"model": CHAT_MODEL, "messages": [{"role":"system","content":system},{"role":"user","content":"Build this project: " + idea}], "temperature":0.35, "max_tokens":6000}
    req = urllib.request.Request(AI_ENDPOINT, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode())
        html = result["choices"][0]["message"]["content"].strip()
        html = re.sub(r"^```(?:html)?\s*|\s*```$", "", html, flags=re.I).strip()
        if "<html" not in html.lower() and "<!doctype" not in html.lower():
            raise ValueError("The model did not return a complete HTML document.")
        if len(html) > 180000:
            raise ValueError("Generated project is too large. Try a smaller idea.")
        pid = secrets.token_urlsafe(9)
        title = idea[:70]
        with db() as con:
            con.execute("INSERT INTO projects(id,username,title,html) VALUES(?,?,?,?)", (pid,current_user(),title,html))
        flash("Project created. Your playable preview is ready below.")
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as error:
        flash("Project generation failed. The free AI may be busy: " + str(error)[:140])
    return redirect(url_for("home") + "#projects")

@app.route("/preview/<project_id>")
@login_required
def preview_project(project_id):
    with db() as con:
        project = con.execute("SELECT html FROM projects WHERE id=? AND username=?", (project_id,current_user())).fetchone()
    if not project:
        abort(404)
    response = app.make_response(project["html"])
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["Content-Security-Policy"] = "sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

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
