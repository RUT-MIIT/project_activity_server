#!/usr/bin/env bash
# Обновление продакшена: git pull, миграции, перезапуск gunicorn (systemd).
# Имя unit для systemctl задаётся в .env переменной GUNICORN_SERVICE
# (например: GUNICORN_SERVICE=project_activity_server).

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

ENV_FILE="${PROJECT_DIR}/.env"

read_env_value() {
  # Читает KEY=value из .env (допускает пробелы вокруг =, кавычки в значении).
  local key="$1"
  if [[ ! -f "$ENV_FILE" ]]; then
    return 1
  fi
  local line
  line="$(grep -E "^[[:space:]]*(export[[:space:]]+)?${key}[[:space:]]*=" "$ENV_FILE" 2>/dev/null | head -1)" || true
  if [[ -z "$line" ]]; then
    return 1
  fi
  local val="${line#*=}"
  val="${val#"${val%%[![:space:]]*}"}"
  val="${val%"${val##*[![:space:]]}"}"
  val="${val#\"}"
  val="${val%\"}"
  val="${val#\'}"
  val="${val%\'}"
  val="${val//$'\r'/}"
  printf '%s' "$val"
}

if [[ ! -d "${PROJECT_DIR}/venv" ]]; then
  log_error "Каталог venv не найден: ${PROJECT_DIR}/venv"
  exit 1
fi

GUNICORN_SERVICE="$(read_env_value GUNICORN_SERVICE || true)"
if [[ -z "${GUNICORN_SERVICE}" ]]; then
  log_error "В ${ENV_FILE} не задана переменная GUNICORN_SERVICE (имя systemd unit для gunicorn)."
  log_error "Добавьте строку, например: GUNICORN_SERVICE=project_activity_server"
  exit 1
fi

log_info "Директория проекта: ${PROJECT_DIR}"
log_info "git pull..."
git pull

log_info "Активация venv..."
# shellcheck source=/dev/null
source "${PROJECT_DIR}/venv/bin/activate"

log_info "Миграции Django..."
python manage.py migrate

log_info "Перезапуск systemd: ${GUNICORN_SERVICE}"
sudo systemctl restart "${GUNICORN_SERVICE}"

log_info "Готово. Статус: sudo systemctl status ${GUNICORN_SERVICE}"
