import subprocess
import shutil
import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from appcommon.helper import subprocess_run, make_dir

from .dbconf import conf


def setup():
    subprocess_run(subprocess, f'{settings.PYENV_DEFAULT_PIP_RUN} install PyMySQL')
    conf_path = Path.joinpath(make_dir(Path.joinpath(settings.MEDIA_ROOT, 'db_mysql')), 'dbconf.json')
    with open(conf_path, 'w', encoding='utf-8') as f:
        json.dump(conf, f, ensure_ascii=False)

    return True


def uninstall():
    shutil.rmtree(f'{settings.MEDIA_ROOT}/db_mysql', ignore_errors=True)