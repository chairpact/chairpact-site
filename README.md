# chairpact-site

Company website for Chairpact Integrated Services Ltd, served via GitHub Pages at `www.chairpact.com`.

## Files
The site lives in `docs/`, and GitHub Pages publishes from that folder. Everything else (this README, `tools/`) stays out of the site.

- `docs/index.html` is the home page: services, training teaser, brands, about, leadership and contact
- `docs/training/index.html` is the IT Training page (modules, how it works, trainers, register interest)
- `docs/404.html` is shown for any missing URL
- `docs/styles.css` holds all styling (colours are variables at the top)
- `docs/main.js` handles the footer year and the mobile menu
- `docs/CNAME` tells GitHub Pages to serve this at www.chairpact.com
- `docs/assets/logo/` contains the logos. `logo.png` and `mark.png` are the original artwork with only the background removed. The `-dark` versions are used automatically in dark mode.
- `tools/logo/` holds the original logo image and the script that generates the logo files

## Preview locally
Any static file server works. The site itself needs no Python, Node or build step. Use either of these:

```sh
# Python (built into macOS, nothing to install)
python3 -m http.server 8080 -d docs

# Node (downloads the `serve` package the first time)
npx serve docs -l 8080
```
Then open http://localhost:8080. Use a server rather than opening the HTML file directly, because the links between pages (`training/`, `../`) rely on it. If you see an old version, press Cmd+Shift+R to reload without the cache.

## Navigation
In the navbar, plain links scroll to a section on the current page, and pill buttons go to another page or are the main action. The link for the section you're viewing is highlighted (see `docs/main.js`). The footer lists both pages' sections in labelled columns.

## Editing
- **Add a service:** copy one `<article class="card">…</article>` block in the Services section of `docs/index.html`.
- **Add a training module:** copy a module card in `docs/training/index.html` and change the title, text and the module name inside its `mailto:` link.
- **Leadership / trainers:** each person is a `<div class="card person">`. To use a photo instead of initials, replace `<div class="avatar">M</div>` with `<img class="avatar" src="assets/team/name.jpg" alt="">`.
- **Colours:** in `docs/styles.css`. Light-mode colours are at the top and dark-mode colours are just below. `--brand` is the logo navy and `--accent` is the logo maroon.
- **Font:** Plus Jakarta Sans (Google Fonts). Change it in the `<link>` in each HTML file and in `body` in `docs/styles.css`.
- **Contact email:** search for `info@chairpact.com`.

## Regenerating the logos
```sh
pip3 install pillow numpy
python3 tools/logo/build.py tools/logo/source.png docs/assets --dark tint
```
This rebuilds the logos, the favicons and the social share image (`docs/assets/og-image.png`). The light-mode logos are always the original artwork. `--dark` sets the dark-mode treatment: `tint`, `white` or `keep` (see the top of the script). Leave it out to keep the existing dark files.

## Hosting
- **Site:** GitHub Pages publishes the `docs/` folder on the `main` branch (Settings → Pages). Merging to `main` puts changes live within a minute or two.
- **`www.chairpact.com`:** a CNAME record pointing to `chairpact.github.io`, set in Zoho DNS.
- **`chairpact.com`:** has no A records. Zoho **Domain Forwarding** sends it to `https://www.chairpact.com` with a 301 redirect, keeping the page path.
- **Email:** the Zoho Mail MX, SPF, DKIM (`zmail._domainkey`) and verification records are separate from the site. Leave them as they are.
