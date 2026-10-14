// Vercel serverless function: POST /api/subscribe {email}
const RE = /^[^\s@]{1,64}@[^\s@]{1,255}\.[^\s@]{2,}$/;
const hits = new Map(); // best-effort per-instance rate limit
const WINDOW = 10 * 60 * 1000, MAX = 5;
const API = "https://api.resend.com";

function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter(t => now - t < WINDOW);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > MAX;
}
async function resend(path, method, body) {
  const r = await fetch(API + path, { method, headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" }, body: body ? JSON.stringify(body) : undefined });
  let j = {}; try { j = await r.json(); } catch {}
  return { status: r.status, ok: r.ok, data: j };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ ok: false, error: "Method not allowed" }); }
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};
  if (body.website) return res.status(200).json({ ok: true }); // honeypot: silently accept bots
  const email = String(body.email || "").trim().toLowerCase();
  if (email.length > 254 || !RE.test(email)) return res.status(400).json({ ok: false, error: "Please enter a valid email address." });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ ok: false, error: "Too many attempts. Please try again later." });
  const seg = process.env.RESEND_AUDIENCE_ID;
  if (!process.env.RESEND_API_KEY || !seg) return res.status(500).json({ ok: false, error: "Signup is temporarily unavailable." });
  try {
    const pre = await resend(`/contacts/${encodeURIComponent(email)}`, "GET");
    let existing = pre.ok && !!pre.data.id;
    const c = await resend("/contacts", "POST", { email, unsubscribed: false, segments: [{ id: seg }] });
    if (!c.ok) {
      const msg = JSON.stringify(c.data).toLowerCase();
      if (c.status === 409 || msg.includes("exist")) {
        existing = true;
        const a = await resend(`/contacts/${encodeURIComponent(email)}/segments/${seg}`, "POST");
        if (!a.ok && !JSON.stringify(a.data).toLowerCase().includes("exist")) throw new Error("segment add failed " + a.status);
      } else throw new Error("contact create failed " + c.status + " " + msg);
    }
    if (!existing) {
      const m = await resend("/emails", "POST", {
        from: "Patricia at ShipStack <hello@shipstack.tools>", to: [email], reply_to: "shipstack.tools@gmail.com",
        subject: "Welcome to ShipStack! 🚀",
        text: "Hey there, welcome to ShipStack! 🎉\n\nYou're all set to get our weekly roundup of the freshest AI tools for vibe coders, ranked and ready to ship with.\nIn the meantime, explore the full list at https://shipstack.tools\n\nHappy building!\nPatricia at ShipStack",
        html: '<p>Hey there, welcome to ShipStack! 🎉</p><p>You\'re all set to get our weekly roundup of the freshest AI tools for vibe coders, ranked and ready to ship with. In the meantime, explore the full list at <a href="https://shipstack.tools" style="color:#7c5cff">shipstack.tools</a>.</p><p>Happy building!<br>Patricia at ShipStack</p>',
      });
      if (!m.ok) console.error("welcome email failed", m.status, JSON.stringify(m.data));
    }
    return res.status(200).json({ ok: true, existing });
  } catch (e) {
    console.error(e.message);
    return res.status(502).json({ ok: false, error: "Something went wrong. Please try again." });
  }
};
