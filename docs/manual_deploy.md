## Руководство по ручному развертыванию Project Activity Server

### 1. Подготовка окружения
- Авторизуйтесь на сервере под пользователем `nnd`.
- Убедитесь, что установлены `git`, `python3`, `python3-venv`, `pip`, `postgresql`, `psql`, `systemd`.
- При необходимости обновите пакеты:
  ```bash
  sudo apt update && sudo apt upgrade
  sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib git
  ```

### 2. Получение исходного кода
```bash
cd /home/nnd
git clone <URL_репозитория> project_activity_server
cd project_activity_server
```

### 3. Создание и активация виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка переменных окружения (.env)
Создайте файл `.env` в корне проекта:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pd
DB_USER=pd_user
DB_PASSWORD=211211!!!
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=замени_на_производственный
DEBUG=False
ALLOWED_HOSTS=pd.emiit.ru,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
FRONT_END=https://pd.emiit.ru
```

### 5. Настройка PostgreSQL
```bash
sudo -u postgres psql
```
В консоли `psql` выполните:
```sql
CREATE USER pd_user WITH PASSWORD '211211!!!';
ALTER USER pd_user CREATEDB;
CREATE DATABASE pd OWNER pd_user;
GRANT ALL PRIVILEGES ON DATABASE pd TO pd_user;
\q
```

### 6. Миграции и статические файлы
```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```
> Статические файлы собираются в директорию `/home/nnd/project_activity_server/staticfiles` (значение `STATIC_ROOT` по умолчанию) и обслуживаются по URL `/backend-static/`. Команда `collectstatic` создаст директорию при необходимости.

### 7. Тестовый запуск приложения
```bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```
Проверьте доступность приложения, затем остановите процесс `Ctrl+C`.

### 8. Настройка systemd сервиса Gunicorn
Создайте файл `/etc/systemd/system/project_activity_server.service`:
```
[Unit]
Description=Project Activity Server (Django + Gunicorn)
After=network.target postgresql.service

[Service]
User=nnd
Group=nnd
WorkingDirectory=/home/nnd/project_activity_server
Environment="PATH=/home/nnd/project_activity_server/venv/bin"
ExecStart=/home/nnd/project_activity_server/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /home/nnd/project_activity_server/logs/gunicorn_access.log \
    --error-logfile /home/nnd/project_activity_server/logs/gunicorn_error.log \
    config.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 9. Логи и запуск сервиса
```bash
mkdir -p /home/nnd/project_activity_server/logs
sudo systemctl daemon-reload
sudo systemctl enable project_activity_server
sudo systemctl start project_activity_server
sudo systemctl status project_activity_server
```

### 10. Проверка и сопровождение
- Проверить логи: `sudo journalctl -u project_activity_server -f`
- При обновлении кода:
  ```bash
  cd /home/nnd/project_activity_server
  git pull
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py collectstatic --noinput
  sudo systemctl restart project_activity_server
  ```

### 11. Настройка nginx (backend + SPA)
Создайте или обновите конфиг `/etc/nginx/sites-available/pd.emiit.ru`:
```
server {
    server_name pd.emiit.ru;

    location /api/ {
        proxy_pass http://unix:/home/nnd/project_activity/project_activity_server/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://unix:/home/nnd/project_activity/project_activity_server/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # React SPA
    location / {
        root /home/nnd/project_activity/project_activity_client/dist;
        try_files $uri /index.html;
        add_header Cache-Control "no-cache";
    }

    # Статика React-билда
    location /static/ {
        alias /home/nnd/project_activity/project_activity_client/dist/static/;
        try_files $uri $uri/ =404;
    }

    # Django статика
    location /backend-static/ {
        alias /home/nnd/project_activity/project_activity_server/staticfiles/;
    }

    location /media/ {
        alias /home/nnd/project_activity/project_activity_server/media/;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/pd.emiit.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pd.emiit.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = pd.emiit.ru) {
        return 301 https://$host$request_uri;
    }

    server_name pd.emiit.ru;
    listen 80;
    return 404;
}
```
После правок проверьте конфигурацию `sudo nginx -t` и перезапустите сервис `sudo systemctl reload nginx`.

