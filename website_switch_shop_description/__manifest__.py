# -*- coding: utf-8 -*-
{
    # Module info
    'name': 'Website Switch Shop Description add fields',
    'version': '14.3.3',
    'category': 'website',
    'sequence': 1,
    'summary': 'Switch the description of the shop for product and add fields for product.',
    'description': """Switch the description of website and sale. Also add new fields for products, to be displayed on the website.""",

    # Author
    'author': 'Business Agility Masters',
    'website': 'https://www.businessagilitymasters.com',

    # Dependencies
    'depends': ['base','website_sale', 'theme_impacto', 'website_product_videos'],

    # Views
    'data': [
        'views/template.xml',
        'views/product.xml',
        'views/views.xml',
        'security/ir.model.access.csv',
    ],

    # Technical Specif.
    'installable': True,
    'application': False,
    'auto_install': False,
}
