#!/bin/bash
# Скрипт установки Шале Релакс на VPS (Ubuntu 22.04)
# Запускать: bash deploy.sh

set -e

PROJECT_DIR="/opt/shale-relax"
SERVICE_USER="shale"

echo "=== 1. Обновление системы ==="
apt-get update -q && apt-get install -y python3.11 python3.11-venv git

echo "=== 2. Создание пользователя ==="
id -u $SERVICE_USER &>/dev/null || useradd -m -s /bin/bash $SERVICE_USER

echo "=== 3. Копирование файлов ==="
mkdir -p $PROJECT_DIR
cp -r . $PROJECT_DIR/
chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

echo "=== 4. Виртуальное окружение ==="
sudo -u $SERVICE_USER bash -c "
  cd $PROJECT_DIR
  python3.11 -m venv .venv
  .venv/bin/pip install -q --upgrade pip
  .venv/bin/pip install -q -r requirements.txt
"

echo "=== 5. Директории данных ==="
sudo -u $SERVICE_USER mkdir -p $PROJECT_DIR/data/photos $PROJECT_DIR/logs $PROJECT_DIR/ready_to_post

echo "=== 6. Установка systemd-сервиса ==="
cp shale-relax.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable shale-relax
systemctl start shale-relax

echo ""
echo "✅ Готово! Статус:"
systemctl status shale-relax --no-pager
