
# Install apt packages we need
sudo apt-get install -y adduser libfontconfig1 wget default-mysql-client python3-pip python3-dev default-libmysqlclient-dev build-essential ffmpeg

do curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl

sudo chmod a+rx /usr/local/bin/youtube-dl
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install pip packages
pip3 install -r requirements.txt

# Grab Grafana
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_8.4.5_amd64.deb

# Install Grafana
dpkg -i grafana-enterprise_8.4.5_amd64.deb

# Delete old deb
rm grafana-enterprise_8.4.5_amd64.deb

# grab the dynamic image plugin
wget https://grafana.com/api/plugins/dalvany-image-panel/versions/2.4.0/download

# unzip it

# Enable Grafana on startup
systemctl enable grafana-server.service
systemctl daemon-reload
systemctl start grafana-server
