# -*- coding: utf-8 -*-


from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    eori_number = fields.Char("EORI Number")
