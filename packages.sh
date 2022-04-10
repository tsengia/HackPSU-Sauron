
# Install apt packages we need
sudo apt-get install -y adduser libfontconfig1 wget default-mysql-client python3-pip python3-dev default-libmysqlclient-dev build-essential ffmpeg unzip

# Install youtube-dl
curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/bin/youtube-dl
chmod a+rx /usr/bin/youtube-dl

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
curl -L https://grafana.com/api/plugins/dalvany-image-panel/versions/2.4.0/download -o dalvany-image-panel.zip

# Create the plugins directory b/c it doesn't exist by default
mkdir -p /var/lib/grafana/plugins

# unzip the plugin into the directory
unzip dalvany-image-panel.zip -d /var/lib/grafana/plugins/dalvany-image-panel

# Clean up
rm dalvany-image-panel.zip

# Enable Grafana on startup
systemctl enable grafana-server.service
systemctl daemon-reload
systemctl start grafana-server
