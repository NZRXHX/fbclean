# FBClean

### Privacy-focused Facebook Share Link → Reel URL Resolver

**FBClean** is a lightweight, privacy-focused tool that converts Facebook share links into clean, direct Reel URLs.

🔗 **Use FBClean:**
https://nzrxhx.github.io/fbclean/

---

## 🚀 What does FBClean do?

Facebook share links can contain unnecessary redirect parameters and tracking information.

For example:

```text
https://www.facebook.com/reel/906793715833527/?rdid=...&share_url=...
```

FBClean extracts the actual Reel identifier and produces a clean URL:

```text
https://www.facebook.com/reel/906793715833527/
```

You can then copy the clean URL with a single click.

---

## 🔒 Privacy

Privacy is the primary purpose of FBClean.

FBClean is designed to minimize the information it handles:

* No Facebook login is required.
* No Facebook credentials are requested.
* No personal information is collected.
* No analytics or tracking scripts are used.
* No database is used.
* The frontend is completely static.
* The Facebook URL is sent only to the project's serverless resolver when resolving a link.
* The returned Reel URL is displayed directly in your browser.

The project does **not** require users to provide their Facebook cookies or session information.

> **Never provide your Facebook password, access token, or session cookies to FBClean.**

---

## ⚙️ How it works

FBClean consists of two simple components:

```text
┌─────────────────────────┐
│       GitHub Pages      │
│                         │
│       FBClean UI        │
└────────────┬────────────┘
             │
             │ Facebook share URL
             ▼
┌─────────────────────────┐
│    Cloudflare Worker    │
│                         │
│   Resolves redirects    │
└────────────┬────────────┘
             │
             │ HTTP request
             ▼
┌─────────────────────────┐
│        Facebook         │
│                         │
│   /share/r/...          │
│          ↓              │
│   /reel/<ID>/           │
└─────────────────────────┘
```

The browser cannot reliably request Facebook directly because of browser security restrictions such as CORS.

The Cloudflare Worker performs the redirect resolution server-side and returns the resulting Reel URL to the static frontend.

---

## 🧹 Example

### Input

```text
https://web.facebook.com/share/r/19B8Zpc5yv/
```

### Facebook redirect

```text
https://www.facebook.com/reel/906793715833527/?rdid=...&share_url=...
```

### FBClean output

```text
https://www.facebook.com/reel/906793715833527/
```

The unnecessary query parameters are removed.

---

## 📁 Project structure

The frontend is intentionally kept extremely simple:

```text
fbclean/
│
└── index.html
```

The website is hosted through **GitHub Pages**.

The redirect resolver runs separately as a **Cloudflare Worker**.

---

## 🛠️ Technologies

* HTML5
* CSS3
* Vanilla JavaScript
* GitHub Pages
* Cloudflare Workers
* Fetch API

No frontend framework or external JavaScript library is required.

---

## 🌐 Live version

**FBClean:**
https://nzrxhx.github.io/fbclean/

---

## 📜 License

This project is provided for educational and personal use.

---

## ⚠️ Disclaimer

FBClean is an independent utility and is not affiliated with, endorsed by, or sponsored by Facebook or Meta Platforms, Inc.

The tool only resolves publicly accessible URL redirects. It does not bypass authentication, access private content, or attempt to circumvent Facebook's access controls.
