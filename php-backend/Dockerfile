FROM alpine:latest

ENV MYSQL_USER=admin \
    MYSQL_PASSWORD=admin \
    MYSQL_DATABASE=admin \
    SQL_PATH=sql \
    FILES_PATH=files \
    TERMINAL_PATH=terminal

RUN apk add --no-cache \
    mariadb mariadb-client apache2 php-apache2 \
    php-mysqli php-pdo_mysql php-mbstring php-xml \
    php-gd php-curl php-session phpmyadmin curl \
    zip unzip php-zip php-ctype php-fileinfo php-json \
    php-opcache php-phar php-openssl php-iconv \
    git composer nano

RUN sed -i 's/Listen 80/Listen 7860/' /etc/apache2/httpd.conf && \
    sed -i 's/#LoadModule rewrite_module/LoadModule rewrite_module/' /etc/apache2/httpd.conf && \
    sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/httpd.conf && \
    printf "\n\
<Directory /usr/share/webapps/phpmyadmin>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n\
<Directory /usr/share/webapps/filemanager>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n\
<Directory /usr/share/webapps/terminal>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n\
<Directory /var/www/localhost/htdocs>\n\
    Options Indexes FollowSymLinks\n\
    IndexOptions FancyIndexing FoldersFirst NameWidth=* DescriptionWidth=* VersionSort\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n\
DirectoryIndex index.php index.html\n" >> /etc/apache2/httpd.conf

RUN sed -i "s|'localhost'|'127.0.0.1'|g" /etc/phpmyadmin/config.inc.php && \
    cat << 'EOF' >> /etc/phpmyadmin/config.inc.php
$cfg['blowfish_secret'] = '12345678901234567890123456789012';
$cfg['Servers'][1]['host'] = '127.0.0.1';
$cfg['Servers'][1]['port'] = '3306';
$cfg['TrustedProxies'] = array('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '127.0.0.1');
$cfg['PmaAbsoluteUri'] = './';
$cfg['CookieSameSite'] = 'None';
EOF

RUN find /etc/php* -name php.ini -exec sh -c 'echo "session.cookie_secure = On" >> "{}" && echo "session.cookie_samesite = \"None\"" >> "{}" && echo "opcache.enable=1" >> "{}"' \;

RUN mkdir -p /run/mysqld /run/apache2 /data/mysql /var/www/localhost/htdocs /usr/share/webapps/filemanager /usr/share/webapps/terminal /etc/apache2/conf.d && \
    curl -sL https://raw.githubusercontent.com/prasathmani/tinyfilemanager/master/tinyfilemanager.php -o /usr/share/webapps/filemanager/index.php && \
    sed -i "s/\$use_auth = true;/\$use_auth = false;/g" /usr/share/webapps/filemanager/index.php && \
    rm -f /var/www/localhost/htdocs/index.html

RUN cat << 'EOF' > /usr/share/webapps/terminal/index.php
<?php
session_start();
if(isset($_POST['cmd'])){
    $cwd = $_SESSION['cwd'] ?? '/var/www/localhost/htdocs';
    $cmd = trim($_POST['cmd']);
    $escaped_cwd = escapeshellarg($cwd);
    $full = "cd {$escaped_cwd} 2>/dev/null; {$cmd}; printf '__PWD__%s' \"\$(pwd)\"";
    $raw = shell_exec($full . ' 2>&1') ?? '';
    $pos = strrpos($raw, '__PWD__');
    if($pos !== false){
        $out = substr($raw, 0, $pos);
        $_SESSION['cwd'] = trim(substr($raw, $pos + 7));
    } else {
        $out = $raw;
    }
    echo json_encode(['out' => htmlspecialchars($out), 'cwd' => $_SESSION['cwd']]);
    exit;
}
$init_cwd = '/var/www/localhost/htdocs';
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Web Terminal</title>
<style>
    body { background: #1e1e1e; color: #00ff00; font-family: monospace; padding: 20px; font-size: 16px; margin: 0; }
    input { background: transparent; color: #00ff00; border: none; outline: none; width: 80%; font-family: monospace; font-size: 16px; }
    #output { white-space: pre-wrap; margin-bottom: 10px; }
    #prompt { color: #00ff00; }
</style>
</head>
<body>
<div id="output">Alpine Server Terminal - Ready.<br></div>
<span id="prompt">$ /var/www/localhost/htdocs </span><input type="text" id="cmd" autofocus autocomplete="off">
<script>
const cmdInput = document.getElementById('cmd');
const output = document.getElementById('output');
const prompt = document.getElementById('prompt');
let cwd = '<?= $init_cwd ?>';

function updatePrompt(dir) {
    cwd = dir;
    prompt.textContent = '$ ' + dir + ' ';
}

cmdInput.addEventListener('keypress', function(e) {
    if(e.key === 'Enter') {
        const cmd = this.value.trim();
        if(!cmd) return;
        this.value = '';
        output.innerHTML += '\n<span style="color:#00ff00;">$ ' + cwd + ' ' + cmd + '</span>\n';
        fetch('index.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'cmd=' + encodeURIComponent(cmd)
        })
        .then(r => r.json())
        .then(data => {
            if(data.out) output.innerHTML += data.out;
            updatePrompt(data.cwd);
            window.scrollTo(0, document.body.scrollHeight);
        });
    }
});
</script>
</body>
</html>
EOF

RUN chown -R 1000:1000 /run/mysqld /run/apache2 /data/mysql /var/www/localhost/htdocs /var/log/apache2 /etc/phpmyadmin /etc/apache2/conf.d /usr/share/webapps/phpmyadmin /usr/share/webapps/filemanager /usr/share/webapps/terminal

RUN cat << 'EOF' > /start.sh
#!/bin/sh
set -e
rm -f /run/mysqld/mysqld.sock /run/mysqld/mysqld.pid /run/apache2/httpd.pid /data/mysql/tc.log 2>/dev/null || true

# Load .env file from web root if it exists
if [ -f /var/www/localhost/htdocs/.env ]; then
    set -a
    . /var/www/localhost/htdocs/.env
    set +a
fi

# Generate dynamic Apache aliases from env vars (defaults: sql, files, terminal)
cat > /etc/apache2/conf.d/tool-aliases.conf << APACHECONF
Alias /${SQL_PATH:-sql} /usr/share/webapps/phpmyadmin
Alias /${FILES_PATH:-files} /usr/share/webapps/filemanager
Alias /${TERMINAL_PATH:-terminal} /usr/share/webapps/terminal
APACHECONF

if [ ! -d /data/mysql/mysql ]; then
    rm -rf /data/mysql/* /data/mysql/.* 2>/dev/null || true
    mariadb-install-db --datadir=/data/mysql --skip-test-db --user=1000 --auth-root-authentication-method=normal
fi

cat << SQL > /tmp/init.sql
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SQL

mariadbd --datadir=/data/mysql --bind-address=127.0.0.1 --port=3306 --socket=/run/mysqld/mysqld.sock --skip-networking=OFF --innodb-use-native-aio=0 --init-file=/tmp/init.sql &

until mariadb-admin ping --socket=/run/mysqld/mysqld.sock -u root --silent; do
    sleep 2
done

rm -f /tmp/init.sql
exec httpd -D FOREGROUND
EOF

RUN chmod +x /start.sh && chown 1000:1000 /start.sh

WORKDIR /var/www/localhost/htdocs
USER 1000
EXPOSE 7860
CMD ["/start.sh"]
