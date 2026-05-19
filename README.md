# councildata.ai

Landing page for [councildata.ai](https://councildata.ai).

Hosted on GitHub Pages. Static HTML, no build step.

## Deploy

1. Push this directory to a new GitHub repo (e.g. `pspedding/councildata-ai`).
2. In **Settings → Pages**, set:
   - Source: `Deploy from a branch`
   - Branch: `main` / `(root)`
3. In **Settings → Pages → Custom domain**, enter `councildata.ai` and tick **Enforce HTTPS** (once DNS propagates).
4. In **GoDaddy DNS**, set:
   - `A` records for `@`:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - `CNAME` for `www`: `pspedding.github.io`
5. Wait 10–60 min for DNS, then verify at https://councildata.ai.

## Adding a council

Duplicate the `.card` block inside `#councils` in `index.html`. Update name, LGA code, and links.
