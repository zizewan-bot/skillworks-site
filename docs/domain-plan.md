# Domain Plan

Primary domain:

- `https://skillworks.dev`

Preferred Picture Dictionary subdomain:

- `https://picturedictionary.skillworks.dev`
- `https://picturedictionary.skillworks.dev/privacy`
- `https://picturedictionary.skillworks.dev/support`

Temporary fallback path if subdomain routing is not ready:

- `https://skillworks.dev/picture-dictionary`
- `https://skillworks.dev/picture-dictionary/privacy`
- `https://skillworks.dev/picture-dictionary/support`

## Recommended App Store Privacy URL

Use this after the subdomain is live and HTTPS is verified:

`https://picturedictionary.skillworks.dev/privacy`

If the subdomain is not ready, use:

`https://skillworks.dev/picture-dictionary/privacy`

## DNS / Cloudflare Notes

- Keep Skillworks as the umbrella site.
- Use the Picture Dictionary subdomain for app-specific privacy/support pages.
- Do not expose backend staging URLs as public privacy/support URLs.
- Do not add third-party scripts for redirects or tracking.
