# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Open Qty",
    "summary": "Allows to identify the purchase orders that have quantities "
               "pending to invoice or to receive.",
    "version": "14.0.1.0.0",
    "author": "GRIPICT",
    "category": "Purchases",
    "depends": ["purchase", "purchase_stock"],
    "data": [
        'views/purchase_view.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
