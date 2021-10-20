# -*- coding: utf-8 -*-


from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    eori_number = fields.Char("EORI Number")
