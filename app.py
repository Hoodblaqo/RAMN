import os
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#e8e3d6">
<title>thugorange7 — personal page</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--paper:#e8e3d6;--ink:#171713;--muted:#77766d;--orange:#f05b35;--line:#171713}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Space Grotesk',sans-serif;overflow-x:hidden}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:5;opacity:.13;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.3'/%3E%3C/svg%3E")}
.wrap{width:min(1060px,calc(100% - 42px));margin:auto}header{height:74px;border-bottom:1px solid #17171355;display:flex;align-items:center;justify-content:space-between}
.brand{font-weight:700;font-size:18px;letter-spacing:-1px;text-decoration:none;color:var(--ink)}.brand span{color:var(--orange)}
nav{display:flex;gap:24px}nav a,.mono{font:10px 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-decoration:none}
nav a:hover{color:var(--orange)}
.hero{padding:95px 0 80px;position:relative;border-bottom:1px solid #17171355}
.kicker{font:11px 'DM Mono',monospace;letter-spacing:.13em;text-transform:uppercase;color:var(--orange)}
h1{font-size:clamp(70px,14vw,155px);line-height:.78;letter-spacing:-.105em;margin:28px 0 25px;font-weight:700}
h1 span{display:block;color:var(--orange);padding-left:12vw}
.intro{max-width:420px;font-size:16px;line-height:1.55;margin:0 0 28px}
.hero-foot{display:flex;align-items:center;gap:15px;flex-wrap:wrap}.tag{border:1px solid var(--ink);border-radius:99px;padding:9px 14px;font:10px 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.1em}
.stamp{position:absolute;right:3%;top:80px;width:112px;height:112px;border:1px solid var(--orange);border-radius:50%;display:grid;place-items:center;color:var(--orange);font:10px 'DM Mono',monospace;text-align:center;transform:rotate(12deg)}
.section{padding:55px 0 75px}.section-head{display:flex;justify-content:space-between;align-items:end;border-bottom:1px solid #17171355;padding-bottom:15px;margin-bottom:24px}
h2{font-size:clamp(34px,6vw,58px);letter-spacing:-.07em;margin:7px 0 0}.section-note{font:10px 'DM Mono',monospace;color:var(--muted);text-transform:uppercase}
.player{background:#171713;color:var(--paper);padding:26px;border-radius:3px;position:relative;overflow:hidden}
.player:after{content:"";position:absolute;width:220px;height:220px;border:1px solid #f05b3544;border-radius:50%;right:-100px;top:-110px;box-shadow:0 0 0 24px #f05b3510,0 0 0 48px #f05b3509;pointer-events:none}
.player-top{display:flex;justify-content:space-between;align-items:center;gap:12px}.status{color:var(--orange);font:10px 'DM Mono',monospace;letter-spacing:.12em}
.now{display:grid;grid-template-columns:130px 1fr;gap:25px;align-items:center;padding:30px 0}
.art{aspect-ratio:1;background:var(--orange);display:grid;place-items:center;color:#171713;font-size:70px;font-weight:700;letter-spacing:-.12em;transform:rotate(-3deg);box-shadow:7px 7px 0 #e8e3d633}
.track-title{font-size:clamp(30px,6vw,48px);font-weight:700;letter-spacing:-.07em;line-height:1}.artist{color:#aaa99e;margin-top:8px;font-size:14px}
.wave{height:28px;display:flex;align-items:center;gap:3px;margin-top:20px}.wave i{display:block;width:3px;background:var(--orange);height:var(--h);opacity:.85}
.timeline{display:flex;align-items:center;gap:12px;color:#aaa99e;font:10px 'DM Mono',monospace}.timeline input{flex:1;accent-color:var(--orange);height:3px}
.controls{display:flex;align-items:center;gap:16px;border-top:1px solid #ffffff24;padding-top:18px}.controls button{background:none;border:0;color:var(--paper);font-size:22px;cursor:pointer}.controls .play{background:var(--orange);color:#171713;width:48px;height:48px;border-radius:50%;font-size:20px}.controls button:hover{color:var(--orange)}.controls .play:hover{color:#171713;transform:scale(1.05)}
.volume{margin-left:auto;display:flex;align-items:center;gap:8px;color:#aaa99e;font:10px 'DM Mono',monospace}.volume input{width:75px;accent-color:var(--orange)}
.track-list{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:12px}.track{background:transparent;border:1px solid #17171355;padding:14px;text-align:left;color:var(--ink);cursor:pointer;font-family:inherit}.track.active,.track:hover{background:var(--orange);border-color:var(--orange)}.track small{display:block;font:10px 'DM Mono',monospace;margin-bottom:8px}.track strong{font-size:15px}.track em{display:block;font-style:normal;font-size:12px;color:#77766d;margin-top:3px}.track.active em,.track:hover em{color:#402116}
.upload{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:17px;border:1px dashed #e8e3d655;padding:14px;color:#aaa99e;font:11px 'DM Mono',monospace}.upload label{color:var(--orange);cursor:pointer}.upload input{display:none}
.social{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:23px;border:1px solid #17171355;margin-top:20px;text-decoration:none;color:var(--ink);transition:.2s}.social:hover{background:var(--orange);border-color:var(--orange)}.social strong{font-size:22px;letter-spacing:-.05em}.social span{font:10px 'DM Mono',monospace;text-transform:uppercase}
footer{border-top:1px solid #17171355;padding:22px 0 32px;display:flex;justify-content:space-between;color:var(--muted);font:10px 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.1em}
@media(max-width:650px){.wrap{width:calc(100% - 30px)}.hero{padding:75px 0 60px}.stamp{width:75px;height:75px;right:0;top:28px;font-size:8px}.intro{max-width:300px}.now{grid-template-columns:92px 1fr;gap:17px;padding:25px 0}.art{font-size:48px}.player{padding:17px}.track-list{grid-template-columns:1fr}.track{display:flex;align-items:center;justify-content:space-between;gap:8px}.track small{margin:0}.track em{margin:0}nav{gap:14px}nav a{font-size:9px}.section{padding:42px 0 55px}.volume{gap:5px}.volume input{width:55px}}
</style>
</head>
<body>
<div class="wrap">
<header><a class="brand" href="/">thugorange<span>7</span></a><nav><a href="#music">music</a><a href="#elsewhere">elsewhere</a></nav></header>
<main>
<section class="hero">
<div class="stamp">MADE BY<br>ME · NOT<br>PERFECT</div>
<div class="kicker">A LITTLE CORNER OF THE INTERNET</div>
<h1>thug<span>orange7.</span></h1>
<p class="intro">Just my page. A few tracks I like, things I'm into, and whatever else I feel like putting here.</p>
<div class="hero-foot"><span class="tag">PERSONAL SITE</span><span class="tag">EST. 2026</span></div>
</section>
<section class="section" id="music">
<div class="section-head"><div><div class="kicker">01 / THE ROTATION</div><h2>On repeat.</h2></div><span class="section-note">3 tracks / RAMN audio</span></div>
<div class="player">
<div class="player-top"><span class="status">● LOCAL PLAYER</span><span class="mono" id="playerState" style="color:#aaa99e">READY / 001</span></div>
<div class="now"><div class="art" id="coverMark">K</div><div><div class="mono" id="trackIndex" style="color:#f05b35">TRACK 01</div><div class="track-title" id="trackTitle">Kills</div><div class="artist" id="trackArtist">OsamaSon</div><div class="wave" id="wave"></div></div></div>
<div class="timeline"><span id="currentTime">0:00</span><input id="seek" type="range" min="0" max="100" value="0"><span id="duration">0:00</span></div>
<div class="controls"><button id="prev" aria-label="Previous track">⏮</button><button class="play" id="play" aria-label="Play">▶</button><button id="next" aria-label="Next track">⏭</button><div class="volume">VOL <input id="volume" type="range" min="0" max="1" step=".01" value=".8"></div></div>
<audio id="audio" preload="metadata"></audio>
<div class="track-list" id="trackList">
<button class="track active" data-index="0"><small>01 / PICK</small><strong>Kills</strong><em>OsamaSon</em></button>
<button class="track" data-index="1"><small>02 / PICK</small><strong>My time</strong><em>Kmar</em></button>
<button class="track" data-index="2"><small>03 / PICK</small><strong>LVL</strong><em>A$AP Rocky</em></button>
</div>
<div class="upload"><span id="fileLabel">Choose an audio file to play it here.</span><label for="audioFile">＋ LOAD AUDIO</label><input id="audioFile" type="file" accept="audio/*"></div>
</div>
</section>
<section class="section" id="elsewhere" style="padding-top:0">
<div class="section-head"><div><div class="kicker">02 / ELSEWHERE</div><h2>Find me.</h2></div><span class="section-note">the internet</span></div>
<a class="social" href="https://www.tiktok.com/@thugorange7" target="_blank" rel="noopener"><div><span>TIKTOK / @THUGORANGE7</span><strong>thugorange7</strong></div><span>VIEW PROFILE ↗</span></a>
</section>
</main>
<footer><span>THUGORANGE7</span><span>MADE BY ME · 2026</span></footer>
</div>
<script>
const tracks=[{title:"Kills",artist:"OsamaSon",mark:"K"},{title:"My time",artist:"Kmar",mark:"M"},{title:"LVL",artist:"A$AP Rocky",mark:"L"}];
let current=0,objectUrl=null;
const $=id=>document.getElementById(id),audio=$("audio");
function fmt(v){if(!Number.isFinite(v))return"0:00";return Math.floor(v/60)+":"+String(Math.floor(v%60)).padStart(2,"0")}
function render(){const t=tracks[current];$("trackTitle").textContent=t.title;$("trackArtist").textContent=t.artist;$("coverMark").textContent=t.mark;$("trackIndex").textContent="TRACK "+String(current+1).padStart(2,"0");$("playerState").textContent=audio.src?"FILE LOADED":"READY / "+String(current+1).padStart(3,"0");document.querySelectorAll(".track").forEach((b,i)=>b.classList.toggle("active",i===current));$("seek").value=0;$("currentTime").textContent="0:00";$("duration").textContent=fmt(audio.duration)}
function select(i){current=(i+tracks.length)%tracks.length;audio.pause();audio.removeAttribute("src");audio.load();if(objectUrl){URL.revokeObjectURL(objectUrl);objectUrl=null}$("play").textContent="▶";render()}
$("prev").onclick=()=>select(current-1);$("next").onclick=()=>select(current+1);document.querySelectorAll(".track").forEach(b=>b.onclick=()=>select(Number(b.dataset.index)));
$("play").onclick=async()=>{if(!audio.src){$("audioFile").click();return}if(audio.paused){try{await audio.play()}catch(e){$("playerState").textContent="TAP TO RETRY"}}else audio.pause()};
audio.onplay=()=>{$("play").textContent="Ⅱ";$("playerState").textContent="PLAYING"};audio.onpause=()=>{$("play").textContent="▶";if(!audio.ended)$("playerState").textContent="PAUSED"};audio.onended=()=>select(current+1);
audio.onloadedmetadata=()=>{$("duration").textContent=fmt(audio.duration);$("seek").max=audio.duration||100};audio.ontimeupdate=()=>{$("currentTime").textContent=fmt(audio.currentTime);$("seek").value=audio.currentTime};
$("seek").oninput=e=>{if(audio.src)audio.currentTime=Number(e.target.value)};$("volume").oninput=e=>audio.volume=Number(e.target.value);audio.volume=.8;
$("audioFile").onchange=e=>{const f=e.target.files[0];if(!f)return;if(objectUrl)URL.revokeObjectURL(objectUrl);objectUrl=URL.createObjectURL(f);audio.src=objectUrl;$("fileLabel").textContent=f.name;$("playerState").textContent="FILE LOADED";audio.play().catch(()=>{$("playerState").textContent="READY TO PLAY"});$("play").textContent="Ⅱ"};
for(let i=0;i<34;i++){const bar=document.createElement("i");bar.style.setProperty("--h",(5+Math.abs(Math.sin(i*1.63))*22)+"px");$("wave").appendChild(bar)}
render();
</script>
</body></html>"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return {"app": "thugorange7", "status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
