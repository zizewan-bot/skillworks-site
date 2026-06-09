# Skillworks Site

Static public site for Skillworks and Picture Dictionary Kids privacy/support pages.

## Purpose

Skillworks is the umbrella site for education, productivity, skill-building, and app projects. The first project page is Picture Dictionary Kids, including public privacy and support pages needed for App Store/TestFlight readiness.

This site intentionally has:

- no backend
- no analytics
- no ads
- no tracking
- no cookies
- no login
- no third-party scripts

## Local Development

Open `public/index.html` directly in a browser, or serve the `public` directory with any local static file server.

## Build

```sh
npm run check
npm run build
```

The build output is `dist/`.

## Deployment Target

Cloudflare Pages.

- Build command: `npm run build`
- Output directory: `dist`

Recommended public privacy URL for App Store Connect:

`https://picturedictionary.skillworks.dev/privacy`

Temporary fallback if the subdomain is not configured yet:

`https://skillworks.dev/picture-dictionary/privacy`

## Public URLs

Recommended App Store Connect Privacy Policy URL:

`https://picturedictionary.skillworks.dev/privacy`

Recommended Support URL:

`https://picturedictionary.skillworks.dev/support`

## Contact Addresses

- Privacy: `privacy@skillworks.dev`
- Support: `support@skillworks.dev`
