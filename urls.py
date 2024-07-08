from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'db_mysql'

urlpatterns = [
    path('init/', login_required(views.mysql_init), name='init'),
    path('index/', login_required(views.DbIndexView.as_view()), name='index'),
    path('install/', login_required(views.DbInstallView.as_view()), name='install'),
    path('action/<str:action>/', login_required(views.DbActionView.as_view()), name='action'),
    path('uninstall/', login_required(views.DbUninstallView.as_view()), name='uninstall'),
    path('schema/create/', login_required(views.SchemaCreateView.as_view()), name='schema_create'),
    path('schema/delete/<str:schema>/', login_required(views.SchemaDeleteView.as_view()), name='schema_del'),
    path('table/list/<str:schema>/', login_required(views.TablesListView.as_view()), name='table_list'),
    path('options/users/root/<str:status>/', login_required(views.RootRemoteActionView.as_view()), name='root_remote'),
    path('users/root/password/form/', login_required(views.RootPasswordView.as_view()), name='root_pass'),
    path('users/root/password/generate/', login_required(views.GeneratePasswordView.as_view()), name='root_pass_generate'),
    # path('sync/', login_required(views.DbSyncView.as_view()), name='sync'),



]