# PGD-GB Programme Archive — IBA-SICIP Batch 11 (2025)

A static website. No build step, no server. Host the files as-is.

## Files
- `index.html` — the entire site (HTML, CSS, JavaScript and data are inlined)
- `images/` — logos and lecturer photos
- `curriculum.pdf` — the course curriculum document (Course Curriculum tab)
- `.nojekyll` — tells GitHub Pages to serve every file as-is

## Deploy on GitHub Pages

### Option A — Upload on the website (no command line)
1. Sign in at https://github.com and click **New repository**.
2. Name it, for example `pgd-gb-archive`. Set it **Public**. Create the repository.
3. On the repo page click **uploading an existing file**.
4. Drag in `index.html`, the `images` folder, `curriculum.pdf`, and `.nojekyll`. Commit.
5. Open **Settings > Pages**.
6. Under **Build and deployment**: Source = **Deploy from a branch**, Branch = **main**, Folder = **/ (root)**. Save.
7. Wait about a minute. The site is live at:
   `https://<your-username>.github.io/<repo-name>/`

### Option B — Command line (git)
    git init
    git add .
    git commit -m "PGD-GB archive"
    git branch -M main
    git remote add origin https://github.com/<your-username>/<repo-name>.git
    git push -u origin main
Then enable Pages as in Option A, steps 5 to 7.

## Notes
- All links are relative, so the site works under the `/<repo-name>/` path.
- Tip: naming the repo `<your-username>.github.io` serves the site at the root, `https://<your-username>.github.io/`.
- Custom domain: **Settings > Pages > Custom domain**, then add a CNAME DNS record at your domain provider.
- Update later: replace `index.html` or files in `images/` and commit again.
