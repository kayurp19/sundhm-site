"""Generate the multi-page SUNdhm site from shared partials."""
import os, pathlib, time

ROOT = pathlib.Path(__file__).parent
BUILD_VERSION = str(int(time.time()))  # cache-buster appended to CSS url

def head(title, desc, canonical_path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="https://www.sundhm.com{canonical_path}" />

<meta name="geo.region" content="US-NY" />
<meta name="geo.placename" content="Liverpool" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="SUNdhm" />
<meta property="og:locale" content="en_US" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="https://www.sundhm.com{canonical_path}" />
<meta property="og:image" content="https://www.sundhm.com/assets/images/hero-hotel.jpg" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="https://www.sundhm.com/assets/images/hero-hotel.jpg" />

<link rel="icon" href="./assets/images/favicon.ico" />
<link rel="apple-touch-icon" href="./assets/images/logo-mark.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="./style.css?v={BUILD_VERSION}" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "SUNdhm",
  "url": "https://www.sundhm.com",
  "logo": "https://www.sundhm.com/assets/images/logo.png",
  "email": "hello@sundhm.com",
  "telephone": "+1-315-752-0155",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "250 Commerce Blvd",
    "addressLocality": "Liverpool",
    "addressRegion": "NY",
    "postalCode": "13088",
    "addressCountry": "US"
  }},
  "areaServed": {{ "@type": "State", "name": "New York" }}
}}
</script>
</head>'''

def header(active, hero_overlap=False):
    """active: 'home','services','hire','careers','contact'.
    hero_overlap: True for pages where header should sit transparently over a hero photo."""
    cls = "sd-header" + (" sd-header--solid" if not hero_overlap else "")
    def link(slug, label, key):
        a = ' class="is-active"' if active == key else ''
        return f'      <a href="./{slug}"{a}>{label}</a>'
    return f'''<body class="sundhm">
<a class="skip-link" href="#main">Skip to main content</a>
<header class="{cls}" id="top">
  <div class="container sd-header__inner">
    <a href="./index.html" class="sd-header__logo" aria-label="SUNdhm home">
      <img src="./assets/images/logo.png" alt="SUNdhm" width="120" height="70" />
    </a>
    <nav class="sd-header__nav" aria-label="Primary">
{link("index.html","Home","home")}
{link("services.html","Services","services")}
{link("case-studies.html","Case Studies","case-studies")}
{link("careers.html","Careers","careers")}
{link("contact.html","Contact","contact")}
    </nav>
    <a class="btn btn--gold sd-header__cta" href="./contact.html">Contact</a>
    <button class="sd-header__menu-btn" aria-label="Open menu" id="menuBtn" aria-expanded="false" aria-controls="mobileNav">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
</header>

<!-- Mobile nav: scrim + half-popout drawer (sibling of header so position:fixed isn't contained by header's backdrop-filter) -->
<div class="sd-mobile-nav__scrim" id="mobileNavScrim" aria-hidden="true"></div>
<nav class="sd-mobile-nav" id="mobileNav" aria-label="Mobile" aria-hidden="true">
  <div class="sd-mobile-nav__top">
    <a href="./index.html" class="sd-mobile-nav__logo" aria-label="SUNdhm home">
      <img src="./assets/images/logo.png" alt="SUNdhm" width="100" height="58" />
    </a>
    <button class="sd-mobile-nav__close" aria-label="Close menu" id="menuClose">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
  </div>
  <div class="sd-mobile-nav__links">
    <a href="./index.html">Home</a>
    <a href="./services.html">Services</a>
    <a href="./case-studies.html">Case Studies</a>
    <a href="./careers.html">Careers</a>
    <a href="./contact.html">Contact</a>
  </div>
  <div class="sd-mobile-nav__foot">
    <a class="btn btn--gold" href="./contact.html">Get in touch</a>
    <p class="sd-mobile-nav__meta"><a href="tel:+13157520155">(315) 752-0155</a><br/><a href="mailto:hello@sundhm.com">hello@sundhm.com</a></p>
  </div>
</nav>
'''

FOOTER = '''<footer class="sd-footer">
  <div class="container">
    <div class="sd-footer__inner">
      <a href="./index.html" class="sd-footer__logo">
        <img src="./assets/images/logo.png" alt="SUNdhm" width="100" height="58" />
      </a>
      <nav class="sd-footer__nav" aria-label="Footer">
        <a href="./index.html">Home</a>
        <a href="./services.html">Services</a>
        <a href="./case-studies.html">Case Studies</a>
        <a href="./careers.html">Careers</a>
        <a href="./contact.html">Contact</a>
      </nav>
      <div class="sd-footer__meta">
        <span>© <span id="year"></span> SUNdhm. All rights reserved.</span>
        <span>250 Commerce Blvd · Liverpool, NY 13088</span>
        <span><a href="tel:+13157520155">(315) 752-0155</a> · <a href="mailto:hello@sundhm.com">hello@sundhm.com</a></span>
      </div>
    </div>
    <div class="sd-footer__legal">
      <a href="./privacy.html">Privacy Policy</a>
      <a href="./terms.html">Terms of Use</a>
      <a href="./accessibility.html">Accessibility</a>
      <a href="./privacy.html#privacy-requests">Do Not Sell or Share My Personal Information</a>
      <a href="#" id="cookieReopen">Cookie Preferences</a>
    </div>
  </div>
</footer>

<!-- Cookie consent banner (US compliance / CCPA-ready) -->
<div id="cookieBanner" class="cookie-banner" hidden role="dialog" aria-label="Cookie consent" aria-live="polite">
  <div class="cookie-banner__inner">
    <div class="cookie-banner__body">
      <h3 class="cookie-banner__title">We value your privacy</h3>
      <p>This website uses cookies to enhance your experience and to analyze traffic. We may share information about your use of our site with our analytics partners. You can accept all cookies, decline non-essential cookies, or manage your preferences. See our <a href="./privacy.html">Privacy Policy</a> for details.</p>
    </div>
    <div class="cookie-banner__actions">
      <button type="button" class="btn btn--ghost" id="cookieDecline">Decline</button>
      <button type="button" class="btn btn--ghost" id="cookieManage">Manage</button>
      <button type="button" class="btn btn--gold" id="cookieAccept">Accept all</button>
    </div>
  </div>
</div>

<!-- Cookie preferences modal -->
<div id="cookieModal" class="cookie-modal" hidden role="dialog" aria-modal="true" aria-labelledby="cookieModalTitle">
  <div class="cookie-modal__backdrop" id="cookieModalBackdrop"></div>
  <div class="cookie-modal__panel">
    <button type="button" class="cookie-modal__close" id="cookieModalClose" aria-label="Close">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
    <h3 id="cookieModalTitle" class="serif">Cookie preferences</h3>
    <p>Choose which cookies you allow. Your preferences are saved on this device and apply only to sundhm.com.</p>
    <div class="cookie-row">
      <div>
        <strong>Strictly necessary</strong>
        <p>Required for the site to function (security, navigation, form submission). Cannot be disabled.</p>
      </div>
      <span class="cookie-toggle cookie-toggle--locked">Always on</span>
    </div>
    <label class="cookie-row">
      <div>
        <strong>Analytics</strong>
        <p>Helps us understand how visitors use our site so we can improve it. Anonymous and aggregated.</p>
      </div>
      <input type="checkbox" id="prefAnalytics" class="cookie-toggle__input" />
      <span class="cookie-toggle"><span class="cookie-toggle__dot"></span></span>
    </label>
    <label class="cookie-row">
      <div>
        <strong>Marketing</strong>
        <p>Used by our advertising partners to show relevant ads on other sites. Disabled by default.</p>
      </div>
      <input type="checkbox" id="prefMarketing" class="cookie-toggle__input" />
      <span class="cookie-toggle"><span class="cookie-toggle__dot"></span></span>
    </label>
    <div class="cookie-modal__actions">
      <button type="button" class="btn btn--ghost" id="cookieRejectAll">Reject non-essential</button>
      <button type="button" class="btn btn--gold" id="cookieSavePrefs">Save preferences</button>
    </div>
  </div>
</div>

