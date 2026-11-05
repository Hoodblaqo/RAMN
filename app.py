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
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#050713"><meta name="description" content="A little universe on the internet. Music, TikTok and more.">
<title>RAMN — My Universe</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{color-scheme:dark;--bg:#050713;--panel:rgba(13,19,43,.72);--line:rgba(156,174,255,.17);--text:#f3f5ff;--muted:#a1a9c7;--cyan:#71e7ff;--violet:#a88cff;--pink:#ff86c8;--green:#7fffd0}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:'Space Grotesk',system-ui,sans-serif;overflow-x:hidden}
#stars{position:fixed;inset:0;width:100%;height:100%;z-index:-3;pointer-events:none}.nebula{position:fixed;inset:-20%;z-index:-2;pointer-events:none;background:radial-gradient(ellipse at 18% 22%,rgba(84,67,190,.25),transparent 35%),radial-gradient(ellipse at 82% 42%,rgba(0,172,210,.15),transparent 33%),radial-gradient(ellipse at 50% 90%,rgba(173,64,157,.14),transparent 38%);filter:blur(26px);animation:nebula 22s ease-in-out infinite alternate}
@keyframes nebula{to{transform:translate3d(3%,-2%,0) scale(1.08)}}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}@keyframes pulse{0%,100%{opacity:.5;transform:scale(.96)}50%{opacity:1;transform:scale(1.04)}}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:translateY(0)}}@keyframes shimmer{to{background-position:220% center}}
a{color:inherit;text-decoration:none}button,input,textarea{font:inherit}.shell{width:min(1120px,calc(100% - 34px));margin:auto}.topbar{position:sticky;top:0;z-index:20;background:rgba(5,7,19,.72);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}.topinner{height:70px;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{font-weight:700;letter-spacing:.2em;font-size:18px}.brand span{color:var(--cyan)}.nav{display:flex;align-items:center;gap:22px;color:var(--muted);font-size:13px}.nav a:hover{color:white}.nav .pill{border:1px solid rgba(113,231,255,.4);border-radius:999px;padding:9px 14px;color:var(--cyan)}
main{padding-bottom:90px}.hero{min-height:630px;display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:40px;padding:70px 0 55px}.eyebrow,.mono{font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.18em;font-size:10px;color:var(--cyan)}.live{display:inline-flex;align-items:center;gap:9px;padding:9px 13px;border:1px solid var(--line);border-radius:999px;background:rgba(12,19,42,.55);color:#c6d1ef;font:10px 'DM Mono',monospace;letter-spacing:.12em}.live i{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 14px var(--green);animation:pulse 1.8s infinite}.hero h1{font-size:clamp(48px,8vw,92px);line-height:.94;letter-spacing:-.075em;margin:24px 0 18px}.gradient{background:linear-gradient(100deg,#fff 5%,#8ceaff 42%,#c5a4ff 72%,#ff9bd9);background-size:220% auto;color:transparent;background-clip:text;-webkit-background-clip:text;animation:shimmer 8s linear infinite}.hero p{max-width:500px;color:var(--muted);font-size:16px;line-height:1.8}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:13px 18px;border-radius:12px;border:1px solid rgba(113,231,255,.38);background:linear-gradient(135deg,rgba(83,197,235,.2),rgba(154,120,255,.2));color:white;font-weight:600;font-size:13px;transition:.25s}.btn:hover{transform:translateY(-3px);box-shadow:0 10px 36px rgba(83,197,235,.17)}.btn.ghost{border-color:var(--line);background:rgba(13,19,43,.55);color:#cbd2ec}
.planet-stage{height:440px;position:relative;display:grid;place-items:center;animation:float 7s ease-in-out infinite}.planet{width:min(290px,65vw);aspect-ratio:1;border-radius:50%;position:relative;background:radial-gradient(circle at 32% 27%,#d8d4ff 0,#9d8bea 10%,#5b4a9f 27%,#24285e 54%,#10172e 74%);box-shadow:inset -30px -24px 55px #030512,0 0 55px rgba(134,121,255,.35),0 0 130px rgba(83,177,255,.18);overflow:hidden}.planet:before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(165deg,transparent 0 18px,rgba(198,180,255,.14) 19px 22px,transparent 24px 39px);border-radius:50%;mix-blend-mode:screen}.planet:after{content:"";position:absolute;inset:12% 0 0 12%;border-radius:50%;background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.28),transparent 38%)}.orbit{position:absolute;width:390px;height:145px;border:1px solid rgba(134,210,255,.48);border-radius:50%;transform:rotate(-24deg);box-shadow:0 0 20px rgba(113,231,255,.12);animation:orbit 24s linear infinite}.orbit:after{content:"";position:absolute;right:10%;top:5%;width:13px;height:13px;border-radius:50%;background:var(--cyan);box-shadow:0 0 18px var(--cyan)}.moon{position:absolute;width:55px;height:55px;border-radius:50%;right:9%;top:16%;background:radial-gradient(circle at 30% 25%,#fff,#c5d4ed 28%,#596b91 70%);box-shadow:0 0 35px rgba(192,213,255,.4)}.planet-label{position:absolute;bottom:25px;right:2%;font:10px 'DM Mono',monospace;color:#aab7dc;letter-spacing:.2em}
.section{padding:52px 0 22px;scroll-margin-top:90px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:22px}.section-head h2{font-size:clamp(27px,4vw,42px);letter-spacing:-.05em;margin:9px 0 0}.section-head p{color:var(--muted);font-size:12px;margin:0}.glass{background:linear-gradient(145deg,rgba(18,26,55,.8),rgba(9,14,32,.7));border:1px solid var(--line);border-radius:22px;box-shadow:0 20px 70px rgba(0,0,0,.18);backdrop-filter:blur(14px)}
.music-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.track{padding:15px;transition:.25s;overflow:hidden;position:relative}.track:hover{transform:translateY(-5px);border-color:rgba(113,231,255,.42)}.cover{aspect-ratio:1;border-radius:15px;display:grid;place-items:center;margin-bottom:15px;position:relative;overflow:hidden;background:radial-gradient(circle at 28% 25%,#b5a2ff,transparent 28%),linear-gradient(135deg,#1d4671,#21163f 60%,#6a286c)}.cover:before,.cover:after{content:"";position:absolute;border:1px solid rgba(255,255,255,.26);border-radius:50%;width:75%;aspect-ratio:1;transform:rotate(-25deg)}.cover:after{width:110%;transform:rotate(35deg)}.cover b{font-size:34px;letter-spacing:-.1em;text-shadow:0 4px 30px #0008}.track:nth-child(2) .cover{background:radial-gradient(circle at 70% 20%,#ffc2dc,transparent 28%),linear-gradient(135deg,#6b315f,#251a50 55%,#123d58)}.track:nth-child(3) .cover{background:radial-gradient(circle at 30% 25%,#8affec,transparent 28%),linear-gradient(135deg,#174b58,#151b45 60%,#52377c)}.track .num{font:10px 'DM Mono';color:var(--cyan);letter-spacing:.16em}.track h3{margin:7px 0 4px;font-size:17px}.track p{margin:0;color:var(--muted);font-size:12px}.track .listen{display:inline-block;margin-top:15px;color:var(--cyan);font-size:12px}
.social-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.social-card{padding:23px;min-height:210px;position:relative;overflow:hidden}.social-card h3{font-size:22px;margin:12px 0 6px}.social-card p{color:var(--muted);font-size:13px;line-height:1.7;max-width:390px}.social-icon{width:47px;height:47px;border-radius:15px;display:grid;place-items:center;background:rgba(113,231,255,.12);border:1px solid rgba(113,231,255,.25);font-size:22px}.profile{display:flex;align-items:center;gap:14px}.avatar{width:64px;height:64px;border-radius:50%;display:grid;place-items:center;font-size:23px;font-weight:700;background:linear-gradient(135deg,#7ae8ff,#a78cff 55%,#ff8bc8);color:#101126;box-shadow:0 0 28px rgba(145,130,255,.3)}.handle{font:11px 'DM Mono';color:var(--cyan)}.social-card .btn{margin-top:12px}.stats{display:flex;gap:20px;margin-top:18px}.stats b{display:block;font-size:18px}.stats span{font-size:10px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
.footer{border-top:1px solid var(--line);padding:25px 0;color:#76809f;font:10px 'DM Mono';letter-spacing:.13em;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.flash{padding:12px 15px;margin:12px 0;border:1px solid var(--line);border-radius:12px;background:#151d39;color:#dce5ff}.workspace{margin-top:44px;padding:24px}.workspace h2{margin-top:0}.chatlog{display:flex;flex-direction:column;gap:12px;max-height:48vh;overflow:auto}.msg{max-width:92%;padding:13px 15px;border:1px solid var(--line);border-radius:14px;background:#10182f;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55}.msg.user{margin-left:auto;background:#192a4a}.msghead{font:10px 'DM Mono';color:var(--cyan);margin-bottom:6px}.composer{display:flex;gap:8px;align-items:end;margin-top:14px}.composer textarea,.field{width:100%;padding:13px;border-radius:12px;border:1px solid var(--line);background:#080d1c;color:white}.composer textarea{min-height:54px;max-height:140px}.composer button,.auth button{cursor:pointer}.toolrow{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.hint{font-size:12px;color:var(--muted);line-height:1.6}.project{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:16px}.project iframe{width:100%;height:380px;border:0;background:white}.projectbar{padding:10px 13px;display:flex;justify-content:space-between;align-items:center;background:#111a32}.auth{max-width:470px;margin:80px auto}.auth .glass{padding:25px}.auth input{margin:8px 0}.auth button{margin-top:10px}.owner-table{width:100%;border-collapse:collapse}.owner-table td,.owner-table th{text-align:left;padding:10px;border-bottom:1px solid var(--line)}
@media(max-width:760px){.nav{gap:12px;font-size:11px}.nav a:nth-child(2){display:none}.hero{grid-template-columns:1fr;padding:55px 0 20px;min-height:auto}.hero-copy{text-align:center}.hero p{margin-left:auto;margin-right:auto}.hero-actions{justify-content:center}.planet-stage{height:330px}.planet{width:220px}.orbit{width:300px;height:110px}.moon{width:40px;height:40px}.music-grid{grid-template-columns:1fr 1fr}.track:last-child{grid-column:1/-1}.social-grid{grid-template-columns:1fr}.section{padding-top:42px}.section-head{align-items:start;flex-direction:column}.workspace{padding:16px}.composer{flex-wrap:wrap}.composer textarea{flex-basis:100%}}
@media(max-width:420px){.music-grid{grid-template-columns:1fr}.track:last-child{grid-column:auto}.nav a:first-child{display:none}.brand{font-size:15px}.hero h1{font-size:52px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition:none!important}}
</style></head>
<body><canvas id="stars"></canvas><div class="nebula"></div>
<header class="topbar"><div class="shell topinner"><a class="brand" href="/">R<span>A</span>MN<span>.</span></a><nav class="nav"><a href="#music">Music</a><a href="#socials">Socials</a><a href="#about">About</a>{% if user %}<a class="pill" href="#workspace">AI workspace</a><a href="/owner">Owner</a><form method="post" action="/logout"><button class="pill" type="submit">Log out</button></form>{% else %}<a class="pill" href="/login">Sign in</a>{% endif %}</nav></div></header>
<main class="shell">
{% with messages=get_flashed_messages() %}{% for m in messages %}<div class="flash">{{m}}</div>{% endfor %}{% endwith %}
{% if page == 'home' %}
<section class="hero" id="about"><div class="hero-copy"><span class="live"><i></i> TRANSMISSION ONLINE · EARTH ORBIT</span><div class="eyebrow" style="margin-top:28px">WELCOME TO MY UNIVERSE</div><h1>Lost in<br><span class="gradient">my own</span><br>orbit.</h1><p>Music on repeat, moments in motion, and a little corner of the internet that is entirely mine. Explore the signal.</p><div class="hero-actions"><a class="btn" href="#music">Explore my music ↗</a><a class="btn ghost" href="#socials">Find me online</a></div></div><div class="planet-stage"><div class="orbit"></div><div class="planet"></div><div class="moon"></div><div class="planet-label">SECTOR 01 · RAMN SYSTEM</div></div></section>
<section class="section" id="music"><div class="section-head"><div><div class="eyebrow">THE SOUNDTRACK</div><h2>Top 3 on Spotify<span style="color:var(--cyan)">.</span></h2></div><p>Three tracks. One universe.</p></div><div class="music-grid">
<div class="track glass"><div class="cover"><b>01</b></div><div class="num">TRACK 01 / SPOTIFY</div><h3>Your first song</h3><p>Song title · Artist</p><span class="listen">Spotify link coming soon ↗</span></div>
<div class="track glass"><div class="cover"><b>02</b></div><div class="num">TRACK 02 / SPOTIFY</div><h3>Your second song</h3><p>Song title · Artist</p><span class="listen">Spotify link coming soon ↗</span></div>
<div class="track glass"><div class="cover"><b>03</b></div><div class="num">TRACK 03 / SPOTIFY</div><h3>Your third song</h3><p>Song title · Artist</p><span class="listen">Spotify link coming soon ↗</span></div>
</div></section>
<section class="section" id="socials"><div class="section-head"><div><div class="eyebrow">FIND THE SIGNAL</div><h2>Elsewhere online<span style="color:var(--cyan)">.</span></h2></div><p>Catch me outside this orbit.</p></div><div class="social-grid">
<div class="social-card glass"><div class="social-icon">♪</div><h3>Spotify</h3><p>Listen to my tracks and explore the music that belongs in this universe.</p><a class="btn ghost" href="https://open.spotify.com/" target="_blank" rel="noopener">Open Spotify ↗</a></div>
<div class="social-card glass"><div class="profile"><div class="avatar">@</div><div><div class="eyebrow">TIKTOK PROFILE</div><h3 style="margin:5px 0">@yourusername</h3><div class="handle">PROFILE LINK NOT SET</div></div></div><p>Short clips, edits and whatever else is happening. My TikTok profile lives here.</p><a class="btn" href="https://www.tiktok.com/" target="_blank" rel="noopener">Open TikTok ↗</a></div>
</div></section>
{% if user %}<section class="section glass workspace" id="workspace"><div class="eyebrow">RAMN AI · ONLINE</div><h2>Talk to RAMN</h2><p class="hint">Chat, use voice input, or build a mini game and play it below.</p><div class="chatlog" id="chatlog">{% for m in history %}<div class="msg {{m.role}}"><div class="msghead">{{'YOU' if m.role=='user' else 'RAMN'}}</div>{{m.text}}{% if m.role!='user' %}<button type="button" class="btn ghost" onclick="speakText(this)">▶ Speak</button>{% endif %}</div>{% endfor %}</div><form class="composer" method="post" action="/chat"><textarea id="message" name="message" placeholder="Message RAMN..." required maxlength="4000"></textarea><button type="button" class="btn ghost" onclick="startVoice()">🎙</button><button class="btn">Send ↗</button></form><p class="hint" id="voiceStatus">Voice input depends on browser support. Replies can be read aloud.</p>
<div style="border-top:1px solid var(--line);margin-top:24px;padding-top:20px" id="builder"><h2>Build a mini game</h2><form method="post" action="/build"><textarea class="field" name="idea" rows="3" placeholder="Describe your game idea..." required maxlength="2000"></textarea><button class="btn" style="margin-top:10px">Create project ↗</button></form></div>{% if latest_project %}<div class="project"><div class="projectbar"><span>{{latest_project.title}}</span><a class="btn ghost" href="/preview/{{latest_project.id}}" target="_blank">Open preview ↗</a></div><iframe title="RAMN game preview" sandbox="allow-scripts" srcdoc="{{latest_project.html|e}}"></iframe></div>{% endif %}</section>{% else %}<section class="section glass workspace" style="text-align:center"><div class="eyebrow">RAMN AI WORKSPACE</div><h2>Want to build something?</h2><p class="hint">Sign in to chat with RAMN and generate playable mini games.</p><a class="btn" href="/login">Sign in ↗</a><a class="btn ghost" href="/register">Create account</a></section>{% endif %}
{% elif page == 'login' or page == 'register' %}<div class="auth"><div class="glass"><div class="eyebrow">RAMN ACCOUNT</div><h1>{{'Create account' if page=='register' else 'Welcome back'}}</h1><form method="post"><input class="field" name="username" placeholder="Username" minlength="3" maxlength="24" required><input class="field" name="password" type="password" placeholder="Password" minlength="8" required><button class="btn">{{'Register' if page=='register' else 'Sign in'}} ↗</button></form><p class="hint"><a href="{{'/login' if page=='register' else '/register'}}">{{'Already have an account? Sign in' if page=='register' else 'Create an account'}}</a></p></div></div>
{% elif page == 'owner_login' %}<div class="auth"><div class="glass"><div class="eyebrow">RESTRICTED ACCESS</div><h1>Owner login</h1><form method="post"><input class="field" name="password" type="password" placeholder="Owner password" required><button class="btn">Unlock ↗</button></form></div></div>
{% elif page == 'owner' %}<section class="section glass workspace"><div class="eyebrow">RESTRICTED ACCESS</div><h1>OWNER PANEL</h1><p>Accounts: {{users|length}} · Banned: {{banned|length}}</p><table class="owner-table"><tr><th>Username</th><th>Status</th><th>Action</th></tr>{% for u in users %}<tr><td>{{u.username}}</td><td>{{'BANNED' if u.banned else 'Active'}}</td><td>{% if u.username.lower() != 'ramn' %}<form method="post" action="/owner/toggle"><input type="hidden" name="username" value="{{u.username}}"><button class="btn ghost">{{'Unban' if u.banned else 'Ban user'}}</button></form>{% endif %}</td></tr>{% endfor %}</table><form method="post" action="/owner/logout"><button class="btn ghost">Lock owner panel</button></form></section>{% endif %}
</main><footer class="shell footer"><span>RAMN SYSTEMS · PERSONAL UNIVERSE</span><span>MADE OF STARDUST · EST. 2026</span></footer>
<script>
(()=>{const c=document.getElementById('stars'),ctx=c.getContext('2d');let w,h,stars=[];function resize(){w=c.width=innerWidth*devicePixelRatio;h=c.height=innerHeight*devicePixelRatio;stars=Array.from({length:Math.min(220,Math.floor(innerWidth/4))},()=>({x:Math.random()*w,y:Math.random()*h,r:Math.random()*1.5+.25,a:Math.random()*.7+.2,s:Math.random()*.008+.002}));}function draw(){ctx.clearRect(0,0,w,h);for(const p of stars){p.a+=p.s;if(p.a>.95||p.a<.15)p.s*=-1;ctx.globalAlpha=p.a;ctx.fillStyle='#d8e9ff';ctx.beginPath();ctx.arc(p.x,p.y,p.r*devicePixelRatio,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1;requestAnimationFrame(draw)}addEventListener('resize',resize);resize();draw()})();
function speakText(btn){if(!('speechSynthesis'in window))return;let box=btn.parentElement.cloneNode(true);box.querySelectorAll('button').forEach(x=>x.remove());let u=new SpeechSynthesisUtterance(box.innerText.replace(/^RAMN\s*/,''));u.lang='en-US';let voices=speechSynthesis.getVoices();let v=voices.find(x=>/male|daniel|markus|thomas/i.test(x.name))||voices.find(x=>x.lang.startsWith('en'));if(v)u.voice=v;speechSynthesis.cancel();speechSynthesis.speak(u)}
function startVoice(){let R=window.SpeechRecognition||window.webkitSpeechRecognition,s=document.getElementById('voiceStatus');if(!R){s.textContent='Voice dictation is not supported here. Use your iPhone keyboard dictation instead.';return}let r=new R();r.lang='en-US';r.interimResults=false;s.textContent='Listening…';r.onresult=e=>{document.getElementById('message').value=e.results[0][0].transcript;s.textContent='Speech recognized. Tap Send.'};r.onerror=e=>s.textContent='Microphone: '+e.error;r.start()}
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
