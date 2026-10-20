import json, pathlib, re
R = pathlib.Path(__file__).parent; S = R/'src'; O = R/'embeds'; O.mkdir(exist_ok=True)
css = (S/'base.css').read_text()
links = json.loads((R/'links.json').read_text()) if (R/'links.json').exists() else {}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..600,0..100,0..1;1,9..144,300..500,0..100,0..1&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">'
REVEAL = "<script>(function(){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll('.rv').forEach(el=>io.observe(el));})();</script>"
def page(name, body, scripts=()):
    pre = '<script>window.LINKS=' + json.dumps(links) + ';</script>' + ''.join('<script>'+(S/x).read_text()+'</script>' for x in scripts)
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Assel Saginayeva · {name}</title>{FONTS}<style>{css}</style>{pre}</head><body>{body}{REVEAL}</body></html>'
    (O/f'{name}.html').write_text(html); return html
page('home', (S/'home.html').read_text(), ['data.js'])
page('weekly', (S/'weekly.html').read_text(), ['data.js'])
import base64
RUN='data:image/jpeg;base64,'+base64.b64encode((R/'assets/run.jpg').read_bytes()).decode()
page('about', (S/'about.html').read_text().replace('{{RUN_IMG}}', RUN))
page('companies', (S/'companies.html').read_text())
page('attestation', (S/'attestation.html').read_text())
page('sources', (S/'sources.html').read_text(), ['sources.js'])
soon = (S/'soon.html').read_text()
def fill(t, **k):
    for a,b in k.items(): t = t.replace('{{'+a+'}}', b)
    return t
li = lambda xs: ''.join(f'<li><span>{a}</span>{b}</li>' for a,b in xs)
page('executive-summary', fill(soon, KICKER='Capstone · 40% of the final exam', TITLE='Executive summary <em>report</em>', TAG='Week 10',
  TEXT='The final report for Bayan Sulu\'s board: recommendation first, every business-case assumption with its verification. 5–7 pages, IEEE. It will grow out of my Assignment 1 business report — deepened, not copied.',
  ITEMS=li([('§1–3','Business context, environment, business model — from A1'),('§4','Human–AI operating model — from Weekly Record 4'),('§5+','Business case and 12-month roadmap')])))
page('video', fill(soon, KICKER='Capstone · 20% of the final exam', TITLE='Video <em>presentation</em>', TAG='Week 10',
  TEXT='10–15 minutes, delivered as if to Bayan Sulu\'s board, with the recommendation in the first minute. It will build on my Assignment 2 video essay about cocoa ordering.',
  ITEMS=li([('A2','Video essay — the human–AI operating model (Week 5)'),('Deck','14–18 slides, roadmap on one slide'),('Live','Individual defence after the video')])))
print(sorted(p.name for p in O.iterdir()))

# ---------- Vercel site: same pages, real navigation, links to /files ----------
V = R/'vercel'; V.mkdir(exist_ok=True)
vlinks = json.loads((R/'links_vercel.json').read_text())
NAV = [('home','Home','/'),('companies','Company Profiles','/companies/'),('about','About Me','/about/'),('weekly','Weekly','/weekly/'),('attestation','Attestation','/attestation/'),('executive-summary','Executive Summary','/executive-summary/'),('video','Video','/video/'),('sources','Sources','/sources/')]
HEADCSS = """<style>
.site{position:sticky;top:0;z-index:20;background:rgba(243,236,225,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.site .in{max-width:1120px;margin:0 auto;padding:0 32px;display:flex;align-items:center;gap:28px}
.site .me{font:500 17px var(--serif);text-decoration:none;white-space:nowrap;padding:16px 0}
.site .me span{font:500 11px var(--mono);letter-spacing:.1em;color:var(--ink-3);margin-left:8px}
.site nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;margin-left:auto}
.site nav::-webkit-scrollbar{display:none}
.site nav a{font-size:13.5px;text-decoration:none;color:var(--ink-2);padding:18px 9px 16px;white-space:nowrap;border-bottom:2px solid transparent}
.site nav a:hover,.site nav a:focus-visible{color:var(--ink);outline:none}
.site nav a[aria-current=page]{color:var(--ink);border-bottom-color:var(--red)}
.foot{max-width:1120px;margin:0 auto;padding:28px 32px 40px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media (max-width:860px){.site .in{flex-direction:column;align-items:flex-start;gap:0;padding:0 16px}.site .me{padding:12px 0 2px}.site nav{margin-left:-9px;max-width:calc(100% + 18px)}.site nav a{padding:10px 9px 12px}.foot{padding:24px 16px 36px}}
</style>"""
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='3' y='5' width='26' height='22' rx='3' fill='%233A2418'/%3E%3Cpath d='M16 5v22M3 16h26' stroke='%2324150D' stroke-width='2'/%3E%3Cpath d='M29 5v11H16z' fill='%23C9A55E'/%3E%3C/svg%3E"
def vpage(key, title, body, scripts=(), extra=''):
    pre = '<script>window.LINKS=' + json.dumps(vlinks) + ';</script>' + ''.join('<script>'+(S/x).read_text()+'</script>' for x in scripts)
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page"' if k==key else '') + f'>{t}</a>' for k,t,h in NAV)
    header = f'<header class="site"><div class="in"><a class="me" href="/">Assel Saginayeva<span>AIB-2602</span></a><nav aria-label="Pages">{nav}</nav></div></header>'
    foot = '<footer class="foot"><span class="label">Assel Saginayeva · AIB-2602 · Astana IT University</span><span class="label">Business Administration · Trimester 1, 2026</span></footer>'
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Assel Saginayeva</title><meta name="description" content="Business Administration e-portfolio of Assel Saginayeva (AIB-2602, Astana IT University): Ferrero vs Bayan Sulu."><link rel="icon" href="{FAV}">{FONTS}<style>{css}</style>{HEADCSS}{pre}</head><body>{header}{body}{foot}{REVEAL}</body></html>'
    d = V if key=='home' else V/key; d.mkdir(exist_ok=True); (d/'index.html').write_text(html)
vpage('home','E-portfolio',(S/'home.html').read_text(),['data.js'])
vpage('weekly','Weekly',(S/'weekly.html').read_text(),['data.js'])
vpage('about','About Me',(S/'about.html').read_text().replace('{{RUN_IMG}}','/img/run.jpg'))
vpage('companies','Company Profiles',(S/'companies.html').read_text())
vpage('attestation','Attestation',(S/'attestation.html').read_text())
vpage('sources','Sources',(S/'sources.html').read_text(),['sources.js'])
vpage('executive-summary','Executive Summary Report',(O/'executive-summary.html').read_text().split('<body>')[1].split('<script>(function(){const io')[0])
vpage('video','Video Presentation',(S/'video.html').read_text())
(V/'img').mkdir(exist_ok=True); (V/'img'/'run.jpg').write_bytes((R/'assets/run.jpg').read_bytes())
(V/'vercel.json').write_text(json.dumps({"cleanUrls":True,"trailingSlash":True}))
print('vercel ok')
