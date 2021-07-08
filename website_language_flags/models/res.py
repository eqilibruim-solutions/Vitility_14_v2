# -*- coding: utf-8 -*-

from odoo import fields, models

class ResLang(models.Model):
    _inherit = 'res.lang'

    lang_flag = fields.Binary(string='Language Flag')
