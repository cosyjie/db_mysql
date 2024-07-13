dnf remove -y mysql
dnf remove -y mysql-libs
yum module -y disable mysql

rm -rf /opt/jieserver/tmp/db_mysql/download
mkdir -p /opt/jieserver/tmp/db_mysql/download

wget https://dev.mysql.com/get/mysql84-community-release-el9-1.noarch.rpm -P /opt/jieserver/tmp/db_mysql/download/

cd /opt/jieserver/tmp/db_mysql/download && yum install -y mysql84-community-release-el9-1.noarch.rpm

dnf config-manager --enable mysql-8.4-lts-community
sudo dnf config-manager --disable mysql80-community

yum install -y mysql-community-server