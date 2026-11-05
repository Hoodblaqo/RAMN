import os
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#090909">
<title>thugorange7 — sound & signal</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#090909;--ink:#f2f0eb;--muted:#8b8984;--line:#ffffff20;--acid:#d7ff3f;--violet:#9a79ff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Space Grotesk',sans-serif;overflow-x:hidden}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:-2;background:radial-gradient(ellipse at 14% 8%,#5739a82e,transparent 34%),radial-gradient(ellipse at 88% 38%,#c7ff3515,transparent 30%),radial-gradient(ellipse at 50% 100%,#6c42a51c,transparent 38%),#090909}
.noise{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.055;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.wrap{width:min(1080px,calc(100% - 42px));margin:auto}header{height:76px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}.brand{font-weight:700;letter-spacing:-.06em;font-size:19px}.brand span{color:var(--acid)}.mono,.eyebrow,.nav{font:10px 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}.nav{display:flex;gap:26px}.nav a{color:inherit;text-decoration:none}.nav a:hover{color:var(--acid)}
.hero{min-height:440px;display:flex;align-items:center;position:relative;padding:70px 0 58px}.hero:after{content:"07";position:absolute;right:4%;top:34px;font-size:clamp(150px,30vw,330px);font-weight:700;letter-spacing:-.12em;color:#ffffff08;line-height:1;pointer-events:none}.hero-inner{position:relative;z-index:1;max-width:720px}.eyebrow{color:var(--acid);display:flex;align-items:center;gap:10px}.dot{width:7px;height:7px;background:var(--acid);border-radius:50%;box-shadow:0 0 15px var(--acid)}h1{font-size:clamp(54px,10vw,112px);line-height:.88;letter-spacing:-.095em;margin:24px 0 22px;font-weight:700}h1 em{font-style:normal;color:transparent;-webkit-text-stroke:1px #f2f0eb9c}.bio{color:#aaa8a2;max-width:480px;line-height:1.8;font-size:15px}.hero-bottom{display:flex;align-items:center;gap:18px;margin-top:30px}.pill{border:1px solid var(--line);padding:11px 15px;border-radius:30px;font:10px 'DM Mono',monospace;letter-spacing:.12em;color:var(--ink);text-decoration:none}.pill:hover{border-color:var(--acid);color:var(--acid)}
.section{padding:44px 0 70px}.section-head{display:flex;justify-content:space-between;align-items:end;margin-bottom:24px}.section-head h2{font-size:clamp(26px,5vw,42px);letter-spacing:-.07em;margin:8px 0 0}.section-head .mono{color:var(--muted)}
.player-shell{border:1px solid #ffffff25;background:linear-gradient(135deg,#19171fef,#11120fee 55%,#171a10ef);border-radius:20px;padding:24px;box-shadow:0 30px 90px #0008;position:relative;overflow:hidden}.player-shell:before{content:"";position:absolute;width:300px;height:300px;border-radius:50%;background:#a27cff18;filter:blur(70px);right:-100px;top:-150px;pointer-events:none}.player-top{display:flex;justify-content:space-between;align-items:center;position:relative}.live{display:flex;align-items:center;gap:8px;color:var(--acid);font:10px 'DM Mono',monospace;letter-spacing:.13em}.live i{width:6px;height:6px;border-radius:50%;background:var(--acid);box-shadow:0 0 12px var(--acid)}.track-area{display:grid;grid-template-columns:180px 1fr;gap:28px;align-items:center;padding:30px 0 24px;position:relative}.cover{aspect-ratio:1;border-radius:13px;background:linear-gradient(140deg,#2b2144,#161616 55%,#b5e13d);display:grid;place-items:center;overflow:hidden;box-shadow:0 15px 40px #0009;position:relative}.cover:before,.cover:after{content:"";position:absolute;border:1px solid #ffffff45;border-radius:50%;width:78%;aspect-ratio:1}.cover:after{width:54%}.cover-mark{font-size:58px;font-weight:700;letter-spacing:-.12em;z-index:1;text-shadow:0 3px 20px #000}.track-meta .eyebrow{font-size:9px}.track-title{font-size:clamp(28px,5vw,46px);font-weight:700;letter-spacing:-.07em;margin:12px 0 3px}.track-artist{color:var(--muted);font-size:14px}.wave{height:38px;display:flex;align-items:center;gap:4px;margin-top:24px}.wave b{display:block;width:3px;border-radius:5px;background:linear-gradient(to top,var(--violet),var(--acid));height:var(--h);opacity:.8;animation:wave 1s ease-in-out infinite alternate;animation-delay:var(--d)}@keyframes wave{to{transform:scaleY(.35);opacity:.45}}.transport{display:flex;align-items:center;gap:14px;position:relative;padding:16px 0 20px;border-top:1px solid var(--line)}.control{border:0;background:transparent;color:var(--ink);font-size:21px;cursor:pointer;padding:8px}.control:hover{color:var(--acid)}.play{width:48px;height:48px;border-radius:50%;background:var(--acid);color:#101010;font-size:18px;display:grid;place-items:center;border:0;cursor:pointer;box-shadow:0 0 25px #d7ff3f30}.play:hover{transform:scale(1.06)}.now{margin-left:auto;text-align:right}.now strong{display:block;font-size:12px}.now span{font:9px 'DM Mono',monospace;color:var(--muted);letter-spacing:.12em}.embed-wrap{border-radius:12px;overflow:hidden;position:relative;z-index:1}.embed-wrap iframe{display:block;width:100%;height:152px;border:0}.track-list{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:15px}.track-pick{background:#ffffff06;border:1px solid var(--line);border-radius:12px;padding:14px;text-align:left;color:var(--ink);cursor:pointer;transition:.2s;min-width:0}.track-pick:hover,.track-pick.active{border-color:#d7ff3f88;background:#d7ff3f0c}.track-pick .n{font:9px 'DM Mono',monospace;color:var(--acid)}.track-pick strong{display:block;font-size:14px;margin-top:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.track-pick small{display:block;color:var(--muted);margin-top:3px;font-size:11px}
.social{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:24px;border:1px solid var(--line);border-radius:16px;background:#ffffff05}.social strong{display:block;font-size:18px;margin-top:5px}.social a{color:var(--acid);font:10px 'DM Mono',monospace;text-decoration:none;letter-spacing:.1em}.social a:hover{text-decoration:underline}
footer{border-top:1px solid var(--line);padding:22px 0 34px;display:flex;justify-content:space-between;color:#77736d;font:9px 'DM Mono',monospace;letter-spacing:.12em}
@media(max-width:650px){.wrap{width:calc(100% - 30px)}header{height:65px}.nav{gap:14px;font-size:9px}.hero{min-height:380px;padding:55px 0}.hero:after{right:0;top:50px}.track-area{grid-template-columns:112px 1fr;gap:17px;padding:24px 0}.track-title{font-size:28px}.cover-mark{font-size:42px}.player-shell{padding:16px}.track-list{gap:7px}.track-pick{padding:11px 9px}.track-pick strong{font-size:12px}.track-pick small{font-size:10px}.section{padding:35px 0 55px}.social{padding:18px}footer{font-size:8px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;scroll-behavior:auto!important}}
</style>
</head>
<body><div class="noise"></div><div class="wrap">
<header><a class="brand" href="/">thugorange<span>7</span></a><nav class="nav"><a href="#music">MUSIC</a><a href="#social">SOCIAL</a></nav></header>
<main>
<section class="hero"><div class="hero-inner"><div class="eyebrow"><i class="dot"></i> PERSONAL FREQUENCY / 2026</div><h1>NO RULES.<br><em>JUST SOUND.</em></h1><p class="bio">YOUR DESCRIPTION GOES HERE.</p><div class="hero-bottom"><a class="pill" href="#music">TUNE IN ↓</a><span class="mono">HANNOVER · ONLINE</span></div></div></section>
<section class="section" id="music"><div class="section-head"><div><div class="eyebrow">01 / THE ROTATION</div><h2>On repeat.</h2></div><span class="mono">3 TRACKS / SPOTIFY</span></div>
<div class="player-shell">
<div class="player-top"><span class="live"><i></i> NOW SELECTED</span><span class="mono">RAMN AUDIO / 001</span></div>
<div class="track-area"><div class="cover" id="cover"><span class="cover-mark" id="coverMark">07</span></div><div class="track-meta"><div class="eyebrow" id="trackIndex">TRACK 01 — TOP 3</div><div class="track-title" id="trackTitle">Kills</div><div class="track-artist" id="trackArtist">OsamaSon</div><div class="wave" id="wave" aria-hidden="true"></div></div></div>
<div class="transport"><button class="control" id="prev" aria-label="Previous track">↶</button><button class="play" id="play" aria-label="Play selected song">▶</button><button class="control" id="next" aria-label="Next track">↷</button><div class="now"><strong id="miniTitle">Kills</strong><span>OPEN IN SPOTIFY PLAYER ↓</span></div></div>
<div class="embed-wrap"><iframe id="spotify" src="https://open.spotify.com/embed/track/5w10naLxZ0NwN4NzzfFQt?utm_source=generator" title="Spotify player" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div>
<div class="track-list" id="trackList">
<button class="track-pick active" data-index="0"><span class="n">01 / SELECT</span><strong>Kills</strong><small>OsamaSon</small></button>
<button class="track-pick" data-index="1"><span class="n">02 / SELECT</span><strong>My time</strong><small>Kmar</small></button>
<button class="track-pick" data-index="2"><span class="n">03 / SELECT</span><strong>LVL</strong><small>A$AP Rocky</small></button>
</div></div>
</section>
<section class="section" id="social"><div class="section-head"><div><div class="eyebrow">02 / ELSEWHERE</div><h2>Find me.</h2></div><span class="mono">OFF THE GRID</span></div><div class="social"><div><span class="mono">TIKTOK / @THUGORANGE7</span><strong>thugorange7</strong></div><a href="https://www.tiktok.com/@thugorange7" target="_blank" rel="noopener">VIEW PROFILE ↗</a></div></section>
</main>
<footer><span>THUGORANGE7</span><span>PERSONAL PAGE © 2026</span></footer></div>
<script>
const tracks=[
 {title:"Kills",artist:"OsamaSon",id:"5w10naLxZ0NwN4NzzfFQt",mark:"K"},
 {title:"My time",artist:"Kmar",id:"37a5UcsLYA94ArBiJrDBms",mark:"M"},
 {title:"LVL",artist:"A$AP Rocky",id:"787rCZF9i4L1cXGMkdyIk4",mark:"L"}
];
let current=0;
const $=id=>document.getElementById(id);
function render(){
 const t=tracks[current];
 $("trackTitle").textContent=t.title;$("trackArtist").textContent=t.artist;
 $("miniTitle").textContent=t.title;$("trackIndex").textContent="TRACK 0"+(current+1)+" — TOP 3";
 $("coverMark").textContent=t.mark;
 $("spotify").src="https://open.spotify.com/embed/track/"+t.id+"?utm_source=generator";
 document.querySelectorAll(".track-pick").forEach((b,i)=>b.classList.toggle("active",i===current));
}
function select(i){current=(i+tracks.length)%tracks.length;render();}
$("prev").addEventListener("click",()=>select(current-1));
$("next").addEventListener("click",()=>select(current+1));
document.querySelectorAll(".track-pick").forEach(b=>b.addEventListener("click",()=>select(Number(b.dataset.index))));
$("play").addEventListener("click",()=>{$("spotify").scrollIntoView({behavior:"smooth",block:"center"});$("spotify").focus();});
const wave=$("wave");for(let i=0;i<30;i++){const b=document.createElement("b");b.style.setProperty("--h",(8+Math.round(Math.abs(Math.sin(i*1.7))*27))+"px");b.style.setProperty("--d",(i*.045)+"s");wave.appendChild(b);}
</script></body></html>"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return {"app": "thugorange7", "status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
