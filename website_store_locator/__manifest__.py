# -*- coding: utf-8 -*-
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
  "name"                 :  "Website Store Locator",
  "summary"              :  """The module allows you to enter the physical address of your store on website so the customers can see it on the Google Map.""",
  "category"             :  "Website",
  "version"              :  "1.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Store-Locator.html",
  "description"          :  """Odoo Website Store Locator
Store location detect
Detect Store location
Store address
Website store address
Store location on google map
Store coordinates
Store location on map""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_store_locator&custom_url=/store/locator",
  "depends"              :  [
                             'sale_shop',
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/sale_shop_inherit_view.xml',
                             'views/res_config_view.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'data/store_set_default_values.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}