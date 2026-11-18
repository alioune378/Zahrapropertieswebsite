"""Build the static site: wraps every src/pages/*.html body in the shared layout.

Each page file starts with a JSON header line:
  <!-- {"title": "...", "description": "...", "nav": "rentals", "file": "rentals.html"} -->
Run:  python3 tools/build.py      (writes the .html files at the repo root)
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://zahraproperties.netlify.app'  # change when the custom domain is live

NAV = [('rentals', '/rentals', 'Rentals'), ('residents', '/residents', 'Residents'),
       ('investors', '/investors', 'Investors'), ('contact', '/#contact', 'Contact')]

ICON_MENU = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def layout(meta, body):
    current = meta.get('nav', '')
    cur = ' aria-current="page"'
    links = '\n'.join(
        '        <a href="%s"%s>%s</a>' % (href, cur if key == current else '', label)
        for key, href, label in NAV)
    path = '/' if meta['file'] == 'index.html' else '/' + meta['file'].removesuffix('.html')
    title = meta['title'] if meta['file'] == 'index.html' else f"{meta['title']} · Zahra Properties"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta['description']}">
  <link rel="canonical" href="{SITE}{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Zahra Properties">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta['description']}">
  <meta property="og:image" content="{SITE}/assets/img/og-zahra.jpg">
  <meta property="og:url" content="{SITE}{path}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#1B2A41">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/" aria-label="Zahra Properties home"><img src="/assets/img/logo.svg" alt="Zahra Properties" width="240" height="52"></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">{ICON_MENU}</button>
      <nav id="site-nav" class="nav" aria-label="Main">
{links}
        <a class="btn btn-navy" href="/rentals#viewing">Book a viewing</a>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer" id="contact">
    <div class="wrap">
      <div class="cols">
        <div class="stack" style="gap:14px">
          <img src="/assets/img/logo.svg" alt="Zahra Properties" width="200" height="44" style="height:52px;width:auto;align-self:flex-start">
          <p class="muted">Locally owned and managed rental homes in Columbus, Ohio, since 2010.</p>
        </div>
        <div>
          <h2>Get in touch</h2>
          <ul>
            <li><a href="/rentals#viewing">Request a viewing</a></li>
            <li><a href="/investors#talk">Investor &amp; partner inquiries</a></li>
            <li><a href="/residents#repair">Residents: request a repair</a></li>
            <li class="muted">Columbus, Ohio</li>
          </ul>
        </div>
        <div>
          <h2>Explore</h2>
          <ul>
            <li><a href="/rentals">Rentals</a></li>
            <li><a href="/apply">Apply online</a></li>
            <li><a href="/residents">Residents</a></li>
            <li><a href="/investors">Investors</a></li>
          </ul>
        </div>
        <div>
          <h2>Fair housing</h2>
          <p class="muted">Zahra Properties is an Equal Housing Opportunity provider. We do not discriminate on any basis protected by federal, Ohio or local law.</p>
        </div>
      </div>
      <div class="legal">
        <span>© <span data-year>2026</span> Zahra Properties LLC</span>
        <span class="eho">Equal Housing Opportunity</span>
      </div>
    </div>
  </footer>
  <script>
    (function () {{
      var b = document.querySelector('.menu-toggle'), n = document.getElementById('site-nav');
      if (b && n) b.addEventListener('click', function () {{
        var open = n.classList.toggle('open'); b.setAttribute('aria-expanded', open ? 'true' : 'false');
      }});
      var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
    }})();
  </script>
</body>
</html>
'''


def main():
    for src in sorted((ROOT / 'src' / 'pages').glob('*.html')):
        text = src.read_text(encoding='utf-8')
        m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', text, re.S)
        meta = json.loads(m.group(1))
        (ROOT / meta['file']).write_text(layout(meta, text[m.end():].rstrip() + '\n'), encoding='utf-8')
        print('built', meta['file'])


if __name__ == '__main__':
    main()
