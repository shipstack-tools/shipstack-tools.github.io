#!/usr/bin/env python3
"""Generate the full ShipStack static site from tools.json."""
import json, html, os, re, shutil
ROOT=os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
SITE="https://shipstack.tools"; e=html.escape
d=json.load(open("tools.json")); UPD=d["updated"]
SLUG={"AI coding agents & IDEs":"best-ai-coding-agents","App builders (prompt-to-app)":"best-ai-app-builders","Deploy & hosting":"best-deploy-hosting-for-ai-apps","Backend, database & auth":"best-backend-database-auth","Design-to-code":"best-design-to-code-tools","AI APIs & models":"best-ai-apis-models","Agent frameworks":"best-agent-frameworks","Testing & debugging":"best-ai-testing-debugging-tools"}
USE={"AI coding agents & IDEs":"writing and refactoring code with AI","App builders (prompt-to-app)":"turning a prompt into a working app","Deploy & hosting":"deploying AI-built apps","Backend, database & auth":"adding a database and login to your app","Design-to-code":"turning designs into code","AI APIs & models":"adding AI features via an API","Agent frameworks":"building your own AI agents","Testing & debugging":"testing and debugging AI-written code"}
def tslug(n): return re.sub(r"[^a-z0-9]+","-",n.lower()).strip("-")
cats=d["categories"]
for c in cats:
  c["slug"]=SLUG[c["name"]]
  for t in c["tools"]: t["slug"]=tslug(t["name"]); t["category"]=c["name"]
alltools=[t for c in cats for t in c["tools"]]
GENERATED=["index.html","advertise","tools","api","data","llms.txt","llms-full.txt","sitemap.xml","robots.txt"]+list(SLUG.values())
KEEP={os.path.join("api","subscribe.js")}  # serverless functions preserved across builds
for g in GENERATED:
  p=os.path.join(ROOT,g)
  if g=="api" and os.path.isdir(p):
    for f in os.listdir(p):
      fp=os.path.join(p,f)
      if os.path.join("api",f) in KEEP: continue
      shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
  elif os.path.isdir(p): shutil.rmtree(p)
  elif os.path.exists(p): os.remove(p)
def ld(o): return '<script type="application/ld+json">'+json.dumps(o).replace("</","<\\/")+'</script>'
def page(path,title,desc,body,jsonld=()):
  url=SITE+path
  h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ShipStack"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@shipstacktools"><meta name="twitter:creator" content="@shipstacktools"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE}/og.png">
