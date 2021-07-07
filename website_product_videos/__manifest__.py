#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

{
    'name'          : "Website Product Videos With Multi Images",
    'version'       : '1.1',
    'summary'       : """Website product videos with multi-images""",
    'author'        : 'Webkul Software Pvt. Ltd.',
    'website'       : 'https://store.webkul.com/Odoo-Website-Product-Videos-With-Multi-Images.html',
    "license"       :  "Other proprietary",
    'category'      : 'website',
    "live_test_url" : "http://odoodemo.webkul.com/?module=website_product_videos&custom_url=/shop/product/e-com10-apple-wireless-keyboard-18",
    'description'   : """

This module works very well with latest version of Odoo 10.0
--------------------------------------------------------------
    """,
    'depends'       : [
        'website_sale',
        'website_webkul_addons'
    ],

    'data'          : [
                        'views/templates.xml',
                        'security/product_video.xml',
                        'security/ir.model.access.csv',
                        'views/res_config_view.xml',
                        'views/product_views.xml',
                        'views/webkul_addons_config_inherit_view.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    "images"        :  ['static/description/Banner.png'],
    "application"   :  True,
    "installable"   :  True,
    "auto_install"  :  False,
    "price"         :  45,
    "currency"      :  "EUR",
    'sequence'      :   1,
    'pre_init_hook' :   'pre_init_check',
    'post_init_hook' : '_auto_configuration',
}