# Cloudflare Pages Deployment

This is a manual deployment checklist. Do not store Cloudflare API tokens or account credentials in this repo.

## Steps

1. Create a GitHub repo named `skillworks-site`.
2. Push this code to the repo.
3. In Cloudflare Pages, create a new Pages project connected to the repo.
4. Configure:
   - Build command: `npm run build`
   - Output directory: `dist`
5. Deploy the first build.
6. Add custom domains:
   - `skillworks.dev`
   - `www.skillworks.dev`
   - `picturedictionary.skillworks.dev`
7. Verify HTTPS for each domain.
8. Confirm these URLs load:
   - `https://skillworks.dev`
   - `https://picturedictionary.skillworks.dev`
   - `https://picturedictionary.skillworks.dev/privacy`
   - `https://picturedictionary.skillworks.dev/support`
9. Use the final App Store Connect Privacy Policy URL:
   - `https://picturedictionary.skillworks.dev/privacy`
10. Use the final Support URL:
   - `https://picturedictionary.skillworks.dev/support`

## Notes

- This site is static and does not need a backend.
- Do not add analytics, ads, tracking, cookies, login, or third-party scripts.
- Do not commit Cloudflare credentials, API tokens, or local account files.
