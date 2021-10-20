# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    """ Purchase Order Line modifier for product price. """
    _inherit = "purchase.order.line"

    product_moq = fields.Char(string="Product MOQ", compute="_compute_product_moq")
    is_click = fields.Boolean(string="Clicked?")

    @api.depends('order_id.partner_id', 'product_id', 'product_id.seller_ids')
    def _compute_product_moq(self):
        for rec in self:
            sort_supplier_info = rec.product_id.seller_ids.filtered(lambda s: s.name.id == rec.order_id.partner_id.id).sorted(key=lambda r: r.min_qty)
            if sort_supplier_info:
                rec.product_moq = str(sort_supplier_info[:1].min_qty or 0.0)
            else:
                rec.product_moq = "No Supplier set."

    def get_supplier_minimum_product_price(self):
        for rec in self:
            rec.is_click = True
            sort_supplier_info = rec.product_id.seller_ids.filtered(lambda s: s.name.id == rec.order_id.partner_id.id).sorted(key=lambda r: r.min_qty)
            if sort_supplier_info:
                if sort_supplier_info[:1].price == 0.0:
                    raise ValidationError(
                        _('Error ! Minimum Price is zero. Please update in Product Or Set Price manually'))
                rec.write({
                    "price_unit": sort_supplier_info[:1].price,
                    "supplier_info": sort_supplier_info[:1].vandor_product_information
                })
                rec.order_id._amount_all()
            else:
                raise ValidationError(_('Error ! No Supplier is available for this product'))

