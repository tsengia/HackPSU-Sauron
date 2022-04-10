# Install apt packages we need
apt-get install -y wget default-mysql-client python-pip

# Install pip packages
pip3 install -r requirements.txt

# Enable Grafana on startup
systemctl enable grafana-server.service
systemctl daemon-reload
systemctl start grafana-server
