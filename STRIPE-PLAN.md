# Cited — Stripe Integration Plan

Business context: solo service business, static site on GitHub Pages (no
server, no backend), CH-based seller, mostly US/EU clients. Products:
one-time audits ($250 Basic / $950 Standard / $2,500 Premium) and later a
$2,500/mo implementation-sprint retainer.

Grounded in the installed `stripe-best-practices` skill (docs.stripe.com).

## Phase A — Payment Links (this week, zero code, zero keys)

Payment Links are Stripe Checkout without a backend — correct choice for a
static site. Do NOT build a custom PaymentIntents integration; there is no
server to hold the secret key, and embedding keys in the static site would
be a security breach.

1. Create 3 products in Stripe Dashboard (or via Stripe MCP once authed):
   - "AI Visibility Snapshot" — $250 one-time
   - "AI Visibility Audit" — $950 one-time (the flagship)
   - "AI Visibility Audit + 30-day Sprint" — $2,500 one-time
2. Create one Payment Link per product.
3. After-payment redirect: a `/paid.html` page on the site with the intake
   questions (store URL, top 3 competitors, target queries). This replaces
   the mailto intake.
4. Swap the 6 mailto CTAs in `index.html` for the payment links. (I do this
   the moment links exist — 5-minute edit + push.)
5. Fulfillment notification: Stripe's built-in payment-receipt emails to
   adnanettaki6@gmail.com are enough at this volume.

## Phase B — retainer subscription (when the first sprint sells)

- $2,500/mo sprint → Stripe Billing: a recurring Price + its own Payment
  Link (Payment Links support subscriptions; still no backend needed).
- Subscriptions REQUIRE webhooks for lifecycle events per best practices —
  at that point add a free-tier webhook endpoint (Cloudflare Worker or
  Stripe's own "no-code" notification rules) rather than a full server.

## Phase C — only if volume justifies (50+ payments/mo)

- Real backend + Checkout Sessions with `integration_identifier` tagging,
  `checkout.session.completed` + `checkout.session.async_payment_succeeded`
  webhook fulfillment (never fulfill on the success page).
- Restricted API key (`rk_…`), never a secret key, never client-side.

## Tax — deliberate decision, not a default

Do NOT enable `automatic_tax` yet. Stripe Tax collects nothing without an
active tax registration (most common Stripe Tax mistake). A CH seller
selling services to US clients is generally outside US sales tax; EU B2B is
reverse-charge; CH VAT applies only above CHF 100k worldwide turnover.
Action: confirm registration status before flipping any tax switch. Until
then prices are tax-exclusive as displayed.

## Key handling rules (apply from day one)

- No Stripe keys in the repo, in `.env` is fine locally (already gitignored
  pattern), never in `index.html` or any committed file.
- Payment Links need no keys at all — that's the point of Phase A.
- If API access is ever needed: restricted key with the minimum scopes.

## Immediate unblock path

Stripe MCP server is added to this CLI's config (`~/.kimi-code/mcp.json`).
After a CLI restart it will prompt for OAuth; once authenticated I can
create the 3 products + payment links via the MCP tools myself and swap the
site CTAs in the same session. Dashboard manual creation (steps in
LAUNCH.md §1) remains the fallback.
