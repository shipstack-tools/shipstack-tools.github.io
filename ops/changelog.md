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
