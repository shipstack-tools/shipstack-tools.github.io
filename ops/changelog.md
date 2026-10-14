# ShipStack changelog

## 2026-10-13
- MVP: tools.json + static site (8 categories, 42 tools), "New this week", placeholder newsletter form.
- Verification pass: all 42 tools checked against official sites; `verified_date` added; 27 tools with pricing from official pricing pages.
  - Windsurf -> "Devin Desktop (formerly Windsurf)" (rebranded Jun 2, 2026).
  - URL fixes: Claude Code, Anthropic API, LangSmith. Several descriptions refreshed.
  - "New this week" expanded to 20 launches (Oct 6–13) across all categories.
- SEO/LLM phase: per-category and per-tool pages, canonical/OG/Twitter tags, JSON-LD (WebSite, ItemList, SoftwareApplication, FAQPage, BreadcrumbList), sitemap.xml, robots.txt, llms.txt, llms-full.txt, /api/tools.json, answer blocks.
- Monetization prep: `affiliate_url` field (empty), empty labeled Featured slot (`featured` in tools.json), /advertise/ page (no prices).
- 2026-10-13: Newsletter signup wired to Resend: /api/subscribe (honeypot, rate limit, welcome email), segment 'ShipStack Newsletter' (7067af20-b2a6-46bb-b595-ec68a8a3e8f9), fetch-based form with inline messages; build.py preserves api/subscribe.js.

## 2026-10-14
- Daily release update (catch-up run): added 9 verified items to "New this week" (Hermes Agent v0.22.0, Claude Platform OTel traces beta, Claude Code 2.1.299, Tiden, Reason, Epherem, Gemini 4 Argon in GitHub Copilot, GitLab Duo agent orchestration, OpenCode 2.0); dropped items older than Oct 7 (Figma agent GA, Bond, Tofu). No pricing/ranking changes verified.
- Bug fix: /api/tools.json returned 404 on Vercel (the /api dir is treated as serverless functions). build.py now also writes data/tools.json and vercel.json rewrites /api/tools.json to it.
- Committed regenerated pages from the @shipstacktools X-handle change (twitter:site, Organization JSON-LD, footer link) that were built but not committed.
