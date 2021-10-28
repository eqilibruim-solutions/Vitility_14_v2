# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# © 2017 Today Mourad EL HADJ MIMOUNE @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase and Invoice Allowed Product",
    "summary": "This module allows to select only products that can be supplied by the supplier",
    "version": "14.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "views/res_partner_view.xml",
        "views/account_move_views.xml",
        "views/purchase_order_view.xml",
    ],
    "installable": True,
}
