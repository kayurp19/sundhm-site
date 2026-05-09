"""Generate the multi-page SUNdhm site from shared partials."""
import os, pathlib

ROOT = pathlib.Path(__file__).parent

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
<link rel="stylesheet" href="./style.css" />

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
<header class="{cls}" id="top">
  <div class="container sd-header__inner">
    <a href="./index.html" class="sd-header__logo" aria-label="SUNdhm home">
      <img src="./assets/images/logo.png" alt="SUNdhm" width="120" height="70" />
    </a>
    <nav class="sd-header__nav" aria-label="Primary">
{link("index.html","Home","home")}
{link("services.html","Services","services")}
{link("careers.html","Careers","careers")}
{link("contact.html","Contact","contact")}
    </nav>
    <a class="btn btn--gold sd-header__cta" href="./contact.html">Contact</a>
    <button class="sd-header__menu-btn" aria-label="Open menu" id="menuBtn">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
  <nav class="sd-mobile-nav" id="mobileNav" aria-label="Mobile">
    <button class="sd-mobile-nav__close" aria-label="Close menu" id="menuClose">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
    <a href="./index.html">Home</a>
    <a href="./services.html">Services</a>
    <a href="./careers.html">Careers</a>
    <a href="./contact.html">Contact</a>
  </nav>
</header>
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
      <a href="./privacy.html#ccpa">Do Not Sell or Share My Personal Information</a>
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
  if (menuBtn) menuBtn.addEventListener('click', () => mobileNav.classList.add('is-open'));
  if (menuClose) menuClose.addEventListener('click', () => mobileNav.classList.remove('is-open'));
  document.querySelectorAll('.sd-mobile-nav a').forEach(a => a.addEventListener('click', () => mobileNav.classList.remove('is-open')));

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
  })();
