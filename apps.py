from django.apps import AppConfig


class DbMysqlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.db_mysql'
    dependent_modules = ['module_database']
    verbose_name = 'MySQL管理'
    version = '0.0.1-Alpha'
    description = 'MySQL管理'