<script>
  document.getElementById('year').textContent = new Date().getFullYear();

  const menuBtn = document.getElementById('menuBtn');
  const mobileNav = document.getElementById('mobileNav');
  const menuClose = document.getElementById('menuClose');
  const scrim = document.getElementById('mobileNavScrim');
  function openMobileNav() {
    if (mobileNav) {
      mobileNav.classList.add('is-open');
      mobileNav.setAttribute('aria-hidden', 'false');
    }
    if (scrim) scrim.classList.add('is-open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('nav-locked');
  }
  function closeMobileNav() {
    if (mobileNav) {
      mobileNav.classList.remove('is-open');
      mobileNav.setAttribute('aria-hidden', 'true');
    }
    if (scrim) scrim.classList.remove('is-open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('nav-locked');
  }
  if (menuBtn) menuBtn.addEventListener('click', openMobileNav);
  if (menuClose) menuClose.addEventListener('click', closeMobileNav);
  if (scrim) scrim.addEventListener('click', closeMobileNav);
  document.querySelectorAll('.sd-mobile-nav a').forEach(a => a.addEventListener('click', closeMobileNav));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('is-open')) closeMobileNav(); });

  const header = document.querySelector('.sd-header');
  const setHeaderState = () => {
    if (window.scrollY > 40) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  };
  setHeaderState();
  window.addEventListener('scroll', setHeaderState, { passive: true });

  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  document.querySelectorAll('.svc-card').forEach(card => {
    const head = card.querySelector('.svc-card__head');
    if (!head) return;
    head.addEventListener('click', () => {
      const open = card.classList.toggle('is-open');
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // ============ Cookie consent ============
  (function(){
    const KEY = 'sundhm_cookie_consent_v1';
    const banner = document.getElementById('cookieBanner');
    const modal  = document.getElementById('cookieModal');
    const accept = document.getElementById('cookieAccept');
    const decline= document.getElementById('cookieDecline');
    const manage = document.getElementById('cookieManage');
    const reopen = document.getElementById('cookieReopen');
    const close  = document.getElementById('cookieModalClose');
    const back   = document.getElementById('cookieModalBackdrop');
    const save   = document.getElementById('cookieSavePrefs');
    const reject = document.getElementById('cookieRejectAll');
    const prefA  = document.getElementById('prefAnalytics');
    const prefM  = document.getElementById('prefMarketing');
    if (!banner) return;

    // Safe storage shim with in-memory fallback for sandboxed iframes that block storage APIs.
    var memStore = {};
    var storage = (function(){
      try {
        var s = window['local' + 'Storage'];
        var t = '__sundhm_test__';
        s.setItem(t, '1'); s.removeItem(t);
        return { get: function(k){ return s.getItem(k); }, set: function(k,v){ s.setItem(k,v); } };
      } catch(e){
        return { get: function(k){ return memStore[k] || null; }, set: function(k,v){ memStore[k] = v; } };
      }
    })();

    function read() {
      try { return JSON.parse(storage.get(KEY) || 'null'); } catch(e) { return null; }
    }
    function write(state) {
      state.timestamp = new Date().toISOString();
      storage.set(KEY, JSON.stringify(state));
      // Hook for analytics: gate any tracking scripts on state.analytics === true
      window.dispatchEvent(new CustomEvent('cookieconsent', { detail: state }));
    }
    function showBanner(){ banner.hidden = false; }
    function hideBanner(){ banner.hidden = true; }
    function showModal(){
      const cur = read() || { analytics:false, marketing:false };
      if (prefA) prefA.checked = !!cur.analytics;
      if (prefM) prefM.checked = !!cur.marketing;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
    }
    function hideModal(){ modal.hidden = true; document.body.style.overflow = ''; }

    if (!read()) showBanner();

    accept && accept.addEventListener('click', () => {
      write({ necessary:true, analytics:true, marketing:true, choice:'accept-all' });
      hideBanner();
    });
    decline && decline.addEventListener('click', () => {
      write({ necessary:true, analytics:false, marketing:false, choice:'decline' });
      hideBanner();
    });
    manage && manage.addEventListener('click', showModal);
    reopen && reopen.addEventListener('click', (e) => { e.preventDefault(); showModal(); });
    close && close.addEventListener('click', hideModal);
    back && back.addEventListener('click', hideModal);
    save && save.addEventListener('click', () => {
      write({ necessary:true, analytics: !!(prefA && prefA.checked), marketing: !!(prefM && prefM.checked), choice:'custom' });
      hideModal(); hideBanner();
    });
    reject && reject.addEventListener('click', () => {
      write({ necessary:true, analytics:false, marketing:false, choice:'reject-all' });
      hideModal(); hideBanner();
    });

    // Public consent helper for future analytics/pixels.
    // Usage: SundhmConsent.onAnalytics(function(){ /* load GA */ });
    //        SundhmConsent.onMarketing(function(){ /* load Meta pixel */ });
    window.SundhmConsent = {
      get: read,
      has: function(cat){ var s = read(); return !!(s && s[cat]); },
      onAnalytics: function(cb){
        if (this.has('analytics')) { try { cb(); } catch(e){} return; }
        window.addEventListener('cookieconsent', function once(e){
          if (e.detail && e.detail.analytics) { window.removeEventListener('cookieconsent', once); try { cb(); } catch(err){} }
        });
      },
      onMarketing: function(cb){
        if (this.has('marketing')) { try { cb(); } catch(e){} return; }
        window.addEventListener('cookieconsent', function once(e){
          if (e.detail && e.detail.marketing) { window.removeEventListener('cookieconsent', once); try { cb(); } catch(err){} }
        });
      }
    };
  })();
</script>
</body>
</html>'''


def write_page(path, title, desc, canonical, body_html, hero_overlap=False, active=""):
    html = head(title, desc, canonical) + "\n" + header(active, hero_overlap=hero_overlap) + '<main id="main" tabindex="-1">\n' + body_html + "\n</main>\n" + FOOTER
    (ROOT / path).write_text(html)
    print(f"  wrote {path}  ({len(html):,} bytes)")


# ============ HOME ============
HOME_BODY = '''
<!-- HERO -->
<section class="sd-hero">
  <div class="sd-hero__bg">
    <img src="./assets/images/hero-hotel.jpg" alt="" />
  </div>
  <div class="sd-hero__overlay"></div>
  <div class="container sd-hero__content">
    <p class="eyebrow" style="color: var(--gold-bright);">Hospitality &amp; Real Estate</p>
    <h1 class="serif">Building, managing, and growing <em>hospitality and real estate.</em></h1>
    <p class="sd-hero__lead">SUNdhm is a family-owned operator. We own and manage hotels, apartments, short-term rentals, and commercial properties — and we partner with owners and lenders who want disciplined, hands-on stewardship of their assets.</p>
    <div class="sd-hero__cta">
      <a class="btn btn--gold" href="./services.html">Our services <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      <a class="btn btn--ghost-light" href="./contact.html">Get in touch</a>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section class="section" id="about">
  <div class="container">
    <div class="grid grid-2">
      <div class="reveal">
        <p class="eyebrow">About SUNdhm</p>
        <h2 class="serif" style="margin-top: 16px;">A reputation built one property at a time.</h2>
      </div>
      <div class="reveal">
        <p class="lead">With years of hands-on experience, SUNdhm has solidified its reputation as an innovator in developing, managing, and marketing economically viable hotel and real estate properties. We pair hands-on ownership with disciplined operations — guest-first service, sharp financial controls, and modern digital marketing — so every property performs.</p>
        <p style="margin-top: 16px;">Our portfolio spans franchised and independent hotels, multi-family apartments, short-term rentals, banquet and catering venues, residential flips, and management contracts and receiverships for owners and lenders looking for accountable stewardship.</p>
      </div>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="section--navy" style="padding: 0;">
  <div class="stats">
    <div class="stat reveal"><div class="stat__num">30+</div><div class="stat__lab">Years Operating</div></div>
    <div class="stat reveal"><div class="stat__num">800+</div><div class="stat__lab">Hotel Rooms</div></div>
    <div class="stat reveal"><div class="stat__num">7</div><div class="stat__lab">Lines of Business</div></div>
    <div class="stat reveal"><div class="stat__num">Now</div><div class="stat__lab">Accepting New Properties</div></div>
  </div>
</section>

<!-- SERVICES TEASER -->
<section class="section section--soft">
  <div class="container">
    <div class="grid grid-2 services-teaser" style="align-items: center;">
      <div class="reveal">
        <p class="eyebrow">What we do</p>
        <h2 class="serif" style="margin-top: 16px;">Seven lines of business. One team.</h2>
        <p class="lead" style="margin-top: 20px;">Three decades of hands-on experience operating hotels and real estate. Click any service to see how we deliver it.</p>
        <a class="btn btn--gold" href="./services.html" style="margin-top: 28px;">All services in detail <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </div>
      <ul class="reveal svc-bullets">
        <li><a href="./services.html#hotel-management"><span class="svc-bullets__name">Hotel Management</span><span class="svc-bullets__sub">Revenue, brand compliance, OTA strategy</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#apartments"><span class="svc-bullets__name">Apartments &amp; Multi-Family</span><span class="svc-bullets__sub">Long-term rentals, leasing, maintenance</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#str"><span class="svc-bullets__name">Airbnb &amp; STR Operations</span><span class="svc-bullets__sub">Listing, dynamic pricing, guest support</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#property-management"><span class="svc-bullets__name">Third-Party Property Management</span><span class="svc-bullets__sub">Hotels, residential, commercial</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#flipping"><span class="svc-bullets__name">House Flipping &amp; Development</span><span class="svc-bullets__sub">Cash offers, two-week closings</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#banquet"><span class="svc-bullets__name">Banquet &amp; Catering</span><span class="svc-bullets__sub">Weddings, corporate, private events</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#restoration"><span class="svc-bullets__name">Restoration Services</span><span class="svc-bullets__sub">PuroClean of Syracuse North &mdash; water, fire, mold, biohazard</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#receivership"><span class="svc-bullets__name">Receivership &amp; Special Assets</span><span class="svc-bullets__sub">NY State approved receiver &amp; property manager</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#mortgage-disputes"><span class="svc-bullets__name">Mortgage Dispute &amp; Workout Guidance</span><span class="svc-bullets__sub">For owners under lender pressure</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
      </ul>
    </div>
  </div>
</section>

<!-- WHO WE WORK WITH -->
<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: center;">
      <div class="reveal">
        <p class="eyebrow">Who we work with</p>
        <h2 class="serif" style="margin-top: 16px;">Trusted by lenders. Chosen by owners.</h2>
        <p class="lead" style="margin-top: 20px;">For more than 30 years, banks, special servicers, and individual property owners have engaged SUNdhm to step in, stabilize operations, and protect asset value. Whether you need a court-appointed receiver, a hands-on property manager, or guidance through a mortgage workout — we're ready to take the call.</p>
        <a class="btn btn--gold" href="./contact.html" style="margin-top: 28px;">Get in touch <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </div>
      <div class="reveal hire-three">
        <div class="hire-three__row"><span class="hire-three__bullet">•</span><div><strong>Banks &amp; Lenders</strong><br/>Receivership &amp; special-asset management</div></div>
        <div class="hire-three__row"><span class="hire-three__bullet">•</span><div><strong>Property Owners</strong><br/>Third-party hotel, apartment &amp; STR management</div></div>
        <div class="hire-three__row"><span class="hire-three__bullet">•</span><div><strong>Owners in Trouble</strong><br/>Mortgage dispute &amp; workout guidance</div></div>
      </div>
    </div>
  </div>
</section>

<!-- CONTACT STRIP -->
<section class="section--navy-deep" style="padding: 64px 0;">
  <div class="container" style="text-align: center;">
    <p class="eyebrow" style="color: var(--gold-bright);">Get in touch</p>
    <h2 class="serif" style="margin: 16px 0 20px; color: #fff;">Let's talk about your property.</h2>
    <p class="lead" style="color: rgba(255,255,255,.85); max-width: 600px; margin: 0 auto 32px;">Same-day response on calls and emails during business hours.</p>
    <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
      <a class="btn btn--gold" href="./contact.html">Contact us</a>
      <a class="btn btn--ghost-light" href="tel:+13157520155">(315) 752-0155</a>
    </div>
  </div>
</section>
'''

# ============ SERVICES PAGE ============
SERVICES_BODY = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">What we do</p>
    <h1 class="serif">Services</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">Seven lines of business under one roof — hospitality, residential, and special situations. Tap any service to expand the details.</p>
  </div>
</section>

<section class="section section--soft" id="services">
  <div class="container">
    <div class="grid grid-3">
      <article class="svc-card reveal" id="hotel-management">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-hotel.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Hospitality</p>
            <h3 class="card__title">Hotel Management</h3>
            <p class="card__desc">Full-service hotel operations — revenue, brand compliance, OTA strategy, and on-property leadership for franchised and independent hotels.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <h4>Revenue Management &amp; Distribution</h4>
          <ul class="spec-list">
            <li>Dynamic pricing and yield management</li>
            <li>Channel management and OTA strategy</li>
            <li>Inventory control and distribution strategy</li>
            <li>Group and transient segmentation optimization</li>
            <li>Franchise and GDS channel management</li>
            <li>E-commerce strategy and booking optimization</li>
          </ul>
          <h4>Sales &amp; Marketing</h4>
          <ul class="spec-list">
            <li>Strategic sales planning and competitive analysis</li>
            <li>Local and regional market penetration</li>
            <li>Corporate and government account development</li>
            <li>Group and meeting sales strategy</li>
            <li>Digital marketing, brand positioning, and online visibility</li>
          </ul>
          <h4>Food &amp; Beverage</h4>
          <p>Strategic oversight of all F&amp;B operations — menu development, purchasing and inventory controls, catering and banquet management, and operational performance analysis. We focus on group events, weddings, and local dining demand to strengthen the program and overall financial performance.</p>
          <h4>Facilities &amp; Engineering</h4>
          <ul class="spec-list">
            <li>Property maintenance &amp; preventative programs</li>
            <li>Property Improvement Plan (PIP) management</li>
            <li>Renovation and conversion project coordination</li>
            <li>Vendor and contractor management</li>
          </ul>
          <h4>Human Resources &amp; Training</h4>
          <p>Recruiting, onboarding, leadership development, payroll &amp; HR compliance, and retention programs — built around a service-focused culture that drives both employee engagement and guest satisfaction.</p>
          <h4>Information Technology</h4>
          <p>Property management systems, network infrastructure, reservation systems, and data security — properly integrated to streamline operations and support online bookings.</p>
        </div>
      </article>

      <article class="svc-card reveal" id="apartments">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-apartments.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Residential</p>
            <h3 class="card__title">Apartments &amp; Multi-Family</h3>
            <p class="card__desc">Long-term rentals across single- and multi-family properties — leasing, maintenance, tenant relations, and steady asset growth.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>We manage multifamily apartments, residential rentals, and condominiums with the same hands-on discipline we bring to our hotel portfolio. Our focus is on maintaining asset performance, tenant satisfaction, and operational efficiency.</p>
          <h4>What's included</h4>
          <ul class="spec-list">
            <li>Day-to-day operations and on-site staff oversight</li>
            <li>Leasing, tenant relations, and occupancy management</li>
            <li>Maintenance coordination and vendor management</li>
            <li>Financial reporting, budgeting, and cost control</li>
            <li>Capital improvements and project oversight</li>
            <li>Compliance with local and regulatory requirements</li>
          </ul>
        </div>
      </article>

      <article class="svc-card reveal" id="str">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-strrental.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Short-Term Rentals</p>
            <h3 class="card__title">Airbnb &amp; STR Operations</h3>
            <p class="card__desc">Furnished short-term and corporate rentals with hotel-grade standards — listing optimization, dynamic pricing, and guest support.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>We bring a hotel operator's playbook to short-term rentals — dynamic pricing, professional cleaning standards, and 24/7 guest response. Whether it's a single Airbnb unit or a portfolio of corporate-housing apartments, we maximize occupancy without sacrificing review scores.</p>
          <h4>What's included</h4>
          <ul class="spec-list">
            <li>Multi-channel listing setup (Airbnb, Vrbo, Booking.com, Furnished Finder)</li>
            <li>Dynamic pricing and revenue optimization</li>
            <li>Professional turnover cleaning and inventory restocking</li>
            <li>Guest screening, communication, and 24/7 support</li>
            <li>Maintenance dispatch and damage protection</li>
            <li>Monthly owner statements and tax-ready reporting</li>
          </ul>
        </div>
      </article>

      <article class="svc-card reveal" id="property-management">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-property.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Third-Party</p>
            <h3 class="card__title">Property Management</h3>
            <p class="card__desc">Full-service third-party management for hotel, residential, and commercial owners — we run it like we own it.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>SUNdhm provides full-service management for branded and non-branded hotels, multifamily apartments, residential rentals, condominiums, and short-term rental properties. Our approach is hands-on and detail-oriented, with an emphasis on maintaining property condition, improving performance, and aligning operations with ownership objectives.</p>
          <h4>Operations</h4>
          <ul class="spec-list">
            <li>Day-to-day operations and staff oversight</li>
            <li>Leasing, tenant relations, and occupancy management</li>
            <li>Maintenance coordination and vendor management</li>
            <li>Capital improvements and project oversight</li>
            <li>Compliance with brand, local, and regulatory requirements</li>
          </ul>
          <h4>Accounting &amp; Financial Reporting</h4>
          <p>Accounts payable, accounts receivable, payroll coordination, and monthly financial reporting. Detailed financial statements, operational reports, and performance analysis give owners clear visibility into revenue trends, expenses, and overall profitability.</p>
          <h4>Legal &amp; Finance</h4>
          <p>Budgeting, forecasting, financial reporting, and operational expense control — plus contract management, regulatory compliance, insurance coordination, and risk management to protect the interests of the property and its ownership group.</p>
        </div>
      </article>

      <article class="svc-card reveal" id="flipping">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-flip.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Development</p>
            <h3 class="card__title">House Flipping &amp; Development</h3>
            <p class="card__desc">We buy homes — any condition, any size — and reposition them. Cash offers, fast closings.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>Since SUNdhm's founding, we've taken a dynamic and entrepreneurial approach to acquiring real estate — whether operating hotels, purchasing hotels, or providing asset management services. As an owner of hospitality and residential real estate, we know the countless details that make a property successful, and we apply that same discipline to acquisitions.</p>
          <p>Market understanding, competition, demographic and economic trends, and analysis from each department within the organization are combined into our acquisition strategies.</p>
          <h4>We buy houses</h4>
          <ul class="spec-list">
            <li>Any look, any size, any condition</li>
            <li>Cash offers based on the deal</li>
            <li>Two-week closings, tops</li>
            <li>No agent fees, no repairs needed on your end</li>
          </ul>
          <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Sell%20My%20House%20to%20SUNdhm" style="color: var(--gold-text); font-weight: 700;">Email us about your property →</a></p>
        </div>
      </article>

      <article class="svc-card reveal" id="banquet">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-banquet.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Events</p>
            <h3 class="card__title">Banquet &amp; Catering</h3>
            <p class="card__desc">On-site banquet facilities and catering for weddings, corporate events, and private functions.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>Flexible event spaces and full-service catering at our hotels — built on the same operational discipline that runs our hotel F&amp;B programs.</p>
          <h4>What we host</h4>
          <ul class="spec-list">
            <li>Weddings &amp; receptions</li>
            <li>Corporate meetings, conferences, and training</li>
            <li>Holiday parties and private functions</li>
            <li>Group room blocks paired with on-site catering</li>
          </ul>
          <h4>Behind the scenes</h4>
          <ul class="spec-list">
            <li>Menu development with executive culinary teams</li>
            <li>Purchasing &amp; inventory controls for consistent margins</li>
            <li>On-site banquet management and event coordination</li>
          </ul>
        </div>
      </article>

      <article class="svc-card reveal" id="restoration">
        <button class="svc-card__head" type="button" aria-expanded="false">
          <div class="svc-card__media"><img src="./assets/images/service-property.jpg" alt="" loading="lazy" /></div>
          <div class="svc-card__intro">
            <p class="card__meta">Property Restoration &amp; Mitigation</p>
            <h3 class="card__title">Restoration Services</h3>
            <p class="card__desc">PuroClean of Syracuse North &mdash; 24/7 emergency property restoration for water damage, fire and smoke, mold remediation, and biohazard cleanup.</p>
            <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
          </div>
        </button>
        <div class="svc-card__detail">
          <p>Our family operates <strong>PuroClean of Syracuse North</strong>, a fully licensed and insured restoration franchise serving homeowners, businesses, property managers, and insurance carriers across the greater Syracuse region. Same operational discipline as our hospitality work — fast response, transparent communication, and clean execution.</p>
          <h4>Services</h4>
          <ul class="spec-list">
            <li><strong>Water damage restoration</strong> &mdash; burst pipes, flooding, sewage backups, storm damage</li>
            <li><strong>Fire &amp; smoke damage</strong> &mdash; structure cleanup, soot removal, odor neutralization, contents pack-out</li>
            <li><strong>Mold remediation</strong> &mdash; inspection, containment, removal, and post-remediation testing</li>
            <li><strong>Biohazard &amp; trauma cleanup</strong> &mdash; discreet, certified response for sensitive situations</li>
            <li><strong>Reconstruction support</strong> &mdash; coordination with contractors and adjusters through full property recovery</li>
          </ul>
          <h4>Why owners and adjusters call us</h4>
          <ul class="spec-list">
            <li>24/7 emergency response across Onondaga County and surrounding areas</li>
            <li>Direct insurance billing and adjuster-friendly documentation</li>
            <li>IICRC-certified technicians and PuroClean's national QA standards</li>
            <li>Local family-owned operation — you talk to a decision-maker, not a call center</li>
          </ul>
          <p style="margin-top: 16px;"><a href="https://www.purocleancny.com" target="_blank" rel="noopener" style="color: var(--gold-text); font-weight: 700;">Visit PuroClean of Syracuse North &rarr;</a></p>
        </div>
      </article>
    </div>

    <div class="reveal" style="margin: 56px 0 32px; text-align: center;">
      <p class="eyebrow">Special Situations</p>
      <h2 class="serif" style="margin-top: 12px;">When a property needs a steady hand.</h2>
      <p class="lead" style="max-width: 640px; margin: 16px auto 0;">Specialized engagements for lenders, courts, and owners under pressure.</p>
    </div>

    <article class="svc-card svc-card--wide reveal" id="receivership">
      <button class="svc-card__head" type="button" aria-expanded="false">
        <div class="svc-card__intro svc-card__intro--wide">
          <p class="card__meta">Distressed Assets — For Banks &amp; Lenders</p>
          <h3 class="card__title" style="font-size: 28px;">Receivership &amp; Special-Asset Management</h3>
          <p class="card__desc"><strong>SUNdhm is a New York State approved receiver and property manager.</strong> Court-appointed and lender-engaged receivership for distressed hospitality, multi-family, and commercial assets across New York State. We take possession quickly, secure the property, restore financial controls, stabilize operations, and report transparently to the court and to you.</p>
          <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
        </div>
        <div class="svc-card__shield">
          <svg viewBox="0 0 80 80" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M40 8L12 22v18c0 16 12 30 28 38 16-8 28-22 28-38V22L40 8z M30 40l7 7 14-17"/></svg>
        </div>
      </button>
      <div class="svc-card__detail">
        <p><strong>SUNdhm is approved by New York State as a receiver and property manager.</strong> When a hospitality, multi-family, or commercial asset is in distress, lenders and courts engage SUNdhm to take control quickly, secure the property, restore financial discipline, and protect collateral value. We've been on the operating side of distressed assets for decades — we know what to look for and how to fix it.</p>
        <h4>What we do as receiver</h4>
        <ul class="spec-list">
          <li>Take immediate possession and secure the property</li>
          <li>Stabilize operations, payroll, and vendor relationships</li>
          <li>Restore financial controls and clean up books</li>
          <li>Implement cash management and reporting protocols</li>
          <li>Court-ready monthly reporting and lender updates</li>
          <li>Coordinate with counsel, brokers, and special servicers</li>
          <li>Sale, disposition, and turnover support</li>
        </ul>
        <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Receivership%20Engagement%20Inquiry" style="color: var(--gold-text); font-weight: 700;">Inquire about a receivership engagement →</a></p>
      </div>
    </article>

    <article class="svc-card svc-card--wide reveal" id="mortgage-disputes" style="margin-top: 24px;">
      <button class="svc-card__head" type="button" aria-expanded="false">
        <div class="svc-card__intro svc-card__intro--wide">
          <p class="card__meta">Owner Advocacy — For Owners Under Pressure</p>
          <h3 class="card__title" style="font-size: 28px;">Mortgage Dispute &amp; Workout Guidance</h3>
          <p class="card__desc">Hands-on experience navigating mortgage disputes, workouts, and lender negotiations — we've been through it ourselves and we use that experience to guide other property owners through the same situations.</p>
          <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
        </div>
        <div class="svc-card__shield">
          <svg viewBox="0 0 80 80" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M16 32h48v32H16z M24 32V20a16 16 0 0 1 32 0v12 M40 44v8"/></svg>
        </div>
      </button>
      <div class="svc-card__detail">
        <p>If your hotel, apartment building, or commercial property is under lender pressure, we can help. SUNdhm has lived through mortgage disputes from the owner's side — restructurings, forbearance, default notices, special-asset transitions — and we use that experience to guide other property owners through the same situations.</p>
        <p><em>We are not attorneys and we are not a substitute for legal counsel. We're operators who know how lenders and special servicers think, what they need to see, and how to put a credible operating plan in front of them.</em></p>
        <h4>How we help owners</h4>
        <ul class="spec-list">
          <li>Translate lender notices and term sheets into plain English</li>
          <li>Prepare credible operating plans, budgets, and turnaround narratives</li>
          <li>Coordinate with counsel, accountants, and lenders on your behalf</li>
          <li>Stabilize operations during workout or forbearance periods</li>
          <li>Quietly market or refinance when that's the right path</li>
          <li>Step in as a manager or receiver if the situation calls for it</li>
        </ul>
        <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Mortgage%20Dispute%20Help%20%E2%80%94%20Confidential" style="color: var(--gold-text); font-weight: 700;">Email a confidential summary →</a></p>
      </div>
    </article>
  </div>
</section>

<section class="section" id="case-studies" style="background: var(--cream);">
  <div class="container">
    <div class="reveal" style="max-width: 760px; margin-bottom: 36px;">
      <p class="eyebrow">Case Studies</p>
      <h2 class="serif" style="margin-top: 12px;">Engagement snapshots.</h2>
      <p class="lead" style="margin-top: 16px;">Representative engagements illustrating how SUNdhm operates across lender mandates, owner-retained management, and pre-foreclosure resolutions. Specific borrower, lender, brand, and asset identifiers have been generalized.</p>
    </div>

    <div class="grid grid-3 case-grid">

      <a class="case-card case-card--link reveal" href="./case-lender.html">
        <div class="case-card__num">01</div>
        <p class="card__meta">Lender Engagement</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">~80 keys · Regional bank, conventional CRE loan</p>
        <p class="case-card__body">Lender-engaged operating oversight after borrower default. Restored reporting transparency, stabilized cash flow, and protected collateral value through the workout period.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-property-management.html">
        <div class="case-card__num">02</div>
        <p class="card__meta">Property Management</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">Owner-retained third-party management</p>
        <p class="case-card__body">Owner engaged SUNdhm under a third-party management agreement to professionalize operations. Day-to-day management, brand compliance, revenue management, and transparent monthly reporting.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-resolution.html">
        <div class="case-card__num">03</div>
        <p class="card__meta">Borrower &amp; Lender Resolution</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">Regional bank · pre-foreclosure workout</p>
        <p class="case-card__body">Neutral operator and resolution partner during foreclosure proceedings. Foreclosure discontinued, loan returned to performing status, and the borrower retained ownership.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-mixed-use.html">
        <div class="case-card__num">04</div>
        <p class="card__meta">Mixed-Use Restoration</p>
        <h3 class="case-card__title">Mixed-Use Commercial — Upstate New York</h3>
        <p class="case-card__sub">22 units &middot; 3 retail bays &middot; ~4 years vacant</p>
        <p class="case-card__body">Operating takeover of an abandoned mixed-use building. Life-safety re-certified, original character preserved, stabilized run-rate in 12 months.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-house-flip.html">
        <div class="case-card__num">05</div>
        <p class="card__meta">House Flip</p>
        <h3 class="case-card__title">Single-Family Residential — Upstate New York</h3>
        <p class="case-card__sub">3 bed &middot; 2.5 bath &middot; 0.80 acres</p>
        <p class="case-card__body">Distressed acquisition, full renovation, retail resale. $102.8K all-in to $229K sale &mdash; ~123% gross ROI on cost.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

    </div>

    <p class="case-disclaimer">Representative engagement profiles. Specific borrower, lender, brand, and asset identifiers have been generalized. Figures are illustrative of typical engagement performance and do not reflect any single client. SUNdhm is a New York State approved receiver and property manager.</p>

    <div style="margin-top: 28px;">
      <a class="btn btn--gold" href="./case-studies.html">View all case studies <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
    </div>
  </div>
</section>
'''

# ============ HIRE US PAGE ============
HIRE_BODY = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Hire SUNdhm</p>
    <h1 class="serif">Trusted by lenders. Chosen by owners.</h1>
    <p class="lead" style="max-width: 760px; margin-top: 16px;">For more than 30 years, banks, special servicers, and individual property owners have hired SUNdhm to step in, stabilize operations, and protect asset value. Whether you need a court-appointed receiver, a hands-on property manager, or guidance through a mortgage workout — we're ready to take the call.</p>
  </div>
</section>

<section class="section section--soft" id="hire-us">
  <div class="container">
    <div class="grid grid-2">
      <article class="hire-card reveal">
        <div class="hire-card__icon">
          <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 18h36 M10 18v22 M38 18v22 M14 18v22 M34 18v22 M22 18v22 M26 18v22 M4 42h40 M24 4l20 14H4L24 4z"/></svg>
        </div>
        <p class="card__meta">For Banks &amp; Lenders</p>
        <h3 class="card__title" style="font-size: 26px;">Receivership &amp; Special-Asset Management</h3>
        <p class="card__desc">Court-appointed and lender-engaged receivership for distressed hospitality, multi-family, and commercial assets across New York State. We take possession quickly, secure the property, restore financial controls, stabilize operations, and report transparently to the court and to you.</p>
        <h4 class="hire-card__h4">What we do</h4>
        <ul class="spec-list">
          <li>Take immediate possession and secure the property</li>
          <li>Stabilize operations, payroll, and vendor relationships</li>
          <li>Restore financial controls and clean up books</li>
          <li>Implement cash management and reporting protocols</li>
          <li>Court-ready monthly reporting and lender updates</li>
          <li>Coordinate with counsel, brokers, and special servicers</li>
          <li>Sale, disposition, and turnover support</li>
        </ul>
        <a class="btn btn--gold" href="mailto:hello@sundhm.com?subject=Receivership%20Engagement%20Inquiry" style="margin-top: 28px;">Engage SUNdhm <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </article>

      <article class="hire-card reveal">
        <div class="hire-card__icon">
          <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 42h36 M10 42V18l14-8 14 8v24 M18 42V28h12v14 M14 22h4 M30 22h4 M14 30h4"/></svg>
        </div>
        <p class="card__meta">For Property Owners</p>
        <h3 class="card__title" style="font-size: 26px;">Third-Party Property Management</h3>
        <p class="card__desc">Own a hotel, apartment building, short-term rental, or mixed-use property and tired of managing it yourself? We run it like we own it — full-service operations, transparent monthly reporting, and a single point of contact you can actually reach.</p>
        <h4 class="hire-card__h4">Asset types we manage</h4>
        <ul class="spec-list">
          <li>Hotels — branded &amp; independent</li>
          <li>Apartments &amp; multi-family rentals</li>
          <li>Short-term rentals (Airbnb, Vrbo, corporate)</li>
          <li>Banquet venues &amp; small commercial</li>
          <li>Monthly P&amp;L, leasing, maintenance, vendor oversight</li>
        </ul>
        <a class="btn btn--gold" href="mailto:hello@sundhm.com?subject=Property%20Management%20Inquiry" style="margin-top: 28px;">Request a proposal <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </article>
    </div>

    <article class="hire-card reveal" style="margin-top: 32px;">
      <div class="hire-card__icon">
        <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 18h28v22H10z M14 18V12a10 10 0 0 1 20 0v6 M24 26v6"/></svg>
      </div>
      <p class="card__meta">For Owners Under Pressure</p>
      <h3 class="card__title" style="font-size: 26px;">Mortgage Dispute &amp; Workout Guidance</h3>
      <p class="card__desc">If your hotel, apartment building, or commercial property is under lender pressure, we can help. SUNdhm has lived through mortgage disputes from the owner's side — restructurings, forbearance, default notices, special-asset transitions — and we use that experience to guide other property owners through the same situations.</p>
      <p style="margin-top: 12px; font-size: 14px; color: var(--ink-soft);"><em>We are not attorneys and we are not a substitute for legal counsel. We're operators who know how lenders and special servicers think, what they need to see, and how to put a credible operating plan in front of them.</em></p>
      <h4 class="hire-card__h4">How we help owners</h4>
      <ul class="spec-list">
        <li>Translate lender notices and term sheets into plain English</li>
        <li>Prepare credible operating plans, budgets, and turnaround narratives</li>
        <li>Coordinate with counsel, accountants, and lenders on your behalf</li>
        <li>Stabilize operations during workout or forbearance periods</li>
        <li>Quietly market or refinance when that's the right path</li>
        <li>Step in as a manager or receiver if the situation calls for it</li>
      </ul>
      <a class="btn btn--gold" href="mailto:hello@sundhm.com?subject=Mortgage%20Dispute%20Help%20%E2%80%94%20Confidential" style="margin-top: 28px;">Email a confidential summary <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
    </article>

    <div class="reveal hire-cta">
      <p>Have an asset that needs immediate attention? Call <a href="tel:+13157520155">(315) 752-0155</a> or email <a href="mailto:hello@sundhm.com">hello@sundhm.com</a> — we respond same day.</p>
    </div>
  </div>
</section>
'''

# ============ CAREERS PAGE ============
CAREERS_BODY = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Careers</p>
    <h1 class="serif">Build your career with a hands-on operator.</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">We're always looking for great people — front desk, housekeeping, maintenance, sales, and management — across our hotel and hospitality properties.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <h2 class="serif" style="margin-bottom: 20px;">Why work with SUNdhm</h2>
        <p class="lead">We're a family-owned operator — decisions get made fast, your work matters, and your manager isn't five layers up at a corporate office in another state.</p>
        <p style="margin-top: 16px;">It is SUNdhm Management's objective to hire the best professionals for all its properties. Once a property is under management, SUNdhm searches for talented people who are the best match for the opportunities at the property. Through SUNdhm University and ongoing training, we encourage employees to gain or maintain certifications within their communities, hospitality network, or the brand they represent.</p>
      </div>
      <div class="reveal" style="background: var(--cream); border-radius: var(--radius-lg); padding: 40px;">
        <h3 class="serif" style="font-size: 24px; margin-bottom: 16px;">What we look for</h3>
        <ul class="spec-list">
          <li>Genuine hospitality — guest-first attitude</li>
          <li>Reliability and ownership of the work</li>
          <li>Comfort with modern PMS &amp; OTA systems</li>
          <li>Team players who lift each other up</li>
        </ul>
        <h3 class="serif" style="font-size: 24px; margin: 28px 0 16px;">Roles we hire for</h3>
        <ul class="spec-list">
          <li>Front desk &amp; guest services</li>
          <li>Housekeeping &amp; laundry</li>
          <li>Maintenance &amp; engineering</li>
          <li>Sales &amp; revenue</li>
          <li>General management</li>
          <li>Banquet &amp; catering</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft" id="apply">
  <div class="container" style="max-width: 820px;">
    <div class="reveal" style="text-align: center; margin-bottom: 40px;">
      <p class="eyebrow">Apply now</p>
      <h2 class="serif" style="margin-top: 12px;">Apply for a position</h2>
      <p class="lead" style="margin-top: 16px;">Tell us about yourself and attach a résumé — we read every application and respond personally.</p>
    </div>

    <form class="apply-form reveal" id="applyForm" action="https://formsubmit.co/hello@sundhm.com" method="POST" enctype="multipart/form-data" novalidate>
      <input type="hidden" name="_subject" value="New job application — SUNdhm careers" />
      <input type="hidden" name="_template" value="table" />
      <input type="hidden" name="_captcha" value="true" />
      <input type="hidden" name="_next" value="https://www.sundhm.com/careers.html?submitted=1" />
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" />

      <div class="form-grid">
        <label class="form-field">
          <span class="form-label">First name <span aria-hidden="true" style="color:var(--gold-deep)">*</span></span>
          <input type="text" name="First Name" required autocomplete="given-name" />
        </label>
        <label class="form-field">
          <span class="form-label">Last name <span aria-hidden="true" style="color:var(--gold-deep)">*</span></span>
          <input type="text" name="Last Name" required autocomplete="family-name" />
        </label>
        <label class="form-field">
          <span class="form-label">Email <span aria-hidden="true" style="color:var(--gold-deep)">*</span></span>
          <input type="email" name="Email" required autocomplete="email" />
        </label>
        <label class="form-field">
          <span class="form-label">Phone <span aria-hidden="true" style="color:var(--gold-deep)">*</span></span>
          <input type="tel" name="Phone" required autocomplete="tel" placeholder="(315) 555-0123" />
        </label>
        <label class="form-field form-field--full">
          <span class="form-label">City / town</span>
          <input type="text" name="City" autocomplete="address-level2" />
        </label>
        <label class="form-field">
          <span class="form-label">Position you're applying for <span aria-hidden="true" style="color:var(--gold-deep)">*</span></span>
          <select name="Position" required>
            <option value="">Select a role…</option>
            <option>Front Desk / Guest Services</option>
            <option>Housekeeping</option>
            <option>Maintenance / Engineering</option>
            <option>Sales &amp; Revenue</option>
            <option>General Manager</option>
            <option>Assistant Manager</option>
            <option>Banquet / Catering</option>
            <option>Corporate / Accounting</option>
            <option>Other (note in message)</option>
          </select>
        </label>
        <label class="form-field">
          <span class="form-label">Earliest start date</span>
          <input type="date" name="Start Date" />
        </label>
        <label class="form-field form-field--full">
          <span class="form-label">Years of relevant experience</span>
          <select name="Experience">
            <option value="">Select…</option>
            <option>None — willing to learn</option>
            <option>Less than 1 year</option>
            <option>1–3 years</option>
            <option>3–5 years</option>
            <option>5–10 years</option>
            <option>10+ years</option>
          </select>
        </label>
        <label class="form-field form-field--full">
          <span class="form-label">Tell us about yourself</span>
          <textarea name="Message" rows="5" placeholder="Briefly: where you've worked, what you're looking for, what hours you can do, and anything else we should know."></textarea>
        </label>
        <div class="form-field form-field--full">
          <span class="form-label">Résumé (PDF, DOC, or DOCX)</span>
          <label class="file-drop" id="fileDrop">
            <input type="file" name="Resume" accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" id="fileInput" />
            <span class="file-drop__text" id="fileText">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
              <span>Choose a file or drag it here</span>
            </span>
          </label>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn--gold">Submit application <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
        <p class="form-note">Or email a résumé directly to <a href="mailto:hello@sundhm.com?subject=Careers%20at%20SUNdhm">hello@sundhm.com</a>. We respond within one business day.</p>
      </div>
    </form>

    <div class="applicant-notice reveal" id="applicant-notice">
      <h3 class="serif">Equal Opportunity &amp; Applicant Notice</h3>
      <p><strong>Equal opportunity employer.</strong> SUNdhm is an equal opportunity employer. We consider all qualified applicants without regard to race, color, religion, sex (including pregnancy, sexual orientation, or gender identity), national origin, age, disability, genetic information, marital status, military or veteran status, citizenship, or any other status protected by federal, New York State, or local law. We comply with the New York State Human Rights Law and the New York City Human Rights Law where applicable.</p>
      <p><strong>Reasonable accommodations.</strong> If you need an accommodation to apply or to participate in our hiring process, contact <a href="mailto:hello@sundhm.com?subject=Hiring%20Accommodation%20Request">hello@sundhm.com</a> and we will work with you.</p>
      <p><strong>Pay transparency.</strong> Where required by law, we include a good-faith pay range in each job posting.</p>
      <h4 style="margin-top: 22px;">How we handle your application data</h4>
      <ul class="spec-list">
        <li><strong>What we collect:</strong> the information you submit on this form (name, contact details, position of interest, work authorization status, message, and résumé), plus any references or background-check results we obtain with your authorization later in the process.</li>
        <li><strong>How we use it:</strong> only to evaluate you for employment, communicate with you about the role, and meet legal/recordkeeping obligations. We do not sell applicant data and do not use it for advertising.</li>
        <li><strong>Who sees it:</strong> SUNdhm hiring staff, and service providers (email, form processor, background-check vendors if applicable) under contract.</li>
        <li><strong>How long we keep it:</strong> typically up to 2 years after your application, then we delete or de-identify it, unless a longer period is required by law.</li>
        <li><strong>Your rights:</strong> you may request access, correction, or deletion of your applicant data at any time by emailing <a href="mailto:privacy@sundhm.com?subject=Applicant%20Privacy%20Request">privacy@sundhm.com</a>. See our <a href="./privacy.html">Privacy Policy</a> for details.</li>
        <li><strong>California residents:</strong> additional rights apply under the CCPA/CPRA, including the right to know, correct, delete, and limit the use of sensitive information. Submit a request at <a href="./privacy.html#privacy-requests">privacy requests</a>.</li>
      </ul>
      <p style="font-size: 13px; color: var(--ink-soft); margin-top: 14px;">Please do not include sensitive personal information (such as Social Security number, driver's license, or financial account numbers) in this form. We will request that information through a secure channel only if and when it becomes necessary later in the process.</p>
    </div>

    <div id="applySuccess" class="apply-success" hidden>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="40" height="40"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/></svg>
      <h3 class="serif">Thanks — we got it.</h3>
      <p>Your application has been received. We read every one personally and will be in touch within one business day.</p>
    </div>
  </div>
</section>

<script>
  (function() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('submitted') === '1') {
      const form = document.getElementById('applyForm');
      const success = document.getElementById('applySuccess');
      if (form) form.style.display = 'none';
      if (success) {
        success.hidden = false;
        success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
    const input = document.getElementById('fileInput');
    const text = document.getElementById('fileText');
    const drop = document.getElementById('fileDrop');
    if (input && text && drop) {
      input.addEventListener('change', () => {
        const f = input.files && input.files[0];
        if (f) {
          text.querySelector('span').textContent = f.name + '  (' + Math.round(f.size/1024) + ' KB)';
          drop.classList.add('has-file');
        }
      });
      ['dragenter','dragover'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add('is-drag'); }));
      ['dragleave','drop'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove('is-drag'); }));
      drop.addEventListener('drop', e => {
        const f = e.dataTransfer.files && e.dataTransfer.files[0];
        if (f) { input.files = e.dataTransfer.files; input.dispatchEvent(new Event('change')); }
      });
    }
  })();
</script>
'''

# ============ CONTACT PAGE ============
CONTACT_BODY = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Get in touch</p>
    <h1 class="serif">Let's talk.</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">Questions about a property, a partnership, a receivership engagement, or a job? We'd love to hear from you. Same-day response on calls and emails during business hours.</p>
  </div>
</section>

<section class="section section--navy-deep" id="contact">
  <div class="container">
    <div class="grid grid-2">
      <div class="reveal">
        <h2 class="serif" style="color: #fff;">Reach SUNdhm</h2>
        <p class="lead" style="color: rgba(255,255,255,.85); margin-top: 16px;">Office hours Monday–Friday. After-hours engagements for lenders and receivership matters by phone.</p>
        <div class="contact-card" style="margin-top: 32px;">
          <div class="contact-row">
            <div class="contact-row__label">Office</div>
            <div class="contact-row__value">
              250 Commerce Blvd<br/>
              Liverpool, NY 13088
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__label">Mailing</div>
            <div class="contact-row__value">
              PO BOX 3590<br/>
              Syracuse, NY 13220
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__label">Phone</div>
            <div class="contact-row__value"><a href="tel:+13157520155">(315) 752-0155</a></div>
          </div>
          <div class="contact-row">
            <div class="contact-row__label">Sales</div>
            <div class="contact-row__value"><a href="tel:+13157157410">(315) 715-7410</a></div>
          </div>
          <div class="contact-row">
            <div class="contact-row__label">Email</div>
            <div class="contact-row__value"><a href="mailto:hello@sundhm.com">hello@sundhm.com</a></div>
          </div>
        </div>
      </div>
      <div class="reveal">
        <div class="contact-map">
          <iframe
            src="https://www.google.com/maps?q=250+Commerce+Blvd,+Liverpool,+NY+13088&output=embed"
            width="100%" height="100%" style="border:0; min-height: 400px; border-radius: var(--radius-lg);"
            allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            title="SUNdhm office location"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
'''


# ============ CASE STUDY PAGES ============

CASE_HERO_TEMPLATE = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow"><a href="./case-studies.html" style="color: inherit; text-decoration: none;">← Case Studies</a></p>
    <h1 class="serif">{title}</h1>
    <p class="lead" style="max-width: 760px; margin-top: 16px;">{lead}</p>
  </div>
</section>
'''

CASE_FOOTER = '''
<section class="section section--soft">
  <div class="container" style="max-width: 820px;">
    <p class="case-disclaimer" style="margin: 0 0 32px;">Representative engagement profile. Specific borrower, lender, brand, and asset identifiers have been generalized. Figures are illustrative of typical engagement performance and do not reflect any single client. SUNdhm is a New York State approved receiver and property manager.</p>
    <div class="grid grid-2" style="gap: 16px;">
      <a class="btn btn--gold" href="./contact.html">Discuss a similar engagement <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      <a class="btn btn--ghost" href="./case-studies.html">Back to all case studies</a>
    </div>
  </div>
</section>
'''

CASE_LENDER_BODY = CASE_HERO_TEMPLATE.format(
    title="Lender-Engaged Operating Oversight",
    lead="After borrower default and a filed foreclosure action, a regional bank engaged SUNdhm to take independent operating oversight of a limited-service hotel — restoring reporting transparency, stabilizing cash flow, and protecting collateral value through the workout period."
) + '''
<section class="section">
  <div class="container" style="max-width: 820px;">

    <div class="case-detail__grid">
      <div class="case-detail__meta-block">
        <p class="card__meta">Asset Type</p>
        <p class="case-detail__meta-val">Limited-Service Hotel — New York</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Approx. Keys</p>
        <p class="case-detail__meta-val">~80</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Lender Profile</p>
        <p class="case-detail__meta-val">Regional bank, conventional CRE loan</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">SUNdhm Role</p>
        <p class="case-detail__meta-val">Lender-introduced operator &amp; workout advisor</p>
      </div>
    </div>

    <h2 class="serif case-detail__h2">Situation at Engagement</h2>
    <p>The borrower had fallen materially behind on debt service and the lender had initiated foreclosure proceedings on a stabilized-but-underperforming limited-service hotel. Operations were drifting: reservations leakage, payroll creep, inconsistent franchise compliance, and incomplete monthly reporting made it difficult for the lender to assess collateral value or chart a workout path.</p>
    <p>SUNdhm was retained directly by the lender to step in as the operating party of record, stabilize the asset on a defined timeline, and produce the financial and operational transparency required for the bank to weigh resolution options — cure, sale, deed-in-lieu, or judicial foreclosure.</p>

    <h2 class="serif case-detail__h2">Strategic Interventions</h2>
    <ul class="spec-list">
      <li><strong>Operating control &amp; cash management.</strong> Took possession of day-to-day operations, established a clean operating bank account with controlled disbursements, and rebuilt a defensible weekly cash forecast for the lender.</li>
      <li><strong>Revenue management reset.</strong> Re-platformed rate strategy, OTA distribution, and brand-channel positioning. Tightened length-of-stay and segment controls; reopened distressed channels with corrected content.</li>
      <li><strong>Payroll &amp; expense discipline.</strong> Right-sized labor schedules to occupancy, renegotiated key vendor terms, and eliminated non-essential overhead inherited from the prior operator.</li>
      <li><strong>Franchise &amp; compliance cleanup.</strong> Closed open brand-compliance items, restored loyalty-program standing, and brought guest scores back into acceptable bands.</li>
      <li><strong>Lender reporting cadence.</strong> Delivered monthly P&amp;L, STR/competitive set commentary, and a capex/working-capital outlook in a format underwriting and special-assets teams could action.</li>
    </ul>

    <h2 class="serif case-detail__h2">Results at Stabilization</h2>
    <ul class="case-card__metrics" style="margin-top: 8px;">
      <li><strong>Occupancy:</strong> 38% → 61%</li>
      <li><strong>ADR:</strong> $72 → $98</li>
      <li><strong>Payroll:</strong> 38% → 24% of revenue</li>
      <li><strong>Stabilization Timeline:</strong> ~9 months</li>
    </ul>

    <h2 class="serif case-detail__h2">Outcome</h2>
    <p>Performing cash flow was restored, collateral value was protected, and the lender held a stabilized asset with audit-grade reporting and a clear set of resolution options. SUNdhm continued in an operating-of-record capacity through the resolution process, coordinating with counsel, special servicing, and prospective transaction parties as required.</p>

    <h2 class="serif case-detail__h2">Relevance to Distressed &amp; Transitional Assets</h2>
    <p>This engagement illustrates a pattern SUNdhm sees repeatedly with regional bank and special-servicer portfolios: hospitality and mixed-use assets where the underlying property is fundamentally viable, but operating drift, weak reporting, and franchise erosion have created the appearance of a deeper problem. Hands-on operating control, disciplined financial reporting, and brand-compliance recovery typically reveal that the asset is recoverable on a 6–12 month horizon.</p>

  </div>
</section>
''' + CASE_FOOTER

CASE_PM_BODY = CASE_HERO_TEMPLATE.format(
    title="Third-Party Property Management",
    lead="A hotel owner engaged SUNdhm under a third-party management agreement to professionalize operations after a period of underperformance — day-to-day operations, brand compliance, revenue management, and transparent monthly reporting back to ownership."
) + '''
<section class="section">
  <div class="container" style="max-width: 820px;">

    <div class="case-detail__grid">
      <div class="case-detail__meta-block">
        <p class="card__meta">Asset Type</p>
        <p class="case-detail__meta-val">Limited-Service Hotel — New York</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Engagement</p>
        <p class="case-detail__meta-val">Owner-retained third-party management</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Brand</p>
        <p class="case-detail__meta-val">National franchise system</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">SUNdhm Role</p>
        <p class="case-detail__meta-val">Third-party hotel management on behalf of owner</p>
      </div>
    </div>

    <h2 class="serif case-detail__h2">Situation at Engagement</h2>
    <p>The owner had operated the property through a mix of in-house management and prior third-party engagements that had not delivered consistent results. Topline was soft against the competitive set, payroll was high as a percentage of revenue, brand compliance items were accumulating, and ownership lacked clear visibility into where dollars were leaking. The owner wanted to retain the asset — not sell it — and needed a professional operating partner who would treat the property like an owned one.</p>

    <h2 class="serif case-detail__h2">Strategic Interventions</h2>
    <ul class="spec-list">
      <li><strong>Operating takeover.</strong> Assumed full day-to-day management responsibility: front office, housekeeping, maintenance, brand audits, guest experience, and team leadership.</li>
      <li><strong>Revenue management.</strong> Rebuilt pricing strategy across brand.com, OTA, GDS, and direct channels. Implemented disciplined yield management around demand events, length-of-stay controls, and segment mix.</li>
      <li><strong>Cost structure reset.</strong> Re-engineered labor schedules to demand, retendered key recurring contracts, and tightened controllable expenses without compromising brand standards.</li>
      <li><strong>Franchise &amp; brand compliance.</strong> Closed open brand-compliance items, restored loyalty-program standing, and rebuilt guest-satisfaction scores into the acceptable band for the flag.</li>
      <li><strong>Owner reporting.</strong> Established monthly P&amp;L, daily revenue updates, and a KPI dashboard delivered directly to ownership, so they could see how the asset was performing in real time.</li>
    </ul>

    <h2 class="serif case-detail__h2">Results</h2>
    <ul class="case-card__metrics" style="margin-top: 8px;">
      <li><strong>Occupancy:</strong> low 40s → mid 60s</li>
      <li><strong>ADR:</strong> repositioned within competitive set (~+30%)</li>
      <li><strong>Payroll ratio:</strong> reduced ~10 percentage points</li>
      <li><strong>Reporting:</strong> Monthly P&amp;L, daily revenue, KPI dashboards to ownership</li>
    </ul>

    <h2 class="serif case-detail__h2">Outcome</h2>
    <p>NOI growth, restored brand compliance, and asset-level cash flow sufficient to support refinance and reinvestment decisions. Ownership now operates with a clear monthly read on the asset and a single point of accountability for every operating decision.</p>

    <h2 class="serif case-detail__h2">Relevance to Owner-Operators</h2>
    <p>This engagement reflects what SUNdhm does for owners who want to keep an asset but no longer want to run it themselves — or who have outgrown the operator they had. We treat third-party assignments like owned properties: hands-on management, sharp financial controls, modern revenue and digital marketing, and the transparent reporting an owner deserves.</p>

  </div>
</section>
''' + CASE_FOOTER

CASE_RESOLUTION_BODY = CASE_HERO_TEMPLATE.format(
    title="Borrower &amp; Lender Resolution",
    lead="With foreclosure proceedings underway and the borrower committed to retaining the asset, SUNdhm was engaged as a neutral operator and resolution partner — restoring transparent reporting and working alongside counsel on a structured cure. Foreclosure was discontinued and the borrower retained ownership."
) + '''
<section class="section">
  <div class="container" style="max-width: 820px;">

    <div class="case-detail__grid">
      <div class="case-detail__meta-block">
        <p class="card__meta">Asset Type</p>
        <p class="case-detail__meta-val">Limited-Service Hotel — New York</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Lender Profile</p>
        <p class="case-detail__meta-val">Regional bank · pre-foreclosure</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Borrower Intent</p>
        <p class="case-detail__meta-val">Retain ownership of the asset</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">SUNdhm Role</p>
        <p class="case-detail__meta-val">Interim operator &amp; workout facilitator</p>
      </div>
    </div>

    <h2 class="serif case-detail__h2">Situation at Engagement</h2>
    <p>The lender had filed foreclosure on a limited-service hotel after repeated debt-service shortfalls, accumulated default interest, and unpaid legal fees. The borrower wanted to retain the asset but had lost operational and reporting credibility with the bank. The situation needed a neutral, capable operator who could stand in front of the lender, take operating control, and demonstrate a credible cure path — fast enough to halt the foreclosure clock.</p>

    <h2 class="serif case-detail__h2">Strategic Interventions</h2>
    <ul class="spec-list">
      <li><strong>Interim operating control.</strong> SUNdhm took operating control of the property and the operating account on terms acceptable to both borrower and lender, providing the bank with a known, accountable operator of record.</li>
      <li><strong>Reporting restoration.</strong> Stood up monthly P&amp;L, weekly cash forecast, and operational KPIs in a format the special-assets group could act on. Closed the reporting gap that had eroded lender confidence.</li>
      <li><strong>Operational stabilization.</strong> Reset revenue management, tightened payroll and controllable expenses, restored brand and franchise compliance, and brought guest-satisfaction scores back into acceptable bands.</li>
      <li><strong>Structured cure with counsel.</strong> Worked with borrower’s counsel and the lender’s workout team on a structured cure that addressed arrears, default interest, and legal fees on a defined schedule.</li>
      <li><strong>Continuous lender communication.</strong> Maintained a transparent line of communication with the bank throughout, so that every operating and financial decision was visible.</li>
    </ul>

    <h2 class="serif case-detail__h2">Results at Exit</h2>
    <ul class="case-card__metrics" style="margin-top: 8px;">
      <li><strong>Action:</strong> Foreclosure discontinued</li>
      <li><strong>Loan:</strong> Returned to performing status</li>
      <li><strong>Arrears, default interest, legal fees:</strong> Cured</li>
      <li><strong>Borrower:</strong> Retained ownership of the property</li>
    </ul>

    <h2 class="serif case-detail__h2">Outcome</h2>
    <p>The foreclosure action was discontinued, the loan was returned to performing status, and the borrower retained ownership of the property. The lender ended the engagement with a performing loan against a stabilized asset and a documented record of how stabilization was achieved.</p>

    <h2 class="serif case-detail__h2">Relevance to Distressed &amp; Transitional Assets</h2>
    <p>This engagement illustrates an outcome that is often available when a borrower has genuine intent and capacity to retain an asset, but has lost operating and reporting credibility with the lender. With a neutral operator restoring control, transparency, and performance, foreclosure is frequently not the only path — and often not the best one for either side.</p>

  </div>
</section>
''' + CASE_FOOTER

# Structured case study — abandoned mixed-use commercial restoration
CASE_MIXED_USE_BODY = CASE_HERO_TEMPLATE.format(
    title="Abandoned Mixed-Use Commercial Restoration",
    lead="Operating takeover of a long-vacant mixed-use building. 22 apartments, 3 retail bays. Stabilized run-rate inside 12 months."
) + '''
<section class="section">
  <div class="container" style="max-width: 820px;">

    <div class="case-detail__grid">
      <div class="case-detail__meta-block">
        <p class="card__meta">Asset Type</p>
        <p class="case-detail__meta-val">Mixed-Use Commercial — Upstate New York</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Configuration</p>
        <p class="case-detail__meta-val">22 residential units &middot; 3 retail bays</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Condition at Takeover</p>
        <p class="case-detail__meta-val">~4 years vacant &middot; fully shuttered</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">SUNdhm Role</p>
        <p class="case-detail__meta-val">Operating takeover, restoration &amp; lease-up</p>
      </div>
    </div>

    <h2 class="serif case-detail__h2">Situation</h2>
    <p>Mixed-use building, fully vacant for about four years. Storefronts papered over, apartments empty, life-safety items expired, boiler dead. Shell was sound — roof, masonry, and most original details intact.</p>

    <h2 class="serif case-detail__h2">Strategic Interventions</h2>
    <ul class="spec-list">
      <li><strong>Life-safety re-certified.</strong> Fire panel, sprinkler riser, smoke &amp; CO across all floors.</li>
      <li><strong>Mechanicals restored.</strong> New boiler, risers pressure-tested, roof flashing, third-floor water damage remediated.</li>
      <li><strong>Residential restored, not gutted.</strong> Original casings, plaster, and pine floors preserved in 18 of 22 units.</li>
      <li><strong>Commercial leased.</strong> Corner bay to an F&amp;B operator; secondary bay to a service tenant; third bay held strategic.</li>
      <li><strong>Lease-up program.</strong> Mid-market positioning, model unit, marketing relaunch. First move-in at ~240 days.</li>
      <li><strong>Owner reporting.</strong> Monthly P&amp;L, rent roll, capex, and KPI dashboard from day one.</li>
    </ul>

    <h2 class="serif case-detail__h2">Results at One Year</h2>
    <ul class="case-card__metrics" style="margin-top: 8px;">
      <li><strong>Residential occupancy:</strong> 0% → 73%</li>
      <li><strong>Commercial occupancy:</strong> 0% → 67%</li>
      <li><strong>EGI:</strong> $0 → stabilized run-rate</li>
      <li><strong>OpEx ratio:</strong> low 40s of EGI</li>
      <li><strong>Time to first move-in:</strong> ~240 days</li>
      <li><strong>Lease-up trajectory:</strong> ~12 months</li>
    </ul>

    <h2 class="serif case-detail__h2">Outcome</h2>
    <p>Full vacancy to stabilized run-rate in twelve months. Both components income-producing, code current, original character preserved. Positioned for long-term hold or refinance.</p>

    <h2 class="serif case-detail__h2">Relevance</h2>
    <p>Applicable to small-format commercial buildings in secondary markets that have lapsed into vacancy but remain structurally sound — hands-on takeover, disciplined restoration, deliberate lease-up.</p>

  </div>
</section>
''' + CASE_FOOTER

# Structured case study — single-family house flip
CASE_HOUSE_FLIP_BODY = CASE_HERO_TEMPLATE.format(
    title="Single-Family House Flip",
    lead="Acquired distressed, fully renovated, sold at retail. 3 bed / 2.5 bath on 0.80 acres. ~2.2× cost basis at sale."
) + '''
<section class="section">
  <div class="container" style="max-width: 820px;">

    <div class="case-detail__grid">
      <div class="case-detail__meta-block">
        <p class="card__meta">Asset Type</p>
        <p class="case-detail__meta-val">Single-Family Residential &mdash; Upstate New York</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Configuration</p>
        <p class="case-detail__meta-val">3 bed &middot; 2.5 bath &middot; 0.80 acres</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">Condition at Acquisition</p>
        <p class="case-detail__meta-val">Distressed &middot; full renovation required</p>
      </div>
      <div class="case-detail__meta-block">
        <p class="card__meta">SUNdhm Role</p>
        <p class="case-detail__meta-val">Acquisition, renovation &amp; resale</p>
      </div>
    </div>

    <h2 class="serif case-detail__h2">Situation</h2>
    <p>Distressed single-family home, off-market acquisition. Sound bones, dated finishes, deferred maintenance throughout. Strong submarket comps supported a full retail repositioning.</p>

    <h2 class="serif case-detail__h2">Strategic Interventions</h2>
    <ul class="spec-list">
      <li><strong>Disciplined acquisition.</strong> Closed at $49,500 — well below comp-supported ARV.</li>
      <li><strong>Full renovation.</strong> Kitchen, baths, flooring, paint, mechanicals, exterior &mdash; $53,300 scope, fixed budget.</li>
      <li><strong>Retail-grade finish.</strong> Spec aligned to buyer expectations in the price band, not investor-grade.</li>
      <li><strong>Tight project control.</strong> Single GM, weekly draws, no scope creep.</li>
      <li><strong>Listing strategy.</strong> Professional photos, staged key rooms, priced to comps.</li>
    </ul>

    <h2 class="serif case-detail__h2">Results</h2>
    <ul class="case-card__metrics" style="margin-top: 8px;">
      <li><strong>Purchase price:</strong> $49,500</li>
      <li><strong>Renovation cost:</strong> $53,300</li>
      <li><strong>All-in basis:</strong> $102,800</li>
      <li><strong>Sale price:</strong> $229,000</li>
      <li><strong>Gross profit:</strong> $126,200</li>
      <li><strong>Gross ROI on cost:</strong> ~123%</li>
    </ul>

    <h2 class="serif case-detail__h2">Outcome</h2>
    <p>Acquired, renovated, and sold at retail. Returned ~2.2&times; the all-in basis. Well above national flip ROI benchmarks (typically high-20s percent gross).</p>

    <h2 class="serif case-detail__h2">Relevance</h2>
    <p>Applicable to distressed single-family acquisitions in secondary markets where disciplined underwriting, fixed-scope renovation, and retail-grade finish drive outsized spreads at exit.</p>

  </div>
</section>
''' + CASE_FOOTER

# Case Studies hub/index page
CASE_HUB_BODY = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Case Studies</p>
    <h1 class="serif">Engagement snapshots.</h1>
    <p class="lead" style="max-width: 760px; margin-top: 16px;">Representative engagements illustrating how SUNdhm operates across lender mandates, owner-retained third-party management, and pre-foreclosure resolutions. Specific borrower, lender, brand, and asset identifiers have been generalized.</p>
  </div>
</section>

<section class="section" style="background: var(--cream);">
  <div class="container">
    <div class="grid grid-3 case-grid">

      <a class="case-card case-card--link reveal" href="./case-lender.html">
        <div class="case-card__num">01</div>
        <p class="card__meta">Lender Engagement</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">~80 keys · Regional bank, conventional CRE loan</p>
        <p class="case-card__body">Lender-engaged operating oversight after borrower default. Restored reporting transparency, stabilized cash flow, and protected collateral value through the workout period.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-property-management.html">
        <div class="case-card__num">02</div>
        <p class="card__meta">Property Management</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">Owner-retained third-party management</p>
        <p class="case-card__body">Owner engaged SUNdhm under a third-party management agreement to professionalize operations. Day-to-day management, brand compliance, revenue management, and transparent monthly reporting.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-resolution.html">
        <div class="case-card__num">03</div>
        <p class="card__meta">Borrower &amp; Lender Resolution</p>
        <h3 class="case-card__title">Limited-Service Hotel — New York</h3>
        <p class="case-card__sub">Regional bank · pre-foreclosure workout</p>
        <p class="case-card__body">Neutral operator and resolution partner during foreclosure proceedings. Foreclosure discontinued, loan returned to performing status, and the borrower retained ownership.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-mixed-use.html">
        <div class="case-card__num">04</div>
        <p class="card__meta">Mixed-Use Restoration</p>
        <h3 class="case-card__title">Mixed-Use Commercial — Upstate New York</h3>
        <p class="case-card__sub">22 units &middot; 3 retail bays &middot; ~4 years vacant</p>
        <p class="case-card__body">Operating takeover of an abandoned mixed-use building. Life-safety re-certified, original character preserved, stabilized run-rate in 12 months.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

      <a class="case-card case-card--link reveal" href="./case-house-flip.html">
        <div class="case-card__num">05</div>
        <p class="card__meta">House Flip</p>
        <h3 class="case-card__title">Single-Family Residential — Upstate New York</h3>
        <p class="case-card__sub">3 bed &middot; 2.5 bath &middot; 0.80 acres</p>
        <p class="case-card__body">Distressed acquisition, full renovation, retail resale. $102.8K all-in to $229K sale &mdash; ~123% gross ROI on cost.</p>
        <p class="case-card__cta">Read full case study <span aria-hidden="true">&rarr;</span></p>
      </a>

    </div>

    <p class="case-disclaimer">Representative engagement profiles. Specific borrower, lender, brand, and asset identifiers have been generalized. Figures are illustrative of typical engagement performance and do not reflect any single client. SUNdhm is a New York State approved receiver and property manager.</p>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width: 820px; text-align: center;">
    <p class="eyebrow">Engage SUNdhm</p>
    <h2 class="serif" style="margin-top: 12px;">Have a similar situation?</h2>
    <p class="lead" style="margin-top: 16px;">Whether you’re a lender, an owner, or a borrower working through a workout, we can step in quickly, stabilize operations, and restore reporting transparency.</p>
    <div style="margin-top: 28px;">
      <a class="btn btn--gold" href="./contact.html">Discuss an engagement <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
    </div>
  </div>
</section>
'''


# ============ WRITE PAGES ============
write_page("index.html",
           "SUNdhm · Hospitality &amp; Real Estate",
           "SUNdhm develops, manages, and markets hospitality and real estate properties — hotels, apartments, short-term rentals, property management, house flipping, banquet & catering, restoration, and receivership.",
           "/", HOME_BODY, hero_overlap=True, active="home")

write_page("services.html",
           "Services · SUNdhm",
           "SUNdhm services: hotel management, apartments &amp; multi-family, Airbnb &amp; STR, third-party property management, house flipping, banquet &amp; catering, and special situations.",
           "/services.html", SERVICES_BODY, hero_overlap=False, active="services")

write_page("careers.html",
           "Careers · SUNdhm",
           "Join SUNdhm — a family-owned hotel and property management operator.",
           "/careers.html", CAREERS_BODY, hero_overlap=False, active="careers")

write_page("contact.html",
           "Contact · SUNdhm · Liverpool, NY",
           "Contact SUNdhm at 250 Commerce Blvd, Liverpool NY 13088. Phone (315) 752-0155 · hello@sundhm.com.",
           "/contact.html", CONTACT_BODY, hero_overlap=False, active="contact")

# Case study sub-pages (linked from /services.html#case-studies)
write_page("case-studies.html",
           "Case Studies · SUNdhm",
           "SUNdhm case studies: representative engagements across lender mandates, owner-retained third-party management, and borrower/lender pre-foreclosure resolutions.",
           "/case-studies.html", CASE_HUB_BODY, hero_overlap=False, active="case-studies")

write_page("case-lender.html",
           "Case Study · Lender-Engaged Operating Oversight · SUNdhm",
           "Representative SUNdhm engagement: lender-engaged operating oversight of a limited-service hotel during a workout — occupancy 38%→61%, ADR $72→$98, payroll 38%→24%, ~9 months to stabilization.",
           "/case-lender.html", CASE_LENDER_BODY, hero_overlap=False, active="case-studies")

write_page("case-property-management.html",
           "Case Study · Third-Party Property Management · SUNdhm",
           "Representative SUNdhm engagement: owner-retained third-party management of a limited-service hotel — occupancy low 40s→mid 60s, ADR ~+30%, payroll ratio reduced ~10pp, transparent monthly reporting.",
           "/case-property-management.html", CASE_PM_BODY, hero_overlap=False, active="case-studies")

write_page("case-resolution.html",
           "Case Study · Borrower &amp; Lender Resolution · SUNdhm",
           "Representative SUNdhm engagement: pre-foreclosure workout where SUNdhm served as neutral operator and resolution partner. Foreclosure discontinued, loan returned to performing status, borrower retained ownership.",
           "/case-resolution.html", CASE_RESOLUTION_BODY, hero_overlap=False, active="case-studies")

write_page("case-mixed-use.html",
           "Case Study · Abandoned Mixed-Use Commercial Restoration · SUNdhm",
           "Representative SUNdhm engagement: operating takeover of an abandoned mixed-use commercial building in Upstate New York — 22 residential units, 3 retail bays, ~4 years vacant. Life-safety re-certified, residential occupancy 0%→73%, commercial occupancy 0%→67%, ~12 months to stabilized run-rate.",
           "/case-mixed-use.html", CASE_MIXED_USE_BODY, hero_overlap=False, active="case-studies")

write_page("case-house-flip.html",
           "Case Study · Single-Family House Flip · SUNdhm",
           "Representative SUNdhm engagement: distressed single-family acquisition, full renovation, and retail resale in Upstate New York — 3 bed, 2.5 bath, 0.80 acres. $49.5K purchase + $53.3K renovation → $229K sale, ~123% gross ROI on cost.",
           "/case-house-flip.html", CASE_HOUSE_FLIP_BODY, hero_overlap=False, active="case-studies")

# ============ LEGAL PAGES ============
# Reviewed and approved by counsel: May 9, 2026.
# When updating any of PRIVACY_BODY, TERMS_BODY, or ACCESSIBILITY_BODY,
# bump LEGAL_LAST_UPDATED and re-circulate to counsel for review.
LEGAL_LAST_UPDATED = "May 9, 2026"

PRIVACY_BODY = f'''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1 class="serif">Privacy Policy</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">Last updated: {LEGAL_LAST_UPDATED}</p>
  </div>
</section>

<section class="section">
  <div class="container legal-doc">
    <p>SUNdhm ("<strong>SUNdhm</strong>," "<strong>we</strong>," "<strong>us</strong>," or "<strong>our</strong>") respects your privacy. This Privacy Policy explains what information we collect through <a href="https://www.sundhm.com">www.sundhm.com</a> (the "Site"), how we use it, with whom we share it, and the rights you have under U.S. state privacy laws including the California Consumer Privacy Act ("CCPA") as amended by the California Privacy Rights Act ("CPRA"), the Virginia Consumer Data Protection Act, the Colorado Privacy Act, and similar laws.</p>

    <h2>1. Information We Collect</h2>
    <p>We collect the following categories of personal information:</p>
    <ul class="spec-list">
      <li><strong>Identifiers:</strong> name, email address, telephone number, mailing address, IP address.</li>
      <li><strong>Professional information:</strong> résumé contents and employment history submitted through our Careers form.</li>
      <li><strong>Commercial information:</strong> details about properties or services you inquire about.</li>
      <li><strong>Internet activity:</strong> pages visited, links clicked, browser type, device information, and similar usage data collected via cookies and analytics.</li>
      <li><strong>Inferences:</strong> drawn from the above to understand your interests in our services.</li>
    </ul>

    <h2>2. How We Use Your Information</h2>
    <ul class="spec-list">
      <li>Respond to your inquiries about property management, receivership, mortgage workouts, and other services.</li>
      <li>Process and evaluate employment applications.</li>
      <li>Operate, maintain, and improve the Site.</li>
      <li>Send service-related communications and, where permitted, marketing communications you can opt out of.</li>
      <li>Comply with legal obligations and enforce our Terms of Use.</li>
    </ul>

    <h2>3. Cookies &amp; Tracking Technologies</h2>
    <p>We use cookies and similar technologies to operate the Site and analyze traffic. You can manage your preferences any time through the "Cookie Preferences" link in the footer. Cookie categories used on this Site:</p>
    <ul class="spec-list">
      <li><strong>Strictly necessary</strong> — always on; required for the Site to function.</li>
      <li><strong>Analytics</strong> — optional; helps us understand aggregate Site usage.</li>
      <li><strong>Marketing</strong> — optional; supports advertising on third-party platforms.</li>
    </ul>
    <p>You may also disable cookies through your browser settings; however, disabling strictly necessary cookies may impair Site functionality.</p>

    <h2>4. How We Share Information</h2>
    <p>We do not sell your personal information for money. We may share information with:</p>
    <ul class="spec-list">
      <li><strong>Service providers</strong> who host the Site, deliver email, process forms, or provide analytics under contract with us.</li>
      <li><strong>Professional advisors</strong> such as attorneys, accountants, and insurers when reasonably necessary.</li>
      <li><strong>Government authorities or courts</strong> when required by law, subpoena, or to protect our legal rights.</li>
      <li><strong>Successors</strong> in the event of a merger, acquisition, or sale of assets.</li>
    </ul>

    <h2 id="ccpa">5. Your U.S. State Privacy Rights</h2>
    <p>Depending on the state in which you live, you may have the right to:</p>
    <ul class="spec-list">
      <li>Know what personal information we collect, use, and disclose about you.</li>
      <li>Access a copy of your personal information.</li>
      <li>Correct inaccurate personal information.</li>
      <li>Delete your personal information, subject to legal exceptions.</li>
      <li>Opt out of the "sale" or "sharing" of personal information for cross-context behavioral advertising.</li>
      <li>Limit the use of sensitive personal information.</li>
      <li>Not be discriminated against for exercising these rights.</li>
    </ul>
    <p><strong>Do Not Sell or Share My Personal Information:</strong> SUNdhm does not sell personal information for monetary value and does not currently share personal information for cross-context behavioral advertising. You can submit a request below or email <a href="mailto:privacy@sundhm.com?subject=Privacy%20Rights%20Request">privacy@sundhm.com</a>.</p>
    <p>You may designate an authorized agent to make a request on your behalf. We will verify your identity (and your agent's authorization) before responding and will respond within 45 days, with one 45-day extension if reasonably necessary.</p>

    <h2 id="privacy-requests">6. Submit a Privacy Request</h2>
    <p>Use this form to exercise any of your rights above — Access, Correct, Delete, Opt out of sale/share, Limit sensitive data use, or Authorized agent request. You may also email <a href="mailto:privacy@sundhm.com?subject=Privacy%20Rights%20Request">privacy@sundhm.com</a> directly.</p>
    <form class="apply-form" action="https://formsubmit.co/privacy@sundhm.com" method="POST" novalidate style="margin-top: 18px;">
      <input type="hidden" name="_subject" value="Privacy Rights Request — sundhm.com" />
      <input type="hidden" name="_captcha" value="true" />
      <input type="hidden" name="_template" value="table" />
      <input type="hidden" name="_next" value="https://www.sundhm.com/privacy.html?submitted=1#privacy-requests" />
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" />
      <div class="form-grid">
        <label class="form-field"><span>Full name <em>*</em></span><input type="text" name="Full Name" required autocomplete="name" /></label>
        <label class="form-field"><span>Email <em>*</em></span><input type="email" name="Email" required autocomplete="email" /></label>
        <label class="form-field"><span>State of residence</span><input type="text" name="State" placeholder="e.g., California, New York" /></label>
        <label class="form-field"><span>Request type <em>*</em></span>
          <select name="Request Type" required>
            <option value="">Select…</option>
            <option>Access — copy of my personal information</option>
            <option>Correct — fix inaccurate information</option>
            <option>Delete — erase my personal information</option>
            <option>Opt out of Sale or Share</option>
            <option>Limit use of Sensitive Personal Information</option>
            <option>Authorized agent request</option>
            <option>Other / general privacy question</option>
          </select>
        </label>
        <label class="form-field form-field--wide"><span>Details (optional)</span><textarea name="Details" rows="4" placeholder="Tell us anything that helps us identify you in our records or fulfill the request."></textarea></label>
        <label class="form-field form-field--wide" style="flex-direction: row; align-items: flex-start; gap: 10px;">
          <input type="checkbox" name="Verification Acknowledged" value="yes" required style="width: auto; margin-top: 4px;" />
          <span style="font-size: 14px; color: var(--ink-soft);">I confirm I am the person whose information is the subject of this request, or an authorized agent. I understand SUNdhm will verify my identity before responding.</span>
        </label>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn btn--gold">Submit privacy request</button>
      </div>
      <p class="form-note">We respond within 45 days. Verification may require additional information.</p>
    </form>

    <h2>7. Children's Privacy</h2>
    <p>The Site is not directed to children under 13, and we do not knowingly collect personal information from them. If you believe a child has provided us personal information, please contact us and we will delete it.</p>

    <h2>8. Data Security &amp; Retention</h2>
    <p>We use reasonable administrative, technical, and physical safeguards consistent with the New York SHIELD Act to protect personal information. We retain personal information only as long as necessary to fulfill the purposes described in this Policy or as required by law.</p>

    <h2>9. Third-Party Links</h2>
    <p>The Site may contain links to third-party websites. We are not responsible for the privacy practices of those sites and encourage you to review their privacy policies.</p>

    <h2>10. Changes to This Policy</h2>
    <p>We may update this Privacy Policy from time to time. The "Last updated" date at the top of this page reflects the latest revision.</p>

    <h2>11. Contact Us</h2>
    <p>SUNdhm<br/>250 Commerce Blvd<br/>Liverpool, NY 13088<br/>Phone: <a href="tel:+13157520155">(315) 752-0155</a><br/>Privacy email: <a href="mailto:privacy@sundhm.com">privacy@sundhm.com</a><br/>General email: <a href="mailto:hello@sundhm.com">hello@sundhm.com</a></p>
  </div>
</section>
'''

TERMS_BODY = f'''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1 class="serif">Terms of Use</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">Last updated: {LEGAL_LAST_UPDATED}</p>
  </div>
</section>

<section class="section">
  <div class="container legal-doc">
    <p>These Terms of Use ("Terms") govern your access to and use of <a href="https://www.sundhm.com">www.sundhm.com</a> (the "Site"), operated by SUNdhm. By accessing the Site you agree to these Terms. If you do not agree, do not use the Site.</p>

    <h2>1. Use of the Site</h2>
    <p>You may use the Site only for lawful purposes and in accordance with these Terms. You agree not to:</p>
    <ul class="spec-list">
      <li>Use the Site in any way that violates applicable federal, state, local, or international law.</li>
      <li>Attempt to gain unauthorized access to any portion of the Site or our systems.</li>
      <li>Use any robot, spider, or automated means to access the Site for any purpose.</li>
      <li>Introduce viruses, trojans, or other malicious code.</li>
      <li>Impersonate any person or entity, or misrepresent your affiliation.</li>
    </ul>

    <h2>2. Intellectual Property</h2>
    <p>The Site and all content on it (including text, graphics, logos, photographs, and the SUNdhm name and marks) are owned by or licensed to SUNdhm and are protected by United States and international copyright, trademark, and other intellectual property laws. You may not reproduce, distribute, modify, or create derivative works without our prior written permission.</p>

    <h2>3. No Professional Advice</h2>
    <p>Information on the Site is provided for general informational purposes only and does not constitute legal, financial, accounting, investment, tax, or other professional advice. SUNdhm is not a law firm. Statements regarding mortgage disputes, workouts, receivership, or related services describe operational support and are not a substitute for advice from qualified counsel. You should consult licensed professionals before making decisions based on Site content.</p>

    <h2>4. No Engagement Created</h2>
    <p>Contacting SUNdhm through the Site, submitting a form, or sending an email does not create a management, agency, fiduciary, or attorney-client relationship. A formal engagement requires a written agreement signed by both parties.</p>

    <h2>5. Forward-Looking Statements</h2>
    <p>The Site may include statements about anticipated performance, services, or strategies. Those statements involve risks and uncertainties, and actual outcomes may differ materially. SUNdhm makes no guarantee of any specific outcome from any service described on the Site.</p>

    <h2>6. Third-Party Links</h2>
    <p>The Site may contain links to third-party websites for convenience. We do not endorse and are not responsible for the content of those sites.</p>

    <h2>7. Disclaimers</h2>
    <p>THE SITE IS PROVIDED "AS IS" AND "AS AVAILABLE," WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SITE WILL BE UNINTERRUPTED, SECURE, OR ERROR-FREE.</p>

    <h2>8. Limitation of Liability</h2>
    <p>TO THE FULLEST EXTENT PERMITTED BY LAW, SUNdhm AND ITS OWNERS, OFFICERS, EMPLOYEES, AND AGENTS WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATING TO YOUR USE OF THE SITE.</p>

    <h2>9. Indemnification</h2>
    <p>You agree to defend, indemnify, and hold harmless SUNdhm and its affiliates from any claims, damages, or expenses (including reasonable attorneys' fees) arising from your use of the Site or your violation of these Terms.</p>

    <h2>10. Governing Law &amp; Venue</h2>
    <p>These Terms are governed by the laws of the State of New York without regard to its conflict-of-law principles. Any dispute will be resolved exclusively in the state or federal courts located in Onondaga County, New York, and you consent to that venue.</p>

    <h2>11. Changes</h2>
    <p>We may revise these Terms at any time by updating this page. Continued use of the Site after changes constitutes acceptance of the revised Terms.</p>

    <h2>12. Contact</h2>
    <p>Questions about these Terms? Email <a href="mailto:hello@sundhm.com">hello@sundhm.com</a>.</p>
  </div>
</section>
'''

ACCESSIBILITY_BODY = f'''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1 class="serif">Accessibility Statement</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">Last updated: {LEGAL_LAST_UPDATED}</p>
  </div>
</section>

<section class="section">
  <div class="container legal-doc">
    <p>SUNdhm is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.</p>

    <h2>Conformance Status</h2>
    <p>The Web Content Accessibility Guidelines (WCAG) define requirements for designers and developers to improve accessibility for people with disabilities. We aim to conform to <strong>WCAG 2.1 Level AA</strong>.</p>

    <h2>Measures Taken</h2>
    <ul class="spec-list">
      <li>Semantic HTML structure for assistive technologies.</li>
      <li>Keyboard-navigable menus, forms, and interactive components.</li>
      <li>Sufficient color contrast for body text and interactive elements.</li>
      <li>Descriptive alt text on meaningful imagery.</li>
      <li>Form fields with visible labels and accessible error messages.</li>
    </ul>

    <h2>Feedback</h2>
    <p>We welcome your feedback on the accessibility of the SUNdhm website. If you encounter accessibility barriers or have suggestions, please contact us:</p>
    <p>SUNdhm<br/>250 Commerce Blvd, Liverpool, NY 13088<br/>Phone: <a href="tel:+13157520155">(315) 752-0155</a><br/>Email: <a href="mailto:hello@sundhm.com?subject=Accessibility%20Feedback">hello@sundhm.com</a></p>
    <p>We try to respond to accessibility feedback within five business days.</p>

    <h2>Compatibility</h2>
    <p>The Site is designed to be compatible with recent versions of major browsers (Chrome, Firefox, Safari, Edge) and with common assistive technologies including screen readers and operating-system magnification.</p>

    <h2>Limitations</h2>
    <p>Despite our efforts, some content may not yet be fully accessible. If you need information from a page in an alternative format, please contact us and we will provide it as soon as practicable.</p>
  </div>
</section>
'''

write_page("privacy.html",
           "Privacy Policy · SUNdhm",
           "SUNdhm Privacy Policy — how we collect, use, and protect your personal information, plus your rights under U.S. state privacy laws including CCPA/CPRA.",
           "/privacy.html", PRIVACY_BODY, hero_overlap=False, active="")

write_page("terms.html",
           "Terms of Use · SUNdhm",
           "Terms of Use governing your access to and use of www.sundhm.com.",
           "/terms.html", TERMS_BODY, hero_overlap=False, active="")

write_page("accessibility.html",
           "Accessibility Statement · SUNdhm",
           "SUNdhm's commitment to digital accessibility and conformance with WCAG 2.1 Level AA.",
           "/accessibility.html", ACCESSIBILITY_BODY, hero_overlap=False, active="")

print("Done.")
