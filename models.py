from django.db import models


# class MysqlConfig(models.Model):
#     host = models.CharField(max_length=50, default='127.0.0.1')
#     port = models.IntegerField(default=3306)
#     user = models.CharField(max_length=50, default='root')
#     password = models.CharField(max_length=100)
#     conf_path = models.CharField(max_length=200)
#     datadir = models.CharField(max_length=200)
#     start_command = models.CharField(max_length=200, default='systemctl start mysqld')
#     stop_command = models.CharField(max_length=200, default='systemctl stop mysqld')
#     restart_command = models.CharField(max_length=200, default='systemctl restart mysqld')
