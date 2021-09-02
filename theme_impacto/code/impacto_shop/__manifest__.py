{
    'name': 'Impacto Shop',
    'description': '''Impacto Website Shop
''',
    'summary': 'Impacto shop addons',
    'category': 'Website',
    'version': '12.0.1.0.0',
    'author': 'adventumweb',
    'website': '',
    'depends': ['website_sale','website_sale_comparison','website_sale_wishlist' ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_view.xml',
        'views/website_product_collection.xml',
        'views/product_carousel.xml',
        'views/product_category_view.xml',
        'views/product_exts.xml',
        'views/shop.xml',
        #'views/shop_details.xml'
    ],
    'application': False,
}
