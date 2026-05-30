#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install openjdk-11-* -y
sudo apt install git wget -y
sudo apt install maven -y
sudo snap install aws-cli --classic
sudo groupadd tomcat
cd /tmp/
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.118/bin/apache-tomcat-9.0.118.tar.gz
sudo mkdir /opt/tomcat
cd /opt/tomcat
sudo tar xzvf /tmp/apache-tomcat-9.0.*tar.gz -C /opt/tomcat --strip-components=1
sudo chgrp -R tomcat /opt/tomcat
sudo chmod -R g+r conf
sudo chmod g+x conf
sudo chown -R tomcat webapps/ work/ temp/ logs/
sudo cat <<EOF > /etc/systemd/system/tomcat.service
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
Environment=CATALINA_PID=/opt/tomcat/temp/tomcat.pid
Environment=CATALINA_Home=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment=’CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC’
Environment=’JAVA_OPTS.awt.headless=true -Djava.security.egd=file:/dev/v/urandom’

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=root
UMask=0007
RestartSec=10
Restart=always

[Install]

WantedBy=multi-user.target
EOF
cd /tmp/
git clone -b main https://github.com/hkhcoder/vprofile-project.git
sed -i "s/db01/db01.aws-webapp.hz/g" /tmp/vprofile-project/src/main/resources/application.properties
sed -i "s/rmq01/rmq01.aws-webapp.hz/g" /tmp/vprofile-project/src/main/resources/application.properties
sed -i "s/mc01/mc01.aws-webapp.hz/g" /tmp/vprofile-project/src/main/resources/application.properties
cd /tmp/vprofile-project
mvn install
sudo systectl daemon-reload
sudo rm -rf /opt/tomcat/webapps/ROOT
sudo cp /tmp/vprofile-project/target/vprofile-v2.war /opt/tomcat/webapps/ROOT.war
sudo systemctl start tomcat
sudo systemctl enable tomcat