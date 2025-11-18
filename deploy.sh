#!/bin/bash

# Скрипт развертывания Django приложения на Linux сервере
# Автор: автоматически сгенерирован
# Дата: $(date +%Y-%m-%d)

set -e  # Остановка при любой ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка, что скрипт запущен от пользователя nnd
if [ "$USER" != "nnd" ]; then
    log_error "Скрипт должен быть запущен от пользователя nnd. Текущий пользователь: $USER"
    exit 1
fi

# Определение пути к проекту
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log_info "Директория проекта: $PROJECT_DIR"

cd "$PROJECT_DIR"

# Проверка наличия PostgreSQL и psql
if ! command -v psql &> /dev/null; then
    log_error "psql не найден. Установите PostgreSQL."
    exit 1
fi

log_info "PostgreSQL найден"

# 1. Создание виртуального окружения
log_info "Создание виртуального окружения..."
if [ -d "venv" ]; then
    log_warn "Виртуальное окружение уже существует, пропускаем создание"
else
    python3 -m venv venv
    log_info "Виртуальное окружение создано"
fi

# Активация виртуального окружения
log_info "Активация виртуального окружения..."
source venv/bin/activate

# Обновление pip
log_info "Обновление pip..."
pip install --upgrade pip

# 2. Установка зависимостей
log_info "Установка зависимостей из requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    log_error "Файл requirements.txt не найден!"
    exit 1
fi

pip install -r requirements.txt
log_info "Зависимости установлены"

# 3. Создание .env файла
log_info "Создание .env файла..."
ENV_FILE="$PROJECT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    log_warn ".env файл уже существует, создаем резервную копию..."
    cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
fi

cat > "$ENV_FILE" << EOF
# Настройки базы данных PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pd
DB_USER=pd_user
DB_PASSWORD=211211!!!
DB_HOST=localhost
DB_PORT=5432

# Настройки Django
SECRET_KEY=django-insecure-fi%=(\$26*@4^71-g%(o0ed&6eej^ov4l1e*8r_mw#m=k#oi*)a
DEBUG=False
ALLOWED_HOSTS=*

# Настройки email (можно настроить позже)
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend

# Frontend URL
FRONT_END=http://localhost:3000
EOF

log_info ".env файл создан"

# 4. Создание пользователя и базы данных PostgreSQL
log_info "Создание пользователя и базы данных PostgreSQL..."

# Проверка существования пользователя
USER_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='pd_user'" 2>/dev/null || echo "")

if [ "$USER_EXISTS" != "1" ]; then
    log_info "Создание пользователя pd_user..."
    sudo -u postgres psql -c "CREATE USER pd_user WITH PASSWORD '211211!!!';" || {
        log_error "Не удалось создать пользователя pd_user"
        exit 1
    }
    log_info "Пользователь pd_user создан"
else
    log_warn "Пользователь pd_user уже существует"
fi

# Предоставление прав пользователю
sudo -u postgres psql -c "ALTER USER pd_user CREATEDB;" || log_warn "Не удалось предоставить права CREATEDB"

# Проверка существования базы данных
DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='pd'" 2>/dev/null || echo "")

if [ "$DB_EXISTS" != "1" ]; then
    log_info "Создание базы данных pd..."
    sudo -u postgres psql -c "CREATE DATABASE pd OWNER pd_user;" || {
        log_error "Не удалось создать базу данных pd"
        exit 1
    }
    log_info "База данных pd создана"
else
    log_warn "База данных pd уже существует"
fi

# Предоставление всех прав на базу данных
sudo -u postgres psql -d pd -c "GRANT ALL PRIVILEGES ON DATABASE pd TO pd_user;" || log_warn "Не удалось предоставить права на базу данных"

log_info "База данных PostgreSQL настроена"

# 5. Запуск миграций Django
log_info "Применение миграций Django..."
python manage.py migrate
log_info "Миграции применены"

# 6. Сбор статических файлов
log_info "Сбор статических файлов..."
python manage.py collectstatic --noinput
log_info "Статические файлы собраны"

# 7. Создание systemd service файла
log_info "Создание systemd service файла..."
SERVICE_FILE="/etc/systemd/system/project_activity_server.service"

# Создание временного файла сервиса
TEMP_SERVICE_FILE=$(mktemp)
cat > "$TEMP_SERVICE_FILE" << EOF
[Unit]
Description=Project Activity Server (Django + Gunicorn)
After=network.target postgresql.service

[Service]
User=nnd
Group=nnd
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind 0.0.0.0:8000 \\
    --timeout 120 \\
    --access-logfile $PROJECT_DIR/logs/gunicorn_access.log \\
    --error-logfile $PROJECT_DIR/logs/gunicorn_error.log \\
    config.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Копирование файла сервиса с правами sudo
sudo cp "$TEMP_SERVICE_FILE" "$SERVICE_FILE"
sudo chmod 644 "$SERVICE_FILE"
rm "$TEMP_SERVICE_FILE"

log_info "Systemd service файл создан: $SERVICE_FILE"

# Создание директории для логов
log_info "Создание директории для логов..."
mkdir -p "$PROJECT_DIR/logs"
chmod 755 "$PROJECT_DIR/logs"
log_info "Директория для логов создана"

# 8. Перезагрузка systemd и запуск сервиса
log_info "Перезагрузка systemd daemon..."
sudo systemctl daemon-reload

log_info "Запуск сервиса project_activity_server..."
sudo systemctl enable project_activity_server.service
sudo systemctl restart project_activity_server.service

# Проверка статуса сервиса
sleep 2
if sudo systemctl is-active --quiet project_activity_server.service; then
    log_info "Сервис успешно запущен!"
    log_info "Проверить статус: sudo systemctl status project_activity_server"
    log_info "Просмотр логов: sudo journalctl -u project_activity_server -f"
else
    log_error "Сервис не запустился. Проверьте логи: sudo journalctl -u project_activity_server"
    exit 1
fi

log_info "Развертывание завершено успешно!"

