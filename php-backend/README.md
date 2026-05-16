<div align="center">

<img src="https://img.shields.io/badge/PHP-8%2B-777BB4?style=for-the-badge&logo=php&logoColor=white" />
<img src="https://img.shields.io/badge/Apache-Web%20Server-D22128?style=for-the-badge&logo=apache&logoColor=white" />
<img src="https://img.shields.io/badge/MariaDB-Database-003545?style=for-the-badge&logo=mariadb&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-Alpine-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-Spaces-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

# 🐘 PHP Web Server — Alpine LAMP Stack

### ⚡ Lightweight · 🔒 Secure · 🚀 Production-Ready

> **A complete PHP development environment in a single Docker container** — Apache, PHP 8+, MariaDB, File Manager & Web Terminal. Deploy on Hugging Face Spaces, VPS, or locally in minutes.

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [☁️ Deploy on Hugging Face Spaces](#️-deploy-on-hugging-face-spaces) ⭐ Recommended
- [🖥️ Deploy on VPS / Local Machine](#️-deploy-on-vps--local-machine)
- [🌐 Access URLs](#-access-urls)
- [🗄️ Database Setup](#️-database-setup)
- [📁 File Manager](#-file-manager)
- [💻 Web Terminal](#-web-terminal)
- [💡 Pro Tips](#-pro-tips)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🐘 **PHP 8+** | Latest PHP with OPcache pre-enabled (2x–3x faster) |
| 🌐 **Apache** | Battle-tested web server, production-ready |
| 🗄️ **MariaDB** | Full relational database with phpMyAdmin UI |
| 📁 **File Manager** | Browser-based file management, no FTP needed |
| 💻 **Web Terminal** | SSH-free server control from your browser |
| 🐳 **Docker Alpine** | Ultra-lightweight base image, minimal footprint |
| ☁️ **Hugging Face Ready** | One-click deploy on HF Spaces — free hosting! |

---

## ☁️ Deploy on Hugging Face Spaces

> ⭐ **Recommended method** — Free hosting, no server required!

### Step 1 — Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Give your space a name (e.g. `my-php-server`)
4. Select **SDK → Docker**
5. Click **"Create Space"**

### Step 2 — Upload Your Files

Once the Space is created, upload your project files:

```
your-space/
├── Dockerfile         ✅ required
├── index.php          (or your project files)
└── ...
```

> 💡 You can drag & drop files directly in the **Files tab**, or use Git:

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Add your project files here
git add .
git commit -m "Initial upload"
git push
```

### Step 3 — Set ENV Variables

On Hugging Face, there is no `docker run` command. Environment variables are set in **Space Settings**:

1. Go to the **"Settings"** tab in your Space
2. Find the **"Variables and Secrets"** section
3. Add the following variables:

| Variable | Value |
|---|---|
| `MYSQL_USER` | `admin` *(or your preferred username)* |
| `MYSQL_PASSWORD` | `yourpassword` *(use a strong password!)* |
| `MYSQL_DATABASE` | `mydb` *(or your preferred DB name)* |

### Step 4 — Done! 🎉

Hugging Face will automatically build and deploy your app. Your live URL will be:

```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/
```

---

## 🖥️ Deploy on VPS / Local Machine

> For those who prefer their own server or want to test locally.

### Prerequisites

- Docker must be installed → [Get Docker](https://docs.docker.com/get-docker/)

### Option A — Docker Run (Quick & Simple)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. Build the image
docker build -t php-lamp .

# 3. Run the container
docker run -d \
  -p 7860:7860 \
  -e MYSQL_USER=admin \
  -e MYSQL_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=mydb \
  --name php-lamp \
  php-lamp
```

### Option B — Docker Compose (Recommended for VPS)

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

> ⚠️ **On VPS:** Make sure to open port `7860` in your firewall!

```bash
# Ubuntu / Debian
sudo ufw allow 7860
```

---

## 🌐 Access URLs

Once the container is running, access your tools at:

| Tool | URL | Description |
|---|---|---|
| 🏠 **Website** | `/` | Your main web root |
| 🗄️ **Database** | `/sql` | phpMyAdmin interface |
| 📁 **File Manager** | `/files` | Browser-based file manager |
| 💻 **Web Terminal** | `/terminal` | In-browser shell |

---

## 🗄️ Database Setup

### Default Credentials

```
Username : admin
Password : admin
```

> ⚠️ **Security Warning:** Change these before going live on a public server!

### How to Change Credentials

**On Hugging Face:**
Go to Space Settings → Variables and Secrets → update the values.

**On VPS / Local:**
Update the ENV variables in your `docker run` command or `docker-compose.yml`.

| Variable | Description |
|---|---|
| `MYSQL_USER` | Database username |
| `MYSQL_PASSWORD` | Database password |
| `MYSQL_DATABASE` | Database name |

---

## 📁 File Manager

By default, the File Manager login is **disabled** for fast local development.

### 🔐 Enable Login (Required for Public Servers!)

1. Open the **Web Terminal** (`/terminal`) or **File Manager** (`/files`)
2. Navigate to:
   ```
   /usr/share/webapps/filemanager/
   ```
3. Open `index.php` and find this line:
   ```php
   $use_auth = false;
   ```
4. Change it to:
   ```php
   $use_auth = true;
   ```
5. Save the file — the login screen is now active! ✅

### Default File Manager Credentials

```
Username : admin
Password : admin@123
```

> 💡 You can change the password anytime via the **Settings ⚙️** icon inside the File Manager.

---

## 💻 Web Terminal

Manage your server directly from the browser — no SSH required! Go to `/terminal` and start typing.

### 📊 System Monitoring

```bash
free -h        # Check RAM usage (Total / Used / Free)
df -h          # Check total disk storage
du -sh *       # Check storage used by files in current folder
```

### 📂 File Navigation

```bash
pwd            # Show current directory path
ls -la         # List all files with permissions
cd folder      # Navigate into a folder
```

### 🛠️ Developer Commands

```bash
php -v         # Check installed PHP version
unzip file.zip # Extract a zip archive
```

---

## 💡 Pro Tips

- 📂 **Website Root:** Place your project files at `/var/www/localhost/htdocs`
- 🗜️ **Fast Uploads:** Upload your project as a `.zip` and extract it via the File Manager
- ⚡ **OPcache:** Pre-enabled out of the box — PHP apps run 2x–3x faster with zero config
- 🔒 **Going Public?** Always enable File Manager login and change default DB passwords
- 🖥️ **No SSH Needed:** The Web Terminal covers all your server management needs

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
