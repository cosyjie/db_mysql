from django import forms
from appcommon.forms import FormBase


class DbSyncForm(FormBase):
    pw1 = forms.CharField(label='密码*', required=True, widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'lay-verify': 'required',
            'lay-reqtext': '密码不能为空！',
        }))
    pw2 = forms.CharField(label='密码确认*', required=True, widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'lay-verify': 'required|confirmPassword',
            'lay-reqtext': '密码确定不能为空！',
        }))
    resetpass = forms.BooleanField(widget=forms.CheckboxInput(attrs={}))


class RootPasswordForm(FormBase):
    root_password = forms.CharField(required=True, widget=forms.TextInput(
         attrs={
            'class': 'form-control', 'lay-verify': 'required', 'lay-reqtext': '密码不能为空！',
        }))



# class DbConForm(FormBase):
#     mysql_path = forms.CharField(label='* mysql命令路径', widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': 'mysql命令地址不能为空'
#             }
#         ))
#     port = forms.CharField(label='* 端口', widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '端口不能为空'
#             }
#         ))
#     conf_dir = forms.CharField(label='* 配置文件路径', max_length=250, widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '数据目录地址不能为空'
#             }
#         ))
#
#     data_dir = forms.CharField(label='* 数据目录路径', max_length=250, widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '数据目录地址不能为空'
#             }
#         ))
#     start_command = forms.CharField(label='* 运行命令', max_length=250, widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': 'mysql运行命令不能为空'
#             }
#         ))
#     stop_command = forms.CharField(label='* 停止命令', max_length=250, widget=forms.TextInput(
#             attrs={
#                 'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': 'mysql停止命令不能为空'
#             }
#         ))
#     restart_command = forms.CharField(label='* 重启命令', max_length=250, widget=forms.TextInput(
#         attrs={
#             'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': 'mysql重启命令不能为空'
#         }
#     ))


class DbInstallForm(FormBase):
    pass


class MysqlUninstallForm(FormBase):
    # confirm = forms.BooleanField(label='保留数据目录（/var/lib/mysql）', required=False, widget=forms.CheckboxInput())
    confirm_txt = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={
            'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '请输入确认卸载文字~'
        }
    ))


class CreateDatabaseForm(FormBase):
    schema_name = forms.CharField(label='* 数据库名称', max_length=250, widget=forms.TextInput(
        attrs={
            'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '数据库名称不能为空'
        }
    ))
    schema_charset = forms.CharField(label='* 字符集', max_length=10, widget=forms.Select(
        choices=(('utf8mb4', 'utf8mb4'), ('utf8', 'utf8'), ('gbk', 'gbk'), ('big5', 'big5')),
        # attrs={}
    ))


class SchemaDeleteForm(FormBase):
    schema_name = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={
            'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'lay-reqtext': '请输入要删除的数据库名称！'
        }
    ))
    