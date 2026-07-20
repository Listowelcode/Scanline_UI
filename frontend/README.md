# ScanLine — Next.js

This is a Next.js 14 (App Router) port of the original static ScanLine
HTML/CSS/JS site. The UI, styling, and backend connection are unchanged.

## What changed vs. the original

- `index.html` → `app/layout.js` (page shell, `<head>`, Google Font link,
  favicon) + `app/page.js` + `app/components/ScanlineApp.js` (the markup).
- `style.css` → `app/globals.css` (copied as-is, with a few extra `@media`
  rules appended at the bottom purely for small-screen / overflow safety —
  no existing rule was modified, removed, or overridden).
- `script.js` → converted into React state/hooks inside
  `app/components/ScanlineApp.js` (`"use client"` component). The logic,
  variable names, and control flow are ported 1:1.
- Added `public/icon-logo.png`, wired up as the browser tab icon via
  `metadata.icons` in `app/layout.js`.

## Backend connection — unchanged

The frontend still talks to the exact same backend, at the exact same
base URL and endpoints as before:

```js
const API = "http://127.0.0.1:8000";

POST  ${API}/preview
POST  ${API}/scan
GET   ${API}/progress
GET   ${API}/download/:filename
```

Nothing about these requests (method, headers, body shape, or URLs) was
changed. If your backend runs elsewhere, update the `API` constant at the
top of `app/components/ScanlineApp.js`.

## Getting started

```bash
npm install
npm run dev
```

Then open http://localhost:3000.

## Build

```bash
npm run build
npm run start
```

## Project structure

```
app/
  layout.js               # <html>/<body> shell, metadata, favicon, font
  page.js                 # renders the client app
  globals.css             # ported styles (unchanged) + responsive additions
  components/
    ScanlineApp.js         # all UI + logic (ported from script.js)
public/
  icon-logo.png            # tab icon / favicon
```
