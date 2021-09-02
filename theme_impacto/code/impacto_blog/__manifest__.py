{
    'name': 'Impacto blog',
    'description': '''Impacto Website blog
''',
    'summary': 'Impacto blog addons',
    'category': 'Website',
    'version': '12.0.1.0.0',
    'author': 'adventumweb',
    'website': '',
    'depends': ['website_blog'],
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/website_blog_collection.xml',
        'views/snipet_blog_carousel.xml',
        'views/website_view.xml'
    ],
    'application': False,
}
