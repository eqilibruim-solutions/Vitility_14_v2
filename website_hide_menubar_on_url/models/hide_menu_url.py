# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HideMenuUrl(models.Model):

    _name = 'hide.menu.url'
    _description = 'Hide Menu URL'

    name = fields.Char("URL string", help="URL or Part of URL to make menus hidden on that page.")
    active = fields.Boolean("Active", default=True)
