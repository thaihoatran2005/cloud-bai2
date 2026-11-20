# Ghi chu ca nhan - Bai ca nhan 2 (MSSV 2324802010030)

Ung dung web 3 tang: Nginx -> Frontend (HTML/JS) -> Backend (Flask + Gunicorn) -> MariaDB.
Chuc nang: dang ky, dang nhap (mat khau bam), them/xem/sua/xoa ghi chu.

## Cai lai tu dau (Ubuntu Server)
1. Cai goi:
   sudo apt update && sudo apt install -y nginx mariadb-server python3-venv python3-pip git ufw
2. Tao CSDL: sua mat khau trong schema.sql roi chay: sudo mariadb < schema.sql
3. Backend:
   sudo mkdir -p /opt/app && sudo chown $USER:$USER /opt/app
   cp app.py requirements.txt /opt/app/ && cd /opt/app
   python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
   cp .env.example .env  (dien SECRET_KEY, DB_HOST=127.0.0.1, DB_USER=appuser, DB_PASS, DB_NAME=appdb)
   chmod 600 .env && sudo chown -R www-data:www-data /opt/app
4. Dich vu: sudo cp deploy/notes.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now notes
5. Frontend: sudo mkdir -p /var/www/frontend && sudo cp frontend/index.html /var/www/frontend/
6. Nginx: sudo cp deploy/nginx-notes.conf /etc/nginx/sites-available/notes
   sudo ln -sf /etc/nginx/sites-available/notes /etc/nginx/sites-enabled/notes
   sudo rm -f /etc/nginx/sites-enabled/default && sudo nginx -t && sudo systemctl reload nginx
7. Tuong lua:
   sudo ufw default deny incoming && sudo ufw default allow outgoing
   sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
   sudo ufw allow 80/tcp && sudo ufw enable
8. Mo trinh duyet: http://<IP VPS>

Luu y: file .env khong dua len GitHub.
