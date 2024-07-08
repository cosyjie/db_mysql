import subprocess
import os
import shutil
from pathlib import Path
import json

from django.shortcuts  import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, DeleteView
from django.conf import settings
from django.contrib import messages

from appcommon.cryptography_message import encrypt_password, decrypt_password, generate_password
from appcommon.helper import subprocess_run, make_dir
from appcommon.mixin import JSONResponseMixin
from panel.module_database.views import ModuleDatabaseMixin

from .forms import DbInstallForm, MysqlUninstallForm, CreateDatabaseForm, SchemaDeleteForm, RootPasswordForm

conf_path = Path.joinpath(make_dir(Path.joinpath(settings.MEDIA_ROOT, 'db_mysql')), 'dbconf.json')


def mysql_init(request):
    from .install import setup
    setup()
    return redirect('module_database:db_mysql:index')


def get_conf():
    conf = {}
    with open(conf_path, 'r', encoding='utf8') as f:
        conf = json.load(f)
    return conf


class DbMysqlMixin(ModuleDatabaseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'db_mysql'

        context['is_init'] = False
        init_file = settings.APP_FILES / 'db_mysql' / 'init'
        if init_file.exists():
            context['is_init'] = True
            db_conf = get_conf()

            context['is_installed'] = False
            context['is_running'] = '-'
            context['db_version'] = ''
            context['login_status'] = False
            context['login_info'] = ''
            if Path.exists(Path(db_conf['mysqladmin'])):
                context['is_installed'] = True
                context['db_version'] = subprocess_run(
                    subprocess, f'{db_conf["mysqladmin"]} -V'
                ).stdout.strip().replace(f'{db_conf["mysqladmin"]}  Ver ', '')
                run_end = subprocess_run(subprocess, 'systemctl status mysqld')
                if "active (running)" in run_end.stdout:
                    context['is_running'] = "running"
                elif "inactive (dead)" in run_end.stdout or "failed" in run_end.stdout:
                    context['is_running'] = "stopped"

                if context['is_running'] == "running":
                    get_pass = decrypt_password(db_conf['password'])
                    check_login = subprocess_run(subprocess, f'{db_conf["mysqladmin"]} -uroot -p"{get_pass}" status')
                    if check_login.returncode == 0:
                        context['login_status'] = True
                    else:
                        error_message = check_login.stderr.strip().replace("\x07", "").split('\n')
                        for message in error_message:
                            if not message.startswith('mysqladmin: [Warning] Using a password on the command line'):
                                context['login_info'] += message + '</br>'
        return context


class DbIndexView(DbMysqlMixin, ListView):
    template_name = 'db_mysql/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'MySQL数据库管理'

        try:
            from .mysqlconn import DbAction

            db_conf = get_conf()
            dbaction = DbAction(
                host=db_conf['host'], port=db_conf['port'], user=db_conf['user'],
                password=decrypt_password(db_conf['password']),
                database='mysql'
            )
            dbaction.connect()
            result = dbaction.select_query("SELECT User, Host FROM user WHERE User = 'root'")[0]
            context['root_remote'] = False
            if '%' in result[1]:
                context['root_remote'] = True
            dbaction.close()
        except:
            pass
        return context

    def get_queryset(self):
        object_list = []
        try:
            db_conf = get_conf()
            from .mysqlconn import DbAction
            dbaction = DbAction(
                host=db_conf['host'], port=db_conf['port'], user=db_conf['user'],
                database='information_schema',
                password=decrypt_password(db_conf['password'])
            )
            result = dbaction.select_query("SELECT * FROM SCHEMATA")
            sys_db = ['information_schema', 'mysql', 'performance_schema', 'sys']
            for row in result:
                if row[1] not in sys_db:
                    object_list.append({
                        'schema_name': row[1],
                        'default_character_set_name': row[2],
                        'default_collation_name': row[3],
                    })
            dbaction.close()
        except:
            pass
        return object_list


class DbInstallView(DbMysqlMixin, FormView):
    form_class = DbInstallForm
    template_name = 'db_mysql/mysql_install.html'
    success_url = reverse_lazy('module_database:db_mysql:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '安装MySQL数据库'
        return context

    def form_valid(self, form):
        db_conf = get_conf()
        if Path(db_conf['log_file']).exists():
            os.remove(db_conf['log_file'])
        os_versioin = subprocess_run(subprocess, 'cat /etc/redhat-release')
        if 'release 8' in os_versioin.stdout:
            install_file = f'{settings.BASE_DIR}/apps/db_mysql/install_sh/8_0_37/8_0_37_el8.sh'
            subprocess_run(subprocess, f'sh {install_file}')
        if 'release 9' in os_versioin.stdout:
            install_file = f'{settings.BASE_DIR}/apps/db_mysql/install_sh/8_0_37/8_0_37_el9.sh'
            subprocess_run(subprocess, f'sh {install_file}')

        pass_log = subprocess_run(subprocess, "grep 'temporary password' /var/log/mysqld.log")
        password = pass_log.stdout.split('A temporary password is generated for root@localhost: ')[1].strip()
        new_password = generate_password()
        subprocess_run(subprocess, f'{db_conf["mysqladmin"]} -uroot -p"{password}" password "{new_password}"')
        db_conf['password'] = encrypt_password(new_password)
        with open(conf_path, 'w', encoding='utf-8') as f:
            json.dump(db_conf, f, ensure_ascii=False)

        return super().form_valid(form)


class DbActionView(DbMysqlMixin, RedirectView):
    url = reverse_lazy('module_database:db_mysql:index')

    def get(self, request, *args, **kwargs):
        db_conf = get_conf()
        action = kwargs.get('action').strip()
        if action == '1':
            subprocess_run(subprocess, db_conf['start_mysql'])
        if action == '2':
            subprocess_run(subprocess, db_conf['stop_mysql'])
        if action == '3':
            subprocess_run(subprocess, db_conf['restart_mysql'])

        return super().get(request, *args, **kwargs)


class DbUninstallView(DbMysqlMixin, FormView):
    form_class = MysqlUninstallForm
    template_name = 'db_mysql/mysql_uninstall.html'
    success_url = reverse_lazy('module_database:db_mysql:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'MySQL卸载'
        context['breadcrumb'] = [
            {'title': 'MySQL数据库管理', 'href': reverse('module_database:db_mysql:index'), 'active': False},
            {'title': 'MySQL卸载', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        db_conf = get_conf()
        confirm_txt = form.cleaned_data.get('confirm_txt')

        if confirm_txt == '确定卸载':
            subprocess_run(subprocess, 'systemctl stop mysqld')
            subprocess_run(subprocess, 'yum remove -y mysql')
            log_path = Path(db_conf['log_file'])
            if log_path.exists(): os.remove(log_path)

            data_path = Path(db_conf['data_dir'])
            if Path.exists(data_path): shutil.rmtree(data_path)

            from .dbconf import conf
            with open(conf_path, 'w', encoding='utf-8') as f:
                json.dump(conf, f, ensure_ascii=False)

        return super().form_valid(form)


class SchemaCreateView(DbMysqlMixin, FormView):
    form_class = CreateDatabaseForm
    template_name = 'db_mysql/create_database.html'
    success_url = reverse_lazy('module_database:db_mysql:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '创建数据库'
        context['breadcrumb'] = [
            {'title': 'MySQL管理', 'href': reverse('module_database:db_mysql:index'), 'active': False},
            {'title': '创建数据库', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        from .mysqlconn import DbAction
        schema_name = form.cleaned_data.get('schema_name').strip()
        schema_charset = form.cleaned_data.get('schema_charset').strip()
        db_conf = get_conf()
        dbaction = DbAction(
            host=db_conf['host'], port=db_conf['port'], user=db_conf['user'],
            password=decrypt_password(db_conf['password'])
        )
        dbaction.connect()
        dbaction.execute_query(f"CREATE DATABASE `{schema_name}` CHARACTER SET {schema_charset}")
        dbaction.close()
        return super().form_valid(form)


class SchemaDeleteView(DbMysqlMixin, FormView):
    form_class = SchemaDeleteForm
    template_name = 'db_mysql/confirm_schema_del.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '删除数据库'
        context['breadcrumb'] = [
            {'title': 'MySQL管理', 'href': reverse('module_database:db_mysql:index'), 'active': False},
            {'title': '删除数据库', 'href': '', 'active': True},
        ]
        context['schema'] = self.kwargs['schema']
        return context

    def form_valid(self, form):
        try:
            conf = get_conf()
            get_schema = self.kwargs['schema']
            schema_name = form.cleaned_data.get('schema_name')
            if schema_name == get_schema:
                run = subprocess_run(
                    subprocess,
                    f'{conf["mysqladmin"]} -u{conf["user"]} -p"{decrypt_password(conf["password"])}" drop "{schema_name}" -f'
                )
                print(run)
                self.success_url = reverse_lazy('module_database:db_mysql:index')
            else:
                messages.warning(self.request, '输入的数据库名校验失败！请重新输入！')
                self.success_url = reverse_lazy('module_database:db_mysql:schema_del', kwargs={'schema': get_schema})
        except:
            self.success_url = reverse_lazy('module_database:db_mysql:schema_del', kwargs={'schema': get_schema})
        return super().form_valid(form)


class TablesListView(DbMysqlMixin, ListView):
    template_name = 'db_mysql/tables_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '数据表'
        context['breadcrumb'] = [
            {'title': 'MySQL管理', 'href': reverse('module_database:db_mysql:index'), 'active': False},
            {'title': '数据表', 'href': '', 'active': True},
        ]
        context['schema'] = self.kwargs.get('schema')
        return context

    def get_queryset(self):
        from .mysqlconn import DbAction
        db_conf = get_conf()
        dbaction = DbAction(
            host=db_conf['host'], port=db_conf['port'], user=db_conf['user'],
            password=decrypt_password(db_conf['password']),
            database='information_schema'
        )
        dbaction.connect()
        result = dbaction.select_query(
            f"SELECT TABLE_NAME,ENGINE,TABLE_ROWS,CREATE_TIME,UPDATE_TIME,TABLE_COLLATION, TABLE_COMMENT "
            f"FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.kwargs.get('schema')}'"
        )
        dbaction.close()
        return result


class RootRemoteActionView(DbMysqlMixin, RedirectView):
    url = reverse_lazy('module_database:db_mysql:index')

    def get(self, request, *args, **kwargs):
        from .mysqlconn import DbAction
        status = kwargs.get('status')
        db_conf = get_conf()
        get_pass = decrypt_password(db_conf['password'])
        dbaction = DbAction(
            host=db_conf['host'], port=db_conf['port'], user=db_conf['user'],
            password=decrypt_password(db_conf['password']),
            database='mysql'
        )
        dbaction.connect()
        status_str = 'localhost'
        if status == '1':
            status_str = '%'
        print(f"UPDATE user SET host='{status_str}' WHERE user='root'")
        dbaction.execute_query(f"UPDATE user SET host='{status_str}' WHERE user='root'")
        dbaction.close()
        runnd = subprocess_run(subprocess, f'{db_conf["mysqladmin"]} -uroot -p"{get_pass}" flush-privileges')
        print(runnd)
        return super().get(request, *args, **kwargs)


class GeneratePasswordView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response({'newpassword': generate_password()}, **response_kwargs)


class RootPasswordView(DbMysqlMixin, FormView):
    form_class = RootPasswordForm
    template_name = 'db_mysql/root_password.html'
    success_url = reverse_lazy('module_database:db_mysql:root_pass')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Root用户密码'
        context['breadcrumb'] = [
            {'title': 'MySQL管理', 'href': reverse('module_database:db_mysql:index'), 'active': False},
            {'title': context['page_title'], 'href': '', 'active': True},
        ]
        return context

    def get_initial(self):
        conf = get_conf()
        self.initial['root_password'] = decrypt_password(conf['password'])
        return self.initial.copy()

    def form_valid(self, form):
        if form.changed_data:
            db_conf = get_conf()
            password = decrypt_password(db_conf["password"])
            new_password = form.cleaned_data.get('root_password')
            subprocess_run(subprocess, f'{db_conf["mysqladmin"]} -uroot -p"{password}" password "{new_password}"')

            db_conf['password'] = encrypt_password(new_password)
            with open(conf_path, 'w', encoding='utf-8') as f:
                json.dump(db_conf, f, ensure_ascii=False)

            messages.success(self.request, f'密码已经修改~ 新密码为 {new_password} ')
        else:
            messages.warning(self.request, '密码没有变化~')
        return super().form_valid(form)

