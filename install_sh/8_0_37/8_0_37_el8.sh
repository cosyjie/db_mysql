yum remove -y mysql
dnf remove -y mysql-libs

yum module -y disable mysql

rm -rf /opt/cosyjieserver/tmp/db_mysql/download
mkdir -p /opt/cosyjieserver/tmp/db_mysql/download

wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-server-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-plugins-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-icu-data-files-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-common-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-libs-8.0.37-1.el8.x86_64.rpm -P /opt/cosyjieserver/tmp/db_mysql/download/

cd /opt/cosyjieserver/tmp/db_mysql/download && yum install -y mysql-community-{common,client-plugins,libs,client,icu-data-files,server}-*

#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-common-8.0.37-1.el8.x86_64.rpm
#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-client-plugins-8.0.37-1.el8.x86_64.rpm
#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-libs-8.0.37-1.el8.x86_64.rpm
#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-client-8.0.37-1.el8.x86_64.rpm
#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-icu-data-files-8.0.37-1.el8.x86_64.rpm
#rpm -ivh /opt/cosyjieserver/tmp/db_mysql/download/mysql-community-server-8.0.37-1.el8.x86_64.rpm

systemctl start mysqld

rm -rf /opt/cosyjieserver/tmp/db_mysql/download/