import os
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#101010">
<meta name="description" content="The personal page of thugorange7.">
<title>thugorange7 — Personal</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{color-scheme:dark;--bg:#101010;--panel:#171717;--line:#303030;--text:#f3f0eb;--muted:#96928c;--accent:#c5ff62}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:Manrope,system-ui,sans-serif}
a{color:inherit;text-decoration:none}.wrap{width:min(960px,calc(100% - 40px));margin:auto}
header{height:76px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}
.logo{font-size:16px;font-weight:800;letter-spacing:-.06em}.logo span{color:var(--accent)}nav{display:flex;gap:25px;font-size:12px;color:var(--muted)}nav a:hover{color:var(--accent)}
main{padding:90px 0 80px}.intro{max-width:720px;animation:appear .7s ease both}.tag{font:10px 'DM Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
h1{font-size:clamp(48px,10vw,104px);line-height:.95;letter-spacing:-.09em;margin:22px 0 20px;font-weight:800}
.desc{font-size:clamp(15px,2vw,18px);line-height:1.9;color:#aaa69f;max-width:590px;margin:0}
.line{height:1px;background:var(--line);margin:72px 0 35px}
.sectiontop{display:flex;align-items:baseline;justify-content:space-between;gap:15px;margin-bottom:20px}
h2{font-size:22px;letter-spacing:-.05em;margin:0}.note{font:10px 'DM Mono',monospace;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
.songs{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.song{border:1px solid var(--line);background:var(--panel);padding:17px;min-height:160px;display:flex;flex-direction:column;justify-content:space-between;transition:transform .2s,border-color .2s}
.song:hover{transform:translateY(-3px);border-color:#666}.songnum{font:11px 'DM Mono',monospace;color:var(--accent)}.songtitle{font-size:16px;font-weight:700;margin-top:28px}.songartist{font-size:12px;color:var(--muted);margin-top:5px}.song a{font-size:11px;color:var(--accent);margin-top:15px}.player{display:block;width:100%;border:0;border-radius:12px;margin-top:16px}
.social{display:flex;align-items:center;justify-content:space-between;gap:18px;border:1px solid var(--line);background:var(--panel);padding:23px;margin-top:35px}.social-left{display:flex;align-items:center;gap:15px}.ttmark{width:43px;height:43px;display:grid;place-items:center;border:1px solid #424242;font-size:20px;font-weight:800}.social small{display:block;color:var(--muted);font:10px 'DM Mono',monospace;letter-spacing:.12em}.social strong{display:block;font-size:17px;margin-top:4px}.visit{font-size:12px;color:var(--accent);white-space:nowrap}.visit:hover{text-decoration:underline}
footer{border-top:1px solid var(--line);padding:20px 0 30px;color:#77736d;font:10px 'DM Mono',monospace;letter-spacing:.1em;display:flex;justify-content:space-between}
@keyframes appear{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:620px){.wrap{width:calc(100% - 30px)}main{padding:65px 0}.line{margin:52px 0 28px}.songs{grid-template-columns:1fr}.song{min-height:120px}.songtitle{margin-top:15px}.social{padding:17px}.note{font-size:9px}nav{gap:14px}footer{font-size:9px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
</head>
<body>
<div class="wrap">
<header><a class="logo" href="/">thugorange<span>7</span></a><nav><a href="#music">MUSIC</a><a href="#social">TIKTOK</a></nav></header>
<main>
<section class="intro">
<div class="tag">A LITTLE ABOUT ME</div>
<h1>Hey, I'm<br>thugorange7.</h1>
<p class="desc">YOUR DESCRIPTION GOES HERE.</p>
</section>
<div class="line"></div>
<section id="music">
<div class="sectiontop"><h2>My top 3 on Spotify</h2><span class="note">Currently listening</span></div>
<div class="songs">
<article class="song"><span class="songnum">01 / TOP TRACK</span><div><div class="songtitle">Kills</div><div class="songartist">OsamaSon</div><iframe class="player" src="https://open.spotify.com/embed/track/5w10naLxZ0NwN4NnzzfFQt?utm_source=generator" width="100%" height="152" frameborder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div></article>
<article class="song"><span class="songnum">02 / TOP TRACK</span><div><div class="songtitle">My time</div><div class="songartist">Kmar</div><a href="https://open.spotify.com/search/My%20time%20Kmar" target="_blank" rel="noopener">FIND & PLAY ON SPOTIFY ↗</a><p class="songartist">Spotify track link not verified yet.</p></div></article>
<article class="song"><span class="songnum">03 / TOP TRACK</span><div><div class="songtitle">LVL</div><div class="songartist">A$AP Rocky</div><iframe class="player" src="https://open.spotify.com/embed/track/787rCZF9i4L1cXGMkdyIk4?utm_source=generator" width="100%" height="152" frameborder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div></article>
</div>
</section>
<section id="social" class="social">
<div class="social-left"><div class="ttmark">♪</div><div><small>FIND ME ON TIKTOK</small><strong>@thugorange7</strong></div></div>
<a class="visit" href="https://www.tiktok.com/@thugorange7" target="_blank" rel="noopener">VIEW PROFILE ↗</a>
</section>
</main>
<footer><span>THUGORANGE7</span><span>PERSONAL PAGE · 2026</span></footer>
</div>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return {"app":"thugorange7","status":"ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
