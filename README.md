# Zahra Properties — website

Public website for Zahra Properties LLC (Columbus, Ohio): rentals, online application,
resident repair requests and investor inquiries. Hosted on Netlify.

## How it works
- Plain HTML + CSS, no framework. Pages live in `src/pages/`; the shared header and footer are in `tools/build.py`.
- After editing a page: `python3 tools/build.py` (writes the `.html` files at the repo root), then commit.
- Forms use **Netlify Forms** (no database yet): `viewing-request`, `listing-alerts`, `rental-application`,
  `repair-request`, `investor-inquiry`. Submissions appear in Netlify → Forms.
  Turn on email notifications there (Forms → Form notifications → Email) to the owner's inbox.

## Brand
Navy `#1B2A41` · Brass `#B08D57` · Ivory `#FAF8F4` · Cormorant Garamond + Inter. Logo files in `assets/img/`.

## Roadmap (phase 2)
Live listings managed from an owner dashboard, viewing calendar, resident portal with repair tracking,
automatic reminders (rent, renewals, viewings) — Supabase + Next.js, same stack as the Kër Téranga project.
