# sundhm-site

Modern static site for **SUNdhm** (sundhm.com).

## Stack
- Plain HTML/CSS/JS (no build step)
- Caddy (Docker) for serving on Railway
- Same deployment pattern as `syracuse-grand` and `cicero-grand`

## Local preview
```bash
python3 -m http.server 8080
```
Then open http://localhost:8080.

## Deploy
Push to `main` — Railway auto-deploys via the included `Dockerfile` and `railway.json`.

## Editing content
- **Copy & sections:** `index.html`
- **Styles & colors:** `style.css` (CSS custom properties at the top)
- **Images:** `assets/images/`
- **Contact info:** edit the contact section in `index.html` (3 places: JSON-LD schema, contact card, footer)