<link rel="alternate" type="application/json" href="/api/tools.json"><link rel="stylesheet" href="/style.css">{"".join(ld(j) for j in jsonld)}</head><body>
<header><a class="logo" href="/">⚡ ShipStack</a><nav><a href="/#tools">Tools</a><a href="/#new">New this week</a><a href="/advertise/">Advertise</a><a href="/#signup">Newsletter</a></nav></header>
{body}
<footer><p>{" · ".join(f'<a href="/{c["slug"]}/">{e(c["name"])}</a>' for c in cats)}</p><p>© 2026 shipstack.tools · Rankings are editorial opinions · Data verified {UPD} · <a href="/api/tools.json">API</a> · <a href="/llms.txt">llms.txt</a> · <a href="/advertise/">Advertise</a> · <a href="https://x.com/shipstacktools" rel="me">Follow @shipstacktools on X</a></p><p class="small">Some links may become affiliate links in future; this will be disclosed on each link.</p></footer><script src="/app.js"></script></body></html>'''
  out=os.path.join(ROOT,path.lstrip("/"),"index.html") if path.endswith("/") else os.path.join(ROOT,path.lstrip("/"))
  os.makedirs(os.path.dirname(out),exist_ok=True); open(out,"w").write(h)
def link(t): return t["affiliate_url"] or t["url"]
def rel(t): return "sponsored noopener" if t["affiliate_url"] else "noopener"
def card(t):
  return (f'<article class="card" data-cat="{e(t["category"])}" data-text="{e((t["name"]+" "+t["description"]+" "+t["best_for"]).lower())}"><div class="rank">#{t["rank"]}</div>'
   f'<h3><a href="/tools/{t["slug"]}/">{e(t["name"])}</a></h3><p>{e(t["description"])}</p>'+(f'<p class="price">💲 {e(t["pricing"])}</p>' if t.get("pricing") else "")+
   f'<p class="meta"><b>Best for:</b> {e(t["best_for"])}</p><p class="why">{e(t["rank_reason"])}</p><a class="tag" href="/{SLUG[t["category"]]}/">{e(t["category"])}</a> <a class="out" href="{e(link(t))}" target="_blank" rel="{rel(t)}">Visit ↗</a></article>')
def featured():
  if d["featured"]:
    return '<section class="featured"><div class="label">Featured · Sponsored</div>'+"".join(f'<a href="{e(f["url"])}" rel="sponsored noopener" target="_blank">{e(f["name"])}</a> — {e(f.get("tagline",""))}' for f in d["featured"])+'</section>'
  return '<section class="featured empty"><div class="label">Featured · Sponsored</div><p>This sponsor slot is open. Sponsored placements are always labeled and never affect rankings. <a href="https://buy.stripe.com/5kQ9AU0r44JD4NFbVb38400" rel="noopener">Feature your tool here — $99 / 30 days →</a></p></section>'
def answer(c):
  ts=c["tools"]; a,b=ts[0],ts[1]
  return (f'<div class="answer"><h2>Quick answer: what is the best tool for {e(USE[c["name"]])}?</h2><p><b>{e(a["name"])}</b> is our top pick for {e(USE[c["name"]])} — {e(a["rank_reason"][0].lower()+a["rank_reason"][1:])}. '
          f'Runner-up: <b>{e(b["name"])}</b> (best for: {e(b["best_for"])}). '+" ".join(f'Best for {e(t["best_for"])}: {e(t["name"])}.' for t in ts[2:])+'</p></div>')
def faq(c):
  ts=c["tools"]
  q=[(f'What is the best {c["name"]} tool in 2026?',f'{ts[0]["name"]} ranks #1 on ShipStack: {ts[0]["rank_reason"]}.'),
     (f'Which {c["name"]} tools have a free tier?',(", ".join(t["name"] for t in ts if t.get("pricing","").lower().startswith(("free","hobby","developer","community","claude free","no-cost","open source"))) or "Check each tool's pricing page; we only list verified pricing.")+"."),
     (f'How does ShipStack rank {c["name"]}?','Rankings are editorial, based on maturity, fit for vibe coders and builders, and verification against each official site. Sponsorships never affect rank.')]
  return q
SUB='''<section id="signup"><h2>Get the weekly ShipStack drop</h2><p>New tools and rank changes, every week.</p><form id="signup-form" novalidate><input type="email" name="email" required placeholder="you@example.com" aria-label="Email"><input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0"><button type="submit">Subscribe</button><small role="status" aria-live="polite">No spam. Unsubscribe anytime.</small></form></section>'''
# home
btns='<button class="f on" data-c="all">All</button>'+"".join(f'<button class="f" data-c="{e(c["name"])}">{e(c["name"])}</button>' for c in cats)
news="".join(f'<li><time>{n["date"]}</time><div><span class="tag">{e(n["category"])}</span> <b>{e(n["name"])}</b> — {e(n["summary"])} <a href="{e(n["source"])}" target="_blank" rel="noopener">source</a></div></li>' for n in d["new_this_week"])
catlinks="".join(f'<a class="catlink" href="/{c["slug"]}/"><b>{e(c["name"])}</b><span>Top pick: {e(c["tools"][0]["name"])}</span></a>' for c in cats)
home_ld=[{"@context":"https://schema.org","@type":"WebSite","name":"ShipStack","url":SITE+"/"},{"@context":"https://schema.org","@type":"Organization","name":"ShipStack","url":SITE+"/","email":"shipstack.tools@gmail.com","sameAs":["https://x.com/shipstacktools"]},
 {"@context":"https://schema.org","@type":"ItemList","name":"Top AI tools for builders by category","itemListElement":[{"@type":"ListItem","position":i+1,"name":c["name"],"url":f'{SITE}/{c["slug"]}/'} for i,c in enumerate(cats)]}]
