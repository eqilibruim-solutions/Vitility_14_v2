from odoo import models, fields


class product_template(models.Model):
    _inherit = 'product.template'

    extra_charge_ok  = fields.Boolean(string="Extra Charges", copy=False)