</script>
</body>
</html>'''


def write_page(path, title, desc, canonical, body_html, hero_overlap=False, active=""):
    html = head(title, desc, canonical) + "\n" + header(active, hero_overlap=hero_overlap) + body_html + "\n" + FOOTER
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
    <p class="eyebrow" style="color: var(--gold-bright);">Upstate New York</p>
    <h1 class="serif">Building, managing, and growing <em>hospitality and real estate.</em></h1>
    <p class="sd-hero__lead">SUNdhm is a family-owned operator with deep roots in Central New York. We own and manage hotels, apartments, short-term rentals, and commercial properties — and we partner with owners and lenders who want disciplined, hands-on stewardship of their assets.</p>
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
        <p class="lead">With years of experience across Upstate New York, SUNdhm has solidified its reputation as an innovator in developing, managing, and marketing economically viable hotel and real estate properties. We pair hands-on ownership with disciplined operations — guest-first service, sharp financial controls, and modern digital marketing — so every property performs.</p>
        <p style="margin-top: 16px;">Our portfolio spans franchised and independent hotels, multi-family apartments, short-term rentals, banquet and catering venues, residential flips, and management contracts and receiverships for owners and lenders looking for accountable stewardship.</p>
      </div>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="section--navy" style="padding: 0;">
  <div class="stats">
    <div class="stat reveal"><div class="stat__num">30+</div><div class="stat__lab">Years Operating</div></div>
    <div class="stat reveal"><div class="stat__num">300+</div><div class="stat__lab">Hotel Rooms</div></div>
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
        <p class="lead" style="margin-top: 20px;">Three decades of hands-on experience operating hotels and real estate across Central New York. Click any service to see how we deliver it.</p>
        <a class="btn btn--gold" href="./services.html" style="margin-top: 28px;">All services in detail <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </div>
      <ul class="reveal svc-bullets">
        <li><a href="./services.html#hotel-management"><span class="svc-bullets__name">Hotel Management</span><span class="svc-bullets__sub">Revenue, brand compliance, OTA strategy</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#apartments"><span class="svc-bullets__name">Apartments &amp; Multi-Family</span><span class="svc-bullets__sub">Long-term rentals, leasing, maintenance</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#str"><span class="svc-bullets__name">Airbnb &amp; STR Operations</span><span class="svc-bullets__sub">Listing, dynamic pricing, guest support</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#property-management"><span class="svc-bullets__name">Third-Party Property Management</span><span class="svc-bullets__sub">Hotels, residential, commercial</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#flipping"><span class="svc-bullets__name">House Flipping &amp; Development</span><span class="svc-bullets__sub">Cash offers, two-week closings</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#banquet"><span class="svc-bullets__name">Banquet &amp; Catering</span><span class="svc-bullets__sub">Weddings, corporate, private events</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
        <li><a href="./services.html#receivership"><span class="svc-bullets__name">Receivership &amp; Special Assets</span><span class="svc-bullets__sub">For banks, lenders, and special servicers</span><svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></li>
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
          <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Sell%20My%20House%20to%20SUNdhm" style="color: var(--gold-deep); font-weight: 600;">Email us about your property →</a></p>
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
          <p>Flexible event spaces and full-service catering at our Central New York hotels — built on the same operational discipline that runs our hotel F&amp;B programs.</p>
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
          <p class="card__desc">Court-appointed and lender-engaged receivership for distressed hospitality, multi-family, and commercial assets across New York State. We take possession quickly, secure the property, restore financial controls, stabilize operations, and report transparently to the court and to you.</p>
          <span class="svc-card__more"><span class="lbl-more">Learn more</span><span class="lbl-less">Show less</span> <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></span>
        </div>
        <div class="svc-card__shield">
          <svg viewBox="0 0 80 80" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M40 8L12 22v18c0 16 12 30 28 38 16-8 28-22 28-38V22L40 8z M30 40l7 7 14-17"/></svg>
        </div>
      </button>
      <div class="svc-card__detail">
        <p>When a hospitality, multi-family, or commercial asset is in distress, lenders and courts engage SUNdhm to take control quickly, secure the property, restore financial discipline, and protect collateral value. We've been on the operating side of distressed assets for decades — we know what to look for and how to fix it.</p>
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
        <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Receivership%20Engagement%20Inquiry" style="color: var(--gold-deep); font-weight: 600;">Inquire about a receivership engagement →</a></p>
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
        <p style="margin-top: 16px;"><a href="mailto:hello@sundhm.com?subject=Mortgage%20Dispute%20Help%20%E2%80%94%20Confidential" style="color: var(--gold-deep); font-weight: 600;">Email a confidential summary →</a></p>
      </div>
    </article>
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
    <h1 class="serif">Build your career with a local operator.</h1>
    <p class="lead" style="max-width: 720px; margin-top: 16px;">We're always looking for great people — front desk, housekeeping, maintenance, sales, and management — across our hotel and hospitality properties in Central New York.</p>
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


# ============ WRITE PAGES ============
write_page("index.html",
           "SUNdhm · Hospitality &amp; Real Estate · Upstate New York",
           "SUNdhm develops, manages, and markets hospitality and real estate properties across Upstate New York — hotels, apartments, short-term rentals, property management, house flipping, banquet & catering, and receivership.",
           "/", HOME_BODY, hero_overlap=True, active="home")

write_page("services.html",
           "Services · SUNdhm",
           "SUNdhm services: hotel management, apartments &amp; multi-family, Airbnb &amp; STR, third-party property management, house flipping, banquet &amp; catering, and special situations.",
           "/services.html", SERVICES_BODY, hero_overlap=False, active="services")

write_page("careers.html",
           "Careers · SUNdhm",
           "Join SUNdhm — a family-owned hotel and property management operator hiring across Central New York.",
           "/careers.html", CAREERS_BODY, hero_overlap=False, active="careers")

write_page("contact.html",
           "Contact · SUNdhm · Liverpool, NY",
           "Contact SUNdhm at 250 Commerce Blvd, Liverpool NY 13088. Phone (315) 752-0155 · hello@sundhm.com.",
           "/contact.html", CONTACT_BODY, hero_overlap=False, active="contact")

# ============ LEGAL PAGES ============
import datetime as _dt
LEGAL_LAST_UPDATED = _dt.datetime.now().strftime("%B %d, %Y")

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
    <p><strong>Do Not Sell or Share My Personal Information:</strong> SUNdhm does not sell personal information for monetary value. To opt out of any sharing for cross-context behavioral advertising or to exercise any of the above rights, email <a href="mailto:hello@sundhm.com?subject=Privacy%20Rights%20Request">hello@sundhm.com</a> with the subject line "Privacy Rights Request" and tell us which right you would like to exercise. We will verify your identity before responding and will respond within 45 days.</p>
    <p>You may also designate an authorized agent to make a request on your behalf.</p>

    <h2>6. Children's Privacy</h2>
    <p>The Site is not directed to children under 13, and we do not knowingly collect personal information from them. If you believe a child has provided us personal information, please contact us and we will delete it.</p>

    <h2>7. Data Security &amp; Retention</h2>
    <p>We use reasonable administrative, technical, and physical safeguards to protect personal information. We retain personal information only as long as necessary to fulfill the purposes described in this Policy or as required by law.</p>

    <h2>8. Third-Party Links</h2>
    <p>The Site may contain links to third-party websites. We are not responsible for the privacy practices of those sites and encourage you to review their privacy policies.</p>

    <h2>9. Changes to This Policy</h2>
    <p>We may update this Privacy Policy from time to time. The "Last updated" date at the top of this page reflects the latest revision.</p>

    <h2>10. Contact Us</h2>
    <p>SUNdhm<br/>250 Commerce Blvd<br/>Liverpool, NY 13088<br/>Phone: <a href="tel:+13157520155">(315) 752-0155</a><br/>Email: <a href="mailto:hello@sundhm.com">hello@sundhm.com</a></p>
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
