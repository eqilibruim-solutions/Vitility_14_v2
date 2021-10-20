# coding=utf-8

{
    'name': 'Website Hide Menubar on URL',
    'version': '10.0.1.0.1',
    'category': 'Website',
    'license': '',
    'summary': 'This modules allows to hide menubar on specific URL.',
    'description': '''
        This modules allows to hide menubar on specific URL.\n
        Below are the steps to follow.\n
        
            >> Go to Website Admin\n
            >> Select Configuration\n
            >> Select URLs to hide menus\n
            >> Create new record and Enter URL or part of url on which you want to hide menubar.\n
        
            e.g. For hide the menubar on all the pages which have /shop in URL.
                 Enter /shop in URL string field.
    ''',
    'author': 'TechUltra Solutions',
    'website': 'www.techultrasolutions.com',
    'depends': ['theme_impacto'],
    'data': [
        'views/templates.xml',
        'views/views.xml'
        ],
    'installable': True,
    'application': True,
}
