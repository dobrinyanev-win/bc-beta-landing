# BC Beta Landing

Standalone static landing page for `https://bc-beta.beyourwealthyness.com/`.

## Boundary

- Separate DigitalOcean App Platform app.
- Static Site component only.
- No database, runtime secrets, or Blend Calculator app routes.
- CTA delegates enrollment to the New Zenler Free plan.

## Local verification

```bash
python scripts/verify.py
python -m http.server 4173 --directory public
```

Enrollment target: `https://beyourwealthyness.newzenler.com/courses/bc-beta/buy`.

## DigitalOcean App Platform

- Type: Static Site
- Source directory: `/`
- Build command: none
- Output directory: `public`
- Catch-all document: `index.html`
- Custom domain: `bc-beta.beyourwealthyness.com`
- DNS management: **You manage your domain**
- Preserve all existing BYW DNS and nameservers.

## Release gates

- Immediately before deployment, verify in New Zenler that the Free plan is active and its enrollment limit is exactly `21`.
- Confirm the DigitalOcean review screen shows a Static Site with `$0.00` incremental monthly cost before creating the app.
- After the 21-place limit is reached, verify that New Zenler rejects further enrollment and retire or update this landing page so its availability copy cannot become stale.
- Do not modify the existing `blend-calculator` app, `www.beyourwealthyness.com`, or the domain nameservers.
