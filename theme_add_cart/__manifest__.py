# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Theme Cart',
    'summary': 'Theme Add To Cart',
    'category': 'Theme/Ecommerce',
    'author': 'TechUltra Solutions',
	'website' : 'https://techultrasolutions.com',
    'description': """
        Theme in shop page design change as Product image(clickable, should take user to product details page),Product description,Product price,Add to Cart(bar)
        and Product Number(Internal referance) in product.
        """,

    'version': '1.0',
    'depends': [
        'theme_impacto',
        ],
    'data': [   
        'views/theme_template_view.xml',
        'views/assets.xml',
    ],


	'installable': True,
    'application': True,
	
}
