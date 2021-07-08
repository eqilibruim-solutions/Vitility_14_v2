# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    wh_qty_available = fields.Char(
        compute='_compute_wh_qty_available',
        string='Quantity on hand warehouse')

    @api.depends(
        'product_id', 'order_id.warehouse_id', 'product_id.immediately_usable_qty')
    def _compute_wh_qty_available(self):
        for rec in self.product_id:
            if rec.exists() and rec.x_omdoos_aantal_producten:
                product = self.env['product.product'].with_context(
                    warehouse=self.order_id.warehouse_id.id).browse(
                    rec.id)
                for record in product:
                    self.wh_qty_available = str(int(record.immediately_usable_qty)) + "(" + \
                                    str(record.x_omdoos_aantal_producten) + ")"
            elif rec.exists():
                product = self.env['product.product'].with_context(
                    warehouse=self.order_id.warehouse_id.id).browse(
                    rec.id)
                for record in product:
                    self.wh_qty_available = str(int(record.immediately_usable_qty))
