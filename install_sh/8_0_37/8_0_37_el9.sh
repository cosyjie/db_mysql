yum remove -y mysql
yum module -y disable mysql

rm -rf /opt/cosyjieserver/tmp/db_mysql/download
mkdir -p /opt/cosyjieserver/tmp/db_mysql/download

wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-server-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-plugins-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-icu-data-files-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-common-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-libs-8.0.37-1.el9.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/

cd /opt/cosyjieserver/tmp/db_mysql/download && yum install -y mysql-community-{common,client-plugins,libs,client,icu-data-files,server}-*

systemctl start mysqld

rm -rf /opt/cosyjieserver/tmp/db_mysql/download/