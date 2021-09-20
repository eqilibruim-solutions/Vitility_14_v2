from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    transus_supplier_sale_order_receiver = fields.Boolean(string='Sale Order receiver')
