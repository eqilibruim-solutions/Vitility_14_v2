# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
##################################################################################

{
    'name': 'Website Product Filter Display In Mobile',
    'version': '10.0.0.1',
    'sequence': 1,
    'summary': 'Display filter options for website sale on mobile/tablet view.',
    'category': 'eCommerce',
    'author': 'SnepTech',
    'license': 'AGPL-3',
    'website': 'https://www.sneptech.com',
    "price": 50,
    "currency": 'EUR',
    'description': """
        Do you want to display website product filter in Mobile/Tablet view ? 
        By default Product Filter on website is not being display in mobile view,
        This module is used to enable the filter options in Mobile/Tablet view.
    """ ,

    'depends': ['website','website_sale'],
    'data': [
        'views/template.xml'
    ],
    'live_test_url':"https://youtu.be/JpBALb5DvT8",
    'application': True,
    'installable': True,
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
