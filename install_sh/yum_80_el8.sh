dnf remove -y mysql
dnf remove -y mysql-libs
yum module -y disable mysql

rm -rf /opt/jieserver/tmp/db_mysql/download
mkdir -p /opt/jieserver/tmp/db_mysql/download

wget https://dev.mysql.com/get/mysql84-community-release-el8-1.noarch.rpm -P /opt/jieserver/tmp/db_mysql/download/

cd /opt/jieserver/tmp/db_mysql/download && yum install -y mysql84-community-release-el8-1.noarch.rpm

dnf config-manager --disable mysql-8.4-lts-community
dnf config-manager --disable mysql-tools-8.4-lts-community
dnf config-manager --enable mysql80-community
dnf config-manager --enable mysql-tools-community

yum install -y mysql-community-server

rm -rf /opt/jieserver/tmp/db_mysql/download/