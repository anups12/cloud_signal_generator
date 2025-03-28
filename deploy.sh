set -e

DOMAIN="your-domain.com"
EMAIL="your-email@example.com"
PROJECT_DIR="/var/www/flask-signal-broadcaster"

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git ufw

sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo tee /etc/systemd/system/signal-broadcaster.service > /dev/null <<EOF
[Unit]
Description=Gunicorn Flask Signal Broadcaster
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start signal-broadcaster
sudo systemctl enable signal-broadcaster

sudo tee /etc/nginx/sites-available/signal-broadcaster > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/signal-broadcaster /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

sudo ufw allow 'Nginx Full'
sudo ufw enable

echo "Deployment Complete: https://$DOMAIN"