page("/","ShipStack — AI tools for vibe coders, ranked by use case",f"Ranked directory of {len(alltools)} verified AI tools for vibe coders and builders across {len(cats)} categories, plus new AI tool launches every week.",
 f'<section class="hero"><h1>The AI stack for vibe coders, <span>ranked by use case.</span></h1><p>{len(alltools)} tools across {len(cats)} categories · every tool verified against its official site · updated {UPD}</p><input id="q" placeholder="Search tools, e.g. auth, deploy, agent…" aria-label="Search tools"></section>'
 f'<section><div class="catgrid">{catlinks}</div></section>{featured()}<section id="new"><h2>🆕 New this week</h2><ul class="news">{news}</ul></section>'
 f'<section id="tools"><h2>All tools</h2><div class="filters">{btns}</div><div class="grid">{"".join(card(t) for t in alltools)}</div></section>{SUB}',home_ld)
# categories
for c in cats:
  qs=faq(c)
  jl=[{"@context":"https://schema.org","@type":"ItemList","name":f'Best {c["name"]}',"itemListOrder":"https://schema.org/ItemListOrderAscending","itemListElement":[{"@type":"ListItem","position":t["rank"],"name":t["name"],"url":f'{SITE}/tools/{t["slug"]}/'} for t in c["tools"]]},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"ShipStack","item":SITE+"/"},{"@type":"ListItem","position":2,"name":c["name"],"item":f'{SITE}/{c["slug"]}/'}]}]
  nw=[n for n in d["new_this_week"] if n["category"]==c["name"]]
  page(f'/{c["slug"]}/',f'Best {c["name"]} for Vibe Coders (2026) — ShipStack',f'Ranked: the {len(c["tools"])} best {c["name"]} tools for builders in 2026 — {", ".join(t["name"] for t in c["tools"][:3])} and more, with verified pricing.',
   f'<section class="hero small"><p class="crumb"><a href="/">ShipStack</a> / {e(c["name"])}</p><h1>Best {e(c["name"])} <span>(2026)</span></h1><p>Ranked for vibe coders and builders · verified {UPD}</p></section><section>{answer(c)}</section>{featured()}'
   f'<section><div class="grid">{"".join(card(t) for t in c["tools"])}</div></section>'+(f'<section><h2>New this week in {e(c["name"])}</h2><ul class="news">'+"".join(f'<li><time>{n["date"]}</time><div><b>{e(n["name"])}</b> — {e(n["summary"])} <a href="{e(n["source"])}" rel="noopener" target="_blank">source</a></div></li>' for n in nw)+'</ul></section>' if nw else "")+
   '<section class="faq"><h2>FAQ</h2>'+"".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in qs)+f'</section>{SUB}',jl)
# tools
for t in alltools:
  c=next(c for c in cats if c["name"]==t["category"]); alts=[x for x in c["tools"] if x is not t][:3]
  sa={"@context":"https://schema.org","@type":"SoftwareApplication","name":t["name"],"url":t["url"],"description":t["description"],"applicationCategory":"DeveloperApplication","operatingSystem":"Web"}
  ans=f'{t["name"]} is ranked #{t["rank"]} of {len(c["tools"])} in {c["name"]} on ShipStack. Best for: {t["best_for"]}. {t["rank_reason"]}.'
  page(f'/tools/{t["slug"]}/',f'{t["name"]} review: pricing, best for & alternatives — ShipStack',f'{t["name"]}: {t["description"]} Ranked #{t["rank"]} in {c["name"]}.'[:300],
   f'<section class="hero small"><p class="crumb"><a href="/">ShipStack</a> / <a href="/{c["slug"]}/">{e(c["name"])}</a> / {e(t["name"])}</p><h1>{e(t["name"])}</h1><p>{e(t["description"])}</p><a class="btn" href="{e(link(t))}" target="_blank" rel="{rel(t)}">Visit official site ↗</a></section>'
   f'<section><div class="answer"><h2>Is {e(t["name"])} right for you?</h2><p>{e(ans)}</p></div><dl class="facts"><dt>Rank</dt><dd>#{t["rank"]} in <a href="/{c["slug"]}/">{e(c["name"])}</a></dd><dt>Best for</dt><dd>{e(t["best_for"])}</dd><dt>Why this rank</dt><dd>{e(t["rank_reason"])}</dd><dt>Pricing</dt><dd>{e(t.get("pricing") or "Not verified — check the official site")}</dd><dt>Official site</dt><dd><a href="{e(t["url"])}" rel="noopener" target="_blank">{e(t["url"])}</a></dd><dt>Verified</dt><dd>{t["verified_date"]}</dd></dl></section>'
   f'<section><h2>Alternatives to {e(t["name"])}</h2><div class="grid">{"".join(card(x) for x in alts)}</div></section>',
   [sa,{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"ShipStack","item":SITE+"/"},{"@type":"ListItem","position":2,"name":c["name"],"item":f'{SITE}/{c["slug"]}/'},{"@type":"ListItem","position":3,"name":t["name"],"item":f'{SITE}/tools/{t["slug"]}/'}]}])
