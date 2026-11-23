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
```sh
python3 -m http.server 8080 -d docs
```
Then open http://localhost:8080. Use the server rather than opening the HTML file directly, because the links between pages rely on it.

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

## Going live (moving off Zoho)
1. Push to GitHub. In **Settings → Pages**, set the source to the `main` branch and the `/docs` folder, and set the custom domain to `www.chairpact.com`.
2. At the DNS provider, replace the Zoho landing-page records:
   - `www` CNAME → `chairpact.github.io`
   - `@` (apex) A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. Don't touch the MX, SPF (`v=spf1 include:zohomail.com`) or other TXT records. Zoho Mail keeps working.
4. Once the certificate has been issued, tick **Enforce HTTPS** in Settings → Pages.
5. Unpublish the Zoho landing page.
