<div align="center">

<img src="https://img.shields.io/badge/PHP-8%2B-777BB4?style=for-the-badge&logo=php&logoColor=white" />
<img src="https://img.shields.io/badge/Apache-Web%20Server-D22128?style=for-the-badge&logo=apache&logoColor=white" />
<img src="https://img.shields.io/badge/MariaDB-Database-003545?style=for-the-badge&logo=mariadb&logoColor=white" />
<img src="https://img.shields.io/badge/Alpine-Linux-0D597F?style=for-the-badge&logo=alpine-linux&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-Spaces-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/Cloudflare-Workers-F38020?style=for-the-badge&logo=cloudflare&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" />

# 🐘 PHP Web Server — Alpine LAMP Stack

### ⚡ Lightweight · 🔒 Secure · 🚀 Production-Ready

> A complete PHP development environment packed into a **single Docker container** — Apache, PHP 8+, MariaDB, phpMyAdmin, File Manager & Web Terminal.  
> Deploy on **Hugging Face Spaces** for free, or on any **VPS / local machine**.

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📦 What's Inside](#-whats-inside)
- [☁️ Deploy on Hugging Face Spaces](#️-deploy-on-hugging-face-spaces) ⭐ Recommended
- [🖥️ Deploy on VPS / Local Machine](#️-deploy-on-vps--local-machine)
- [🌐 Access URLs](#-access-urls)
- [🗄️ Database Setup](#️-database-setup)
- [💾 Persistent Storage](#-persistent-storage)
- [⚙️ Environment Variables & .env](#️-environment-variables--env)
- [📁 File Manager](#-file-manager)
- [💻 Web Terminal](#-web-terminal)
- [🔀 Custom Domain via Cloudflare Workers](#-custom-domain-via-cloudflare-workers) 🆕
- [💡 Pro Tips](#-pro-tips)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🐘 **PHP 8+** | With OPcache pre-enabled — runs 2x–3x faster out of the box |
| 🌐 **Apache** | Configured with `mod_rewrite` and `.htaccess` support |
| 🗄️ **MariaDB** | Full database engine with phpMyAdmin UI at `/sql` |
| 📁 **File Manager** | [TinyFileManager](https://github.com/prasathmani/tinyfilemanager) at `/files` |
| 💻 **Web Terminal** | Custom browser-based shell at `/terminal` — no SSH needed |
| ⚙️ **.env Support** | Auto-loads `/var/www/localhost/htdocs/.env` at startup |
| 💾 **Persistent Storage** | `/data` mount **required** — database is stored here |
| 🔒 **Non-root** | Runs as user `1000` for improved security |
| 🐳 **Alpine Base** | Ultra-lightweight image with minimal footprint |
| ☁️ **HF Spaces Ready** | Works seamlessly on Hugging Face Docker Spaces |
| 🔀 **Custom Domain** | Mask your HF URL with a custom domain via Cloudflare Workers |

---

## 📦 What's Inside

```
Alpine Linux (latest)
├── Apache 2           → Web server (port 7860)
├── PHP 8.4
├── MariaDB            → Database server
├── phpMyAdmin         → Database UI at /sql
├── TinyFileManager    → File manager at /files
├── Web Terminal       → Custom shell UI at /terminal
├── Composer           → PHP dependency manager
├── Git, Nano, Wget, Zip, Unzip, ImageMagick
```

### 🐘 PHP Extensions

| Extension | Purpose |
|---|---|
| **php-mysqli** | MySQL / MariaDB direct connection |
| **php-pdo** | PHP Data Objects — database abstraction base |
| **php-pdo_mysql** | PDO driver for MySQL / MariaDB |
| **php-mbstring** | Multibyte string handling — required by most frameworks |
| **php-xml** | XML parsing and generation |
| **php-simplexml** | Simple XML object interface — used by WordPress and APIs |
| **php-dom** | Full DOM XML/HTML parsing — required by Laravel and Symfony |
| **php-xmlwriter** | Writing XML documents programmatically |
| **php-xmlreader** | Streaming XML reader for large files |
| **php-xsl** | XSLT transformations |
| **php-gd** | Image creation and manipulation (resize, crop, watermark) |
| **php-imagick** | Advanced image processing via ImageMagick |
| **php-exif** | Read image metadata (camera, GPS, dimensions) |
| **php-curl** | HTTP requests — required by APIs, Guzzle, SDKs |
| **php-session** | Session management |
| **php-opcache** | Bytecode caching — makes PHP 2x–3x faster |
| **php-phar** | PHP Archive support — required by Composer |
| **php-openssl** | SSL/TLS encryption, JWT, secure hashing |
| **php-sodium** | Modern cryptography library |
| **php-iconv** | Character encoding conversion |
| **php-zip** | Create and extract ZIP archives |
| **php-bz2** | Bzip2 compression support |
| **php-intl** | Internationalization — dates, currencies, locales |
| **php-gettext** | Translations and i18n support |
| **php-bcmath** | Arbitrary precision math — required by payment gateways |
| **php-gmp** | GNU Multiple Precision — cryptography and big numbers |
| **php-apcu** | In-memory user cache — speeds up repeated operations |
| **php-redis** | Redis cache and session driver |
| **php-soap** | SOAP web services client and server |
| **php-ldap** | LDAP authentication and directory services |
| **php-ctype** | Character type checking functions |
| **php-fileinfo** | Detect file MIME types |
| **php-tokenizer** | PHP code tokenizer — required by Composer and Laravel |
| **php-sockets** | Low-level socket programming and WebSocket support |
| **php-posix** | POSIX process functions |
| **php-pcntl** | Process control — fork, signals, process management |
| **php-ftp** | FTP client functions |
| **php-calendar** | Calendar and date conversion functions |
| **php-shmop** | Shared memory read/write |
| **php-sysvmsg** | System V message queues |
| **php-sysvsem** | System V semaphores |
| **php-sysvshm** | System V shared memory |
| **php-tidy** | HTML cleanup and repair |
| **readline** | System library — enables interactive PHP shell (php -a) |

---

## ☁️ Deploy on Hugging Face Spaces

> ⭐ **Recommended** — Free hosting, no server required!

### Step 1 — Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Give your space a name (e.g. `my-php-server`)
4. Select **SDK → Docker**
5. Set the Space visibility to **Public**
6. Click **"Create Space"**

> ⚠️ **Keep your Space set to Public.** Hugging Face requires the Space to be public for it to run continuously and be accessible via a URL. Private Spaces may sleep or become inaccessible depending on your plan.

### Step 2 — Upload the Dockerfile

Only the `Dockerfile` is needed in your Space repository:

```
your-space/
└── Dockerfile    ✅ this is the only file needed here
```

> 💡 Drag & drop the `Dockerfile` in the **Files tab**, or push via Git:

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Only add the Dockerfile here
git add Dockerfile
git commit -m "Add Dockerfile"
git push
```

> ⚠️ **Do NOT place your project files here.**  
> Once the Space is live, upload your project files using the **File Manager** at `/files`.  
> Simply go to `/files` → navigate to `/var/www/localhost/htdocs` → upload your files there.

### Step 3 — Set Environment Variables

On Hugging Face, environment variables are configured in **Space Settings** — not in the command line.

1. Open your Space → click **"Settings"** tab
2. Scroll to **"Variables and Secrets"**
3. Add these variables:

| Variable | Default | Description |
|---|---|---|
| `MYSQL_USER` | `admin` | Database username |
| `MYSQL_PASSWORD` | `admin` | Database password *(change this!)* |
| `MYSQL_DATABASE` | `admin` | Database name |
| `SQL_PATH` | `sql` | URL path for phpMyAdmin — e.g. `mysecretdb` opens at `/mysecretdb` |
| `FILES_PATH` | `files` | URL path for File Manager |
| `TERMINAL_PATH` | `terminal` | URL path for Web Terminal |

### Step 4 — Mount Persistent Storage 🚨

> **This step is mandatory** — without it, your database will reset on every restart.

Go to Space **Settings → Persistent Storage** and add:
- **Permission:** Read & Write
- **Mount path:** `/data`

Full setup details → [Persistent Storage section](#-persistent-storage)

### Step 5 — Done! 🎉

Hugging Face will build and deploy automatically. Your live URL:

```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/
```

---

## 🖥️ Deploy on VPS / Local Machine

> For those who prefer their own server or want to test locally.

### Prerequisites

- Docker installed → [Get Docker](https://docs.docker.com/get-docker/)

### Step 1 — Clone & Build

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

docker build -t php-lamp .
```

### Option A — Docker Run

```bash
docker run -d \
  -p 7860:7860 \
  -e MYSQL_USER=admin \
  -e MYSQL_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=mydb \
  --name php-lamp \
  php-lamp
```

### Option B — Docker Compose *(Recommended for VPS)*

```yaml
# docker-compose.yml
version: '3.8'

services:
  php-lamp:
    build: .
    ports:
      - "7860:7860"
    environment:
      - MYSQL_USER=admin
      - MYSQL_PASSWORD=yourpassword
      - MYSQL_DATABASE=mydb
    restart: unless-stopped
```

```bash
docker compose up -d
```

### Access Your Server

```
http://localhost:7860/      → Local machine
http://YOUR_VPS_IP:7860/   → Remote VPS
```

> ⚠️ **On VPS:** Open port `7860` in your firewall first:
> ```bash
> sudo ufw allow 7860   # Ubuntu / Debian
> ```

---

## 🌐 Access URLs

| Tool | Default URL | Env Variable |
|---|---|---|
| 🏠 **Website** | `/` | — |
| 🗄️ **Database UI** | `/sql` | `SQL_PATH` |
| 📁 **File Manager** | `/files` | `FILES_PATH` |
| 💻 **Web Terminal** | `/terminal` | `TERMINAL_PATH` |

> **Web root directory:** `/var/www/localhost/htdocs`

All tool paths are **fully customizable** via environment variables — set them in Space Settings (or `.env`) to hide the default URLs from public discovery. For example, setting `SQL_PATH=x7k2mdb` means phpMyAdmin is only accessible at `/x7k2mdb`.

---

## 🗄️ Database Setup

### Default Credentials

```
Username : admin
Password : admin
Database : admin
Host     : 127.0.0.1
Port     : 3306
```

> ⚠️ **Change the password before going live on a public server!**

### How to Change Credentials

**On Hugging Face:**
Space → Settings → Variables and Secrets → update the values.

**On VPS / Local:**
Update ENV variables in your `docker run` command or `docker-compose.yml`.

---

## 💾 Persistent Storage

> 🚨 **This step is REQUIRED — the database will not work without it!**

MariaDB stores all its data at `/data/mysql` inside the container. If `/data` is not mounted as persistent storage, the **entire database is wiped every time** the Space restarts or rebuilds.

### Setting Up Persistent Storage on Hugging Face

1. Open your Space → click the **"Settings"** tab
2. Scroll down to the **"Persistent Storage"** section
3. Configure it as follows:

| Field | Value |
|---|---|
| **Permission** | Read & Write |
| **Mount path** | `/data` |
| **Visibility** | **Private** *(your data stays secure)* |

> 🔒 **Always keep your Persistent Storage bucket set to Private.** The storage bucket holds your entire database — keeping it private ensures that no one else can access or browse your data files. Your Space itself can remain Public (so your website is accessible), while the storage bucket stays Private (so your database is protected). These are two separate settings — one does not affect the other.

4. Click **"Add storage"** and wait for the Space to restart ✅

Once mounted, the `/data/mysql` directory will **survive restarts and rebuilds** — your database tables and data are fully preserved automatically. No extra configuration needed.

The container handles everything internally on first boot:

```bash
# First run — initializes the database at /data/mysql
mariadb-install-db --datadir=/data/mysql --skip-test-db --user=1000

# Every run — starts MariaDB using /data/mysql as datadir
mariadbd --datadir=/data/mysql --bind-address=127.0.0.1
```

> 💡 You don't need to run these manually — `start.sh` does it automatically.

---

## ⚙️ Environment Variables & .env

You can configure your PHP app using a `.env` file — no need to hardcode sensitive values like API keys or database credentials in your code.

### How It Works

Place a `.env` file in your web root:

```
/var/www/localhost/htdocs/.env
```

The server automatically loads it at startup, before Apache and MariaDB start. All variables are then available to your PHP app via `getenv()` or `$_ENV`.

### Example `.env` File

```env
# App config
APP_NAME=MyApp
APP_ENV=production
APP_DEBUG=false

# Third-party API keys
STRIPE_KEY=sk_live_xxxxxxxxxxxx
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=yourpassword
```

### Accessing Variables in PHP

```php
$appName  = getenv('APP_NAME');
$stripe   = getenv('STRIPE_KEY');

// Or via $_ENV superglobal
$debug = $_ENV['APP_DEBUG'];
```

### ⚠️ Important Rules

- One variable per line — `KEY=value` format
- Use `#` for comments — `# this is a comment`
- **No spaces** around `=` — `KEY=value` ✅ &nbsp; `KEY = value` ❌
- **No inline comments** — `KEY=value # comment` ❌ (comment becomes part of value)
- **Never commit `.env` to Git** — add it to `.gitignore`

> 💡 `.env` variables are loaded **after** the `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` env vars set in Space Settings — so they can override them if needed.

---

## 📁 File Manager

This setup uses [TinyFileManager](https://github.com/prasathmani/tinyfilemanager) — accessible at `/files`.

By default, authentication is **disabled** for easy development.

### 🔐 Enable Login (Required for Public Servers!)

1. Open **Web Terminal** (`/terminal`) or **File Manager** (`/files`)
2. Navigate to:
   ```
   /usr/share/webapps/filemanager/
   ```
3. Open `index.php` and find:
   ```php
   $use_auth = false;
   ```
4. Change it to:
   ```php
   $use_auth = true;
   ```
5. Save — the login screen is now active! ✅

### Default File Manager Credentials

```
Username : admin
Password : admin@123
```

> 💡 Change the password via the **Settings ⚙️** icon inside TinyFileManager.

---

## 💻 Web Terminal

A custom PHP-powered browser shell is available at `/terminal` — no SSH required.

### 📊 System Monitoring

```bash
free -h        # RAM usage (Total / Used / Free)
df -h          # Total disk storage
du -sh *       # File sizes in current folder
```

### 📂 File Navigation

```bash
pwd            # Current directory
ls -la         # List files with permissions
cd folder      # Navigate into a folder
```

### 🛠️ Developer Commands

```bash
php -v         # Check PHP version
composer -v    # Check Composer version
git --version  # Check Git version
unzip file.zip # Extract a zip archive
nano file.php  # Edit a file in terminal
```

---

## 🔀 Custom Domain via Cloudflare Workers

> 🎭 **Hide your Hugging Face URL** — Serve your app from your own domain (e.g. `yoursite.com`) while the actual server stays on Hugging Face behind the scenes.

This method uses a **Cloudflare Worker** as a reverse proxy. All traffic hits your domain first, gets forwarded to your HF Space, and the response is served back — visitors never see the `*.hf.space` URL.

**Prerequisites:**
- A domain added to Cloudflare (with DNS managed by Cloudflare)
- A free Cloudflare account → [cloudflare.com](https://cloudflare.com)

---

### Step 1 — Connect Your Domain to Cloudflare

If your domain is not already on Cloudflare:

1. Log in to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Click **"Add a Site"** → enter your domain name
3. Select the **Free plan** → click **Continue**
4. Cloudflare will scan your existing DNS records — review and confirm
5. Copy the two **Cloudflare nameservers** shown (e.g. `alice.ns.cloudflare.com`)
6. Go to your domain registrar (GoDaddy, Namecheap, etc.) → update the nameservers to the ones Cloudflare gave you
7. Wait for propagation — usually takes **5–30 minutes** (up to 48 hours in rare cases)
8. Once active, Cloudflare will send a confirmation email ✅

---

### Step 2 — Create a Cloudflare Worker

1. In Cloudflare dashboard → go to **Workers & Pages** (left sidebar)
2. Click **"Create application"**
3. Click **"Create Worker"**
4. Give your worker a name (e.g. `my-php-proxy`)
5. Click **"Deploy"** — this creates a default Hello World worker

---

### Step 3 — Replace the Worker Code

1. After deploying, click **"Edit code"**
2. Delete all the existing code in the editor
3. Paste the following worker script:

```js
export default {
  async fetch(request) {
    try {
      const url = new URL(request.url);

      // 🔁 Replace this with your actual Hugging Face Space URL
      const backendHost = "YOUR_USERNAME-YOUR_SPACE_NAME.hf.space";

      const backendUrl = new URL(request.url);
      backendUrl.hostname = backendHost;
      backendUrl.protocol = "https:";

      const newHeaders = new Headers(request.headers);
      newHeaders.set("X-Forwarded-Host", url.hostname);
      newHeaders.set("X-Forwarded-Proto", "https");

      if (newHeaders.has("origin")) {
        newHeaders.set("origin", `https://${backendHost}`);
      }

      if (newHeaders.has("referer")) {
        try {
          const referer = new URL(newHeaders.get("referer"));
          referer.hostname = backendHost;
          referer.protocol = "https:";
          newHeaders.set("referer", referer.toString());
        } catch {}
      }

      const body = request.method === "GET" || request.method === "HEAD"
        ? undefined
        : await request.arrayBuffer();

      const response = await fetch(new Request(backendUrl.toString(), {
        method: request.method,
        headers: newHeaders,
        body: body,
        redirect: "manual",
      }));

      const headers = new Headers();

      for (const [key, value] of response.headers.entries()) {
        if (key.toLowerCase() === "set-cookie") continue;
        if (key.toLowerCase() === "location") {
          try {
            const loc = new URL(value);
            loc.hostname = url.hostname;
            loc.protocol = url.protocol;
            headers.set("location", loc.toString());
          } catch {
            headers.set("location", value);
          }
          continue;
        }
        headers.set(key, value);
      }

      for (const cookie of response.headers.getAll("set-cookie")) {
        headers.append("set-cookie", cookie
          .replace(/;\s*Domain=[^;]*/gi, "")
          .replace(/;\s*SameSite=[^;]*/gi, "")
          .concat("; SameSite=Lax")
        );
      }

      // Security headers
      headers.delete("x-powered-by");
      headers.delete("server");
      headers.delete("cf-cache-status");
      headers.set("X-Frame-Options", "SAMEORIGIN");
      headers.set("X-Content-Type-Options", "nosniff");
      headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
      headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
      headers.set("X-XSS-Protection", "1; mode=block");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });

    } catch (err) {
      return new Response(`Worker Error: ${err.message}`, { status: 500 });
    }
  },
};
```

4. **Important:** Replace `YOUR_USERNAME-YOUR_SPACE_NAME.hf.space` on line 6 with your actual HF Space URL.  
   For example: `shkumaraman-backend.hf.space`

5. Click **"Deploy"** ✅

---

### Step 4 — Attach Your Domain to the Worker

You need to complete **both** parts below — Simple domain mapping AND the Route pattern. Both are required for the worker to handle your domain correctly.

---

#### Part A — Simple Domain Mapping

1. In your Worker → go to **"Settings"** tab
2. Under **"Domains & Routes"** → click **"Add"**
3. A dialog appears — select **"Custom Domain"**
4. You will see a domain input field — **leave it empty**
5. Click **"Add domain"**

> This registers your domain with the Worker directly.

---

#### Part B — Route Pattern (Advanced URL Matching)

1. Under **"Domains & Routes"** → click **"Add"** again
2. This time select **"Route"**
3. The **"Advanced URL matching"** section appears
4. In the **Route pattern** field — it will **auto-fill** with:
   ```
   *.yourdomain.com/*
   ```
5. Click **"Add domain"** ✅

> 💡 The `*.yourdomain.com/*` pattern covers all subdomains and all paths automatically. Do not change it unless you need a more specific rule.

---

### Step 5 — Done! 🎉

Your custom domain now proxies all traffic to your Hugging Face Space.

```
https://yourdomain.com/        → Your website
https://yourdomain.com/sql     → phpMyAdmin
https://yourdomain.com/files   → File Manager
https://yourdomain.com/terminal → Web Terminal
```

The original `*.hf.space` URL still works too — the Worker doesn't disable it, it just adds your custom domain on top.

---

### 🔐 What the Worker Does (Security Overview)

| Feature | What it does |
|---|---|
| **Proxy** | Forwards all requests to your HF Space and returns the response |
| **URL masking** | Rewrites `Location` headers on redirects so visitors stay on your domain |
| **Cookie handling** | Strips `Domain` and `SameSite` attributes so cookies work cross-domain |
| **Security headers** | Adds `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`, and more |
| **Header cleanup** | Removes `x-powered-by` and `server` headers to reduce fingerprinting |

---

### 🛠️ Troubleshooting

**Domain not routing to the worker?**
- Make sure your domain's nameservers are pointing to Cloudflare
- Check that the route pattern matches your domain exactly
- Wait a few minutes after saving — changes propagate quickly but not instantly

**Getting a Cloudflare error page?**
- Double-check the `backendHost` in the worker code — it must match your exact HF Space URL (no `https://`, no trailing slash)
- Make sure your HF Space is running and accessible directly at `your-username-your-space.hf.space`

**Cookies or sessions not working?**
- The worker already handles cookie rewriting. If issues persist, try clearing browser cookies for your domain.

**Worker only needed on one subdomain?**
- Change the route pattern to `app.yourdomain.com/*` instead of `*.yourdomain.com/*`
- Make sure a DNS record exists for that subdomain (add an `A` record pointing to `192.0.2.1` as a placeholder — Cloudflare's proxy will intercept it before it reaches that IP)

---

## 💡 Pro Tips

- 📂 **Website Root:** Place your project files at `/var/www/localhost/htdocs`
- 💾 **Persistent Storage Required:** Mount `/data` in Space Settings — without it, database resets on every restart
- 🗜️ **Fast Deploys:** Upload a `.zip` via File Manager and extract it directly on the server
- ⚡ **OPcache:** Already enabled — PHP apps run 2x–3x faster with zero extra config
- 🔒 **Going Public?** Enable File Manager login and set a strong `MYSQL_PASSWORD`
- 🛠️ **Composer & Git** are pre-installed — install PHP packages directly from the terminal
- 🖥️ **No SSH Needed:** The Web Terminal handles all server management from your browser
- 🔄 **mod_rewrite:** Enabled by default — Laravel, WordPress, and other frameworks work out of the box
- 🔀 **Custom Domain:** Use a Cloudflare Worker to mask your HF Space URL with your own domain — completely free

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request 🎉

---

<div align="center">

**Made with ❤️ for developers who love simplicity**

⭐ **If this helped you, please give it a Star!** ⭐

</div>
