<div align="center">

<img src="https://img.shields.io/badge/PHP-8%2B-777BB4?style=for-the-badge&logo=php&logoColor=white" />
<img src="https://img.shields.io/badge/Apache-Web%20Server-D22128?style=for-the-badge&logo=apache&logoColor=white" />
<img src="https://img.shields.io/badge/MariaDB-Database-003545?style=for-the-badge&logo=mariadb&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-Alpine-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

# 🐘 PHP Web Server — Alpine LAMP Stack

### ⚡ Lightweight · 🔒 Secure · 🚀 Production-Ready

> **A complete PHP development environment in a single Docker container** — Apache, PHP 8+, MariaDB, File Manager & Web Terminal. Deploy anywhere in minutes.

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🌐 Access URLs](#-access-urls)
- [🗄️ Database Setup](#️-database-setup)
- [📁 File Manager](#-file-manager)
- [💻 Web Terminal](#-web-terminal)
- [⚙️ Configuration](#️-configuration)
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
| ☁️ **Hugging Face Ready** | Runs seamlessly on HF Spaces, VPS, or locally |

---

## 🚀 Quick Start

### Using Docker

```bash
docker run -d \
  -p 7860:7860 \
  -e MYSQL_USER=admin \
  -e MYSQL_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=mydb \
  --name php-lamp \
  your-image-name
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  php-lamp:
    image: your-image-name
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

---

## 🌐 Access URLs

Once the container is running on port `7860`, access your tools at:

| Tool | URL | Description |
|---|---|---|
| 🏠 **Website** | `http://localhost:7860/` | Your main web root |
| 🗄️ **Database** | `http://localhost:7860/sql` | phpMyAdmin interface |
| 📁 **File Manager** | `http://localhost:7860/files` | Browser-based file manager |
| 💻 **Web Terminal** | `http://localhost:7860/terminal` | In-browser shell |

> 💡 **Deployed on a server?** Replace `localhost` with your server's IP address or domain.

---

## 🗄️ Database Setup

### Default Credentials

```
Username : admin
Password : admin
```

> ⚠️ **Security Warning:** Change these credentials before going live!

### Changing Credentials (No Code Edits Needed!)

Simply update the following **environment variables** in your Docker run command, VPS settings, or Hugging Face Space Variables:

| Variable | Description | Default |
|---|---|---|
| `MYSQL_USER` | Database username | `admin` |
| `MYSQL_PASSWORD` | Database password | `admin` |
| `MYSQL_DATABASE` | Database name | *(set by you)* |

---

## 📁 File Manager

By default, the File Manager login is **disabled** for fast local development.

### 🔐 Enable Login (Recommended for Public Servers)

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
5. Save the file — the login screen is now active!

### File Manager Default Credentials

```
Username : admin
Password : admin@123
```

> 💡 You can change the password anytime via the **Settings (⚙️)** icon inside the File Manager.

---

## 💻 Web Terminal

No SSH required! Access your server shell directly from the browser at `/terminal`.

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

## ⚙️ Configuration

### Website Root Directory

Upload your project files to:

```
/var/www/localhost/htdocs
```

You can upload a `.zip` file via the File Manager and extract it directly there.

### PHP OPcache

PHP OPcache comes **pre-enabled** out of the box — no configuration needed. This can improve PHP performance by **2x to 3x** without any extra setup.

---

## 💡 Pro Tips

- 🚀 **Fast deploys** — Upload your project as a `.zip` and extract it in the File Manager
- 🔒 **Secure first** — Always change default passwords before exposing to the internet
- ☁️ **Hugging Face** — Works perfectly as an HF Space; set ENV vars in the Space settings
- ⚡ **OPcache** is pre-configured — your PHP apps are already optimized on first run
- 🖥️ **No SSH needed** — The Web Terminal covers all your server management needs

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

<div align="center">

**Made with ❤️ for developers who love simplicity**

⭐ **Star this repo if it helped you!** ⭐

</div>