# advertise
page("/advertise/","Advertise on ShipStack — reach vibe coders and AI builders","Sponsor ShipStack: labeled featured placements and newsletter sponsorships for AI developer tools. Rankings are never for sale.",
 '<section class="hero small"><h1>Advertise on <span>ShipStack</span></h1><p>Reach vibe coders and builders choosing their AI stack.</p></section><section class="prose"><h2>Placements</h2><ul><li><b>Featured slot</b> — a clearly labeled “Featured · Sponsored” card on the homepage and category pages.</li><li><b>Newsletter sponsorship</b> — one labeled sponsor block in the weekly ShipStack drop.</li></ul><h2>Our rules</h2><ul><li>Sponsored placements are always labeled.</li><li>Rankings are editorial and cannot be bought.</li><li>Affiliate links, if used, are marked rel="sponsored" and disclosed.</li></ul><h2>Pricing</h2><p><b>Featured listing: $99 for 30 days.</b> Your tool appears in a labeled “Featured · Sponsored” card on the homepage and your category page, live within 1 business day of payment.</p><p><a class="btn" href="https://buy.stripe.com/5kQ9AU0r44JD4NFbVb38400" rel="noopener">Buy a featured listing — $99 →</a></p><p>Newsletter sponsorships: pricing on request.</p><h2>Contact</h2><p>Questions, custom placements, or newsletter sponsorships: <a href="mailto:shipstack.tools@gmail.com">shipstack.tools@gmail.com</a></p></section>')
# api + llms
os.makedirs("api",exist_ok=True)
api={"name":"ShipStack","url":SITE,"updated":UPD,"license":"Editorial data; please attribute ShipStack","categories":[{"name":c["name"],"slug":c["slug"],"url":f'{SITE}/{c["slug"]}/',"tools":[{k:t.get(k) for k in ["rank","name","slug","url","description","best_for","rank_reason","pricing","verified_date"]}|{"page":f'{SITE}/tools/{t["slug"]}/'} for t in c["tools"]]} for c in cats],"new_this_week":d["new_this_week"]}
json.dump(api,open("api/tools.json","w"),indent=2)
# Vercel treats /api as functions, so static api/tools.json 404s; serve it from /data via a rewrite in vercel.json
os.makedirs("data",exist_ok=True)
json.dump(api,open("data/tools.json","w"),indent=2)
L=[f"# ShipStack\n\n> ShipStack (shipstack.tools) ranks AI tools by use case for vibe coders and builders, and tracks new AI tool launches weekly. Data verified {UPD}. Rankings are editorial; sponsorships never affect rank.\n\n## Data\n- [Tools JSON API]({SITE}/api/tools.json): all tools, ranks, verified pricing\n- [Full text for LLMs]({SITE}/llms-full.txt)\n\n## Categories"]
L+= [f'- [Best {c["name"]}]({SITE}/{c["slug"]}/): top pick {c["tools"][0]["name"]}' for c in cats]
open("llms.txt","w").write("\n".join(L)+"\n")
F=[f"# ShipStack — full directory (verified {UPD})\n"]
for c in cats:
  F.append(f'\n## Best {c["name"]}\n\nBest for {USE[c["name"]]}: {c["tools"][0]["name"]}.\n')
  for t in c["tools"]: F.append(f'{t["rank"]}. {t["name"]} ({t["url"]}) — {t["description"]} Best for: {t["best_for"]}. Why: {t["rank_reason"]}.'+(f' Pricing: {t["pricing"]}.' if t.get("pricing") else ""))
F.append("\n## New this week\n"); F+=[f'- {n["date"]} — {n["name"]} [{n["category"]}]: {n["summary"]} Source: {n["source"]}' for n in d["new_this_week"]]
open("llms-full.txt","w").write("\n".join(F)+"\n")
urls=["/","/advertise/"]+[f'/{c["slug"]}/' for c in cats]+[f'/tools/{t["slug"]}/' for t in alltools]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{SITE}{u}</loc><lastmod>{UPD}</lastmod></url>\n" for u in urls)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(f"Built {len(urls)} HTML pages")
