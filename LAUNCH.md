# Cited — Launch Handoff (things only you can do)

The business is built and live. These items need your accounts/credentials.
Each takes ~5–10 minutes.

## 1. Payment rails (highest priority — this is what blocks "checkout")
Full plan in `cited/STRIPE-PLAN.md`. Two routes now:

**Route A (new, fastest):** the Stripe MCP server is configured in this CLI
(`~/.kimi-code/mcp.json`). Restart the CLI — it will prompt you to
authenticate Stripe (OAuth in browser). Once connected, I create the 3
products + payment links ($250 / $950 / $2,500) myself and swap the site
CTAs in the same session. The `/paid.html` post-payment intake page is
already built and deployed.

**Route B (manual, ~10 min):**
1. Create/login at https://stripe.com (free, no monthly fee)
2. Products → Add: "AI Visibility Audit", one-time $950 (optionally also
   $250 Snapshot and $2,500 Audit+Sprint — see gig packages)
3. Create a **Payment Link** per product, set the after-payment redirect to
   https://adnanettaki.github.io/cited/paid.html
4. Send me the link(s) — I'll swap every
   `mailto:adnanettaki6@gmail.com?...Start your audit` CTA on the page

Do NOT enable Stripe Tax / automatic_tax yet — see STRIPE-PLAN.md tax note.

PayPal alternative: create a paypal.me link and I'll add it as a second option.

## 2. Sending the outreach
Templates live in `cited/outreach-templates.md`. Approve/edit them, then:
- Send from adnanettaki6@gmail.com (or a fresh domain mailbox later), or
- Grant this CLI Gmail access (Composio Gmail is configured in Antigravity
  IDE but not reachable from this CLI) and I'll send + track them for you.

## 3. Prospect list
`cited/prospects.md` — 25 verified DTC brands with real contact emails.
Top-5 flagged: Loftie, Sundays for Dogs, Arrae, Bells of Steel, Bearaby.
Per-brand ready-to-send emails: `cited/outreach-ready/*.md`.
10 live sample audits to link in pitches: https://adnanettaki.github.io/cited/

## 3b. Marketplace gigs (new — paste-ready)
`cited/gig-copy.md` — Fiverr gig (title, packages $250/$950/$2,500, FAQ,
image brief) and Upwork profile + proposal template. You create the accounts
(they require phone/ID); everything to paste is written.

## 3c. Reddit / Indie Hackers playbook (new — paste-ready)
`cited/reddit-playbook.md` — which subs to watch, 4 reply templates for the
weekly "traffic dropped / how do I rank in ChatGPT" posts, and a
build-in-public post that leads with the 10 audit findings and offers 3 free
snapshots. You post them from your own account.

## 4. Optional upgrades (all free)
- Custom domain later (~$12/yr — needs your OK per the no-spending rule)
- Calendly free account for the walkthrough-call booking → I'll embed it
- Google Sheet for the outreach tracker → share it with me

## What is NOT done / honest status
- No paying customers yet. Revenue starts when outreach converts.
- Payment collection awaits your Stripe/PayPal link (step 1).
- No testimonials on the page on purpose — we don't have real ones yet and
  the goal rules forbid faking them. First 2–3 clients become the proof.
