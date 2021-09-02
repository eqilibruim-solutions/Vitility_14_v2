# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Theme Impacto',
    'summary': 'Html5 Responsive E-Commerce And Multi-Purpose theme',
    'category': 'Theme/Ecommerce',
    'author': 'Adventumweb',
    'sequence': 1,
    'version': '1.1',
    'depends': [
        'website',
        'website_crm',
        'theme_common',
        'auth_signup',
        'website_sale'],
    'data': [   
        'views/customize_modal.xml',
         'views/assets.xml',
		  'views/shop.xml',
         'views/page_login.xml',
		'views/snippets.xml',
        'views/snippets_option.xml',
		'views/header.xml',
        'views/footer.xml',
        'views/page_login_business.xml'
    ],
    'images': [
      'static/description/impacto.jpg',
    ],
    'price': '99',
    'currency':'EUR',
    'live_test_url':'http://198.251.72.29/',
	'installable': True,
    'application': True,
	
}
