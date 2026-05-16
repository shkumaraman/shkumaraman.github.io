====================================================================
PHP WEB SERVER (ALPINE LAMP STACK + WEB TERMINAL)
Welcome to the ultimate lightweight PHP Web Server setup! This Docker-based configuration gives you a complete, high-performance web environment (Apache, PHP 8+, MariaDB) along with built-in tools like a File Manager and Web Terminal—all running smoothly in a single container.

Perfect for Hugging Face Spaces, VPS, or local development.

IMPORTANT URLS & ACCESS PATHS

Once your Docker container is running (exposed on port 7860), you can access your tools using the following paths:

Main Website:    http://:7860/

Database:        http://:7860/sql

File Manager:    http://:7860/files

Web Terminal:    http://:7860/terminal

(Note: If testing locally, replace  with localhost)

DATABASE LOGIN & SECURITY (ENV VARIABLES)

Database (MySQL & phpMyAdmin)

Username: admin (Default)

Password: admin (Default)

SECURITY TIP (IMPORTANT):
It is highly recommended to change these default credentials before going live. You do NOT need to edit the code to change them!

These are securely configured using Environment Variables (ENV). To change them, simply update the following variables in your Docker run command, VPS environment settings, or Hugging Face Space Variables:

MYSQL_USER

MYSQL_PASSWORD

MYSQL_DATABASE

FILE MANAGER - HOW TO ENABLE THE LOGIN SCREEN

By default, the File Manager login is bypassed (disabled) to make initial development fast and easy. However, if your server is public, anyone can access your files.

To secure your files and bring back the login page, follow these steps:

Step 1: Open your File Manager (/files) or Web Terminal (/terminal).
Step 2: Navigate to this directory: /usr/share/webapps/filemanager/
Step 3: Open the 'index.php' file to edit it.
Step 4: Find this exact line in the code:
$use_auth = false;
Step 5: Change the 'false' to 'true' so it looks like this:
$use_auth = true;
Step 6: Save the file.

The login screen will now be active!

Default Username: admin

Default Password: admin@123
(You can easily change this password by clicking the 'Settings' gear icon inside the File Manager after logging in).

WEB TERMINAL GUIDE & BASIC COMMANDS

Your setup includes a custom, browser-based Web Terminal. You don't need SSH access to manage your server! Simply go to /terminal and start typing.

System Monitoring (Storage & RAM):

free -h   : Checks the server's RAM (Memory). Shows Total, Used, and Free RAM.

df -h     : Checks your total server Hard Disk / SSD storage space.

du -sh *  : Checks exactly how much storage the files in your current folder are taking.

File & Folder Navigation:

pwd       : Shows your current folder path.

ls -la    : Lists all files/folders in your current directory with permissions.

cd folder : Moves you into a specific folder.

Developer Commands:

php -v            : Checks the currently installed PHP version.

unzip file.zip    : Extracts a zip file directly from the terminal.

PRO TIPS FOR BUYERS

Website Root Directory: Your main website files must be placed inside '/var/www/localhost/htdocs'. You can use the File Manager to directly upload your .zip project here and extract it.

Speed & Performance: This server comes with PHP OPcache pre-enabled. This means your PHP applications and APIs will run 2x to 3x faster right out of the box without any extra configuration!

====================================================================
