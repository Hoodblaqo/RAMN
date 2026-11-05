import os
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#09090d"><title>thugorange7</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#09090d;--panel:#111117;--panel2:#171720;--text:#f3f0f7;--muted:#85818f;--line:#ffffff16;--lime:#c6ff4d;--purple:#a58bff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse at 80% 0%,#292044 0,transparent 34%),var(--bg);color:var(--text);font-family:Manrope, sans-serif}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.14;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.3'/%3E%3C/svg%3E")}
.wrap{width:min(1050px,calc(100% - 36px));margin:auto}header{height:76px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}
.brand{font-weight:800;letter-spacing:-1.2px;font-size:20px;color:var(--text);text-decoration:none}.brand span{color:var(--lime)}nav{display:flex;gap:25px}nav a{color:var(--muted);font:11px 'DM Mono',monospace;text-decoration:none;text-transform:uppercase;letter-spacing:.1em}nav a:hover{color:var(--lime)}
.hero{padding:90px 0 75px;position:relative}.eyebrow{font:11px 'DM Mono',monospace;color:var(--lime);letter-spacing:.16em;text-transform:uppercase}
h1{font-size:clamp(65px,13vw,140px);line-height:.86;letter-spacing:-.095em;margin:22px 0 24px;font-weight:800}h1 span{color:var(--purple)}
.intro{font-size:16px;color:#b7b2c1;line-height:1.7;max-width:450px}.hero-bottom{display:flex;gap:10px;margin-top:26px;flex-wrap:wrap}.pill{border:1px solid var(--line);border-radius:99px;padding:9px 13px;color:#aaa5b4;font:10px 'DM Mono',monospace;letter-spacing:.08em}
.section{padding:20px 0 70px}.section-head{display:flex;align-items:end;justify-content:space-between;margin-bottom:22px}.section-head h2{font-size:clamp(32px,6vw,52px);letter-spacing:-.07em;margin:8px 0 0}.hint{font:10px 'DM Mono',monospace;color:var(--muted);text-transform:uppercase}
.player{background:linear-gradient(135deg,#191923,#101016 70%);border:1px solid #ffffff18;border-radius:22px;padding:26px;box-shadow:0 24px 80px #0008;position:relative;overflow:hidden}.player:before{content:"";position:absolute;width:340px;height:340px;border-radius:50%;background:#9a75ff12;filter:blur(4px);right:-160px;top:-180px;pointer-events:none}
.player-head{display:flex;justify-content:space-between;align-items:center;position:relative}.live{color:var(--lime);font:10px 'DM Mono',monospace;letter-spacing:.12em}.status{font:10px 'DM Mono',monospace;color:var(--muted)}
.now{display:grid;grid-template-columns:190px 1fr;gap:30px;align-items:center;padding:34px 0 26px;position:relative}
.cover{width:100%;aspect-ratio:1;border-radius:15px;background:linear-gradient(145deg,#9d7cff,#342354 65%,#c6ff4d);display:grid;place-items:center;overflow:hidden;position:relative;box-shadow:0 15px 40px #0008}.cover img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}.cover-mark{font-size:84px;font-weight:800;letter-spacing:-.12em;color:#09090d}
.track-no{font:10px 'DM Mono',monospace;color:var(--lime);letter-spacing:.13em}.track-title{font-size:clamp(30px,5vw,48px);font-weight:800;letter-spacing:-.07em;line-height:1.05;margin-top:9px}.artist{color:var(--muted);margin-top:8px;font-size:15px}
.wave{height:38px;display:flex;align-items:center;gap:4px;margin-top:23px}.wave i{width:3px;height:var(--h);background:linear-gradient(var(--purple),var(--lime));border-radius:5px;opacity:.85}
.timeline{display:flex;gap:12px;align-items:center;color:#8d8997;font:10px 'DM Mono',monospace}.timeline input{flex:1;accent-color:var(--lime);min-width:0}
.controls{display:flex;align-items:center;gap:15px;border-top:1px solid var(--line);padding-top:19px}.controls button{border:0;background:none;color:var(--text);font-size:20px;cursor:pointer}.controls .main-play{width:54px;height:54px;border-radius:50%;background:var(--lime);color:#101016;font-size:22px;box-shadow:0 0 25px #c6ff4d30}.controls .main-play:hover{transform:scale(1.06)}.controls button:hover{color:var(--lime)}.vol{margin-left:auto;display:flex;gap:9px;align-items:center;font:10px 'DM Mono',monospace;color:var(--muted)}.vol input{width:85px;accent-color:var(--lime)}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:19px}.action{border:1px solid #ffffff25;border-radius:10px;background:#ffffff08;color:var(--text);padding:12px 15px;font:10px 'DM Mono',monospace;letter-spacing:.08em;cursor:pointer}.action.primary{background:var(--lime);border-color:var(--lime);color:#101016}.action:hover{border-color:var(--lime)}
.track-list{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:15px}.track{background:#ffffff06;border:1px solid var(--line);border-radius:12px;color:var(--text);padding:15px;text-align:left;cursor:pointer;font-family:inherit}.track.active,.track:hover{border-color:#c6ff4d88;background:#c6ff4d0b}.track small{display:block;color:var(--muted);font:10px 'DM Mono',monospace;margin-bottom:9px}.track strong{font-size:15px}.track em{display:block;font-style:normal;color:var(--muted);font-size:12px;margin-top:4px}
.help{color:var(--muted);font-size:12px;line-height:1.6;margin:13px 2px 0}.file-input{display:none}
.social{margin-top:16px;border:1px solid var(--line);border-radius:15px;padding:21px;display:flex;justify-content:space-between;align-items:center;text-decoration:none;color:var(--text);background:#ffffff05}.social:hover{border-color:var(--purple);background:#a58bff0b}.social small{display:block;font:10px 'DM Mono',monospace;color:var(--muted);margin-bottom:8px}.social strong{font-size:21px;letter-spacing:-.04em}.social span{font:10px 'DM Mono',monospace;color:var(--lime)}
footer{border-top:1px solid var(--line);padding:24px 0 32px;display:flex;justify-content:space-between;color:var(--muted);font:10px 'DM Mono',monospace;letter-spacing:.1em}
@media(max-width:650px){.wrap{width:calc(100% - 28px)}header{height:65px}nav{gap:14px}nav a{font-size:9px}.hero{padding:70px 0 60px}.now{grid-template-columns:112px 1fr;gap:18px;padding:27px 0 22px}.cover-mark{font-size:55px}.player{padding:17px;border-radius:17px}.track-list{grid-template-columns:1fr}.track{display:flex;align-items:center;justify-content:space-between;gap:12px}.track small{margin:0}.track em{margin:0}.section{padding-bottom:52px}.vol input{width:60px}.controls{gap:10px}}
</style></head><body><div class="wrap">
<header><a class="brand" href="/">thugorange<span>7</span></a><nav><a href="#music">music</a><a href="#elsewhere">elsewhere</a></nav></header>
<main><section class="hero"><div class="eyebrow">WELCOME TO MY PAGE</div><h1>thugorange<span>7.</span></h1><p class="intro">My own little corner online. Music I'm into, links, and random stuff. Have a look around.</p><div class="hero-bottom"><span class="pill">PERSONAL PAGE</span><span class="pill">2026</span></div></section>
<section class="section" id="music"><div class="section-head"><div><div class="eyebrow">01 / MUSIC</div><h2>On repeat.</h2></div><span class="hint">THE ROTATION</span></div>
<div class="player"><div class="player-head"><span class="live">● RAMN PLAYER</span><span class="status" id="status">SPOTIFY PLAYER</span></div>
<div class="now"><div class="cover" id="cover"><div class="cover-mark" id="coverMark">7</div></div><div><div class="track-no" id="trackNo">TRACK 01 / 03</div><div class="track-title" id="trackTitle">Kills</div><div class="artist" id="trackArtist">OsamaSon</div><div class="wave" id="wave"></div></div></div>
<div class="controls"><button id="prev" aria-label="Previous">⏮</button><button class="main-play" id="play" aria-label="Play on Spotify">▶</button><button id="next" aria-label="Next">⏭</button></div>
<div style="margin-top:20px;border-radius:14px;overflow:hidden"><iframe id="spotifyFrame" title="Spotify music player" src="https://open.spotify.com/embed/track/5w10naLxZ0NwN4NnzzfFQt?utm_source=generator&theme=0" width="100%" height="152" frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div>
<p class="help" id="help">Play the song right here in the Spotify player. The round play button opens the selected song in Spotify.</p></div>
<div class="track-list"><button class="track active" data-index="0"><small>01 / TRACK</small><strong>Kills</strong><em>OsamaSon</em></button><button class="track" data-index="1"><small>02 / TRACK</small><strong>My time</strong><em>Kmar</em></button><button class="track" data-index="2"><small>03 / TRACK</small><strong>LVL</strong><em>A$AP Rocky</em></button></div>
</section>
<section class="section" id="elsewhere"><div class="section-head"><div><div class="eyebrow">02 / LINKS</div><h2>Elsewhere.</h2></div><span class="hint">FIND ME</span></div><a class="social" href="https://www.tiktok.com/@thugorange7" target="_blank" rel="noopener"><div><small>TIKTOK / @THUGORANGE7</small><strong>thugorange7</strong></div><span>OPEN PROFILE ↗</span></a></section></main>
<footer><span>THUGORANGE7</span><span>2026</span></footer></div>
<script>
const tracks=[
 {title:"Kills",artist:"OsamaSon",id:"5w10naLxZ0NwN4NnzzfFQt"},
 {title:"My time",artist:"Kmar",id:"37a5UcsLYA94ArBiJrDBms"},
 {title:"LVL",artist:"A$AP Rocky",id:"787rCZF9i4L1cXGMkdyIk4"}
];
let current=0;
const el=id=>document.getElementById(id);
function render(){
 const t=tracks[current];
 el("trackTitle").textContent=t.title;
 el("trackArtist").textContent=t.artist;
 el("trackNo").textContent="TRACK "+String(current+1).padStart(2,"0")+" / 03";
 el("spotifyFrame").src="https://open.spotify.com/embed/track/"+t.id+"?utm_source=generator&theme=0";
 document.querySelectorAll(".track").forEach((b,i)=>b.classList.toggle("active",i===current));
 el("status").textContent="SPOTIFY PLAYER";
}
function changeTrack(i){current=(i+tracks.length)%tracks.length;render()}
el("prev").onclick=()=>changeTrack(current-1);
el("next").onclick=()=>changeTrack(current+1);
document.querySelectorAll(".track").forEach(b=>b.onclick=()=>changeTrack(Number(b.dataset.index)));
el("play").onclick=()=>window.open("https://open.spotify.com/track/"+tracks[current].id,"_blank");
render();
</script></body></html>"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return {"app": "thugorange7", "status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
