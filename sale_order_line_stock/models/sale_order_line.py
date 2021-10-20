# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    wh_qty_available = fields.Char(
        compute='_compute_wh_qty_available',
        string='Quantity on hand warehouse')

    @api.depends(
        'product_id', 'order_id.warehouse_id', 'product_id.immediately_usable_qty')
    def _compute_wh_qty_available(self):
        for rec in self:
            if rec.product_id.exists() and rec.product_id.x_omdoos_aantal_producten:
                product = self.env['product.product'].with_context(
                    warehouse=rec.order_id.warehouse_id.id).browse(
                    rec.product_id.id)
                rec.wh_qty_available = str(int(product.immediately_usable_qty)) + "(" + \
                                    str(product.x_omdoos_aantal_producten) + ")"
            elif rec.product_id.exists():
                product = self.env['product.product'].with_context(
                    warehouse=rec.order_id.warehouse_id.id).browse(
                    rec.product_id.id)
                rec.wh_qty_available = str(int(product.immediately_usable_qty))
            else:
                rec.wh_qty_available = "0"

