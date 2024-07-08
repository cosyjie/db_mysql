from django.urls import reverse

menu = {
    'module_database': {
        'child': [
            {
                'name': 'db_mysql',
                'title': 'MySQL数据库',
                'href': reverse('module_database:db_mysql:index'),
            },
        ]
    }
}