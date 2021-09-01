from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class sale_order(models.Model):
    _inherit = 'sale.order'

    def is_extra_charge_product(self):
        extra_change = False
        for line in self.order_line:
            if line.product_id and line.product_id.extra_charge_ok:
                extra_change = True
        return extra_change

    def _create_delivery_line(self, carrier, price_unit):
        SaleOrderLine = self.env['sale.order.line']
        res = super(sale_order, self)._create_delivery_line(carrier, price_unit)
        is_extra_charge = self.is_extra_charge_product()
        if carrier and is_extra_charge:
            country_id = self.partner_id.country_id
            if country_id:
                extra_charge_id = self.env['charge.lines'].search([('country_id', '=', country_id.id)])
                if extra_charge_id:
                    taxes = extra_charge_id.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
                    taxes_ids = taxes.ids
                    if self.partner_id and self.fiscal_position_id:
                        taxes_ids = self.fiscal_position_id.map_tax(taxes, extra_charge_id.product_id, self.partner_id).ids

                    carrier_with_partner_lang = carrier.with_context(lang=self.partner_id.lang)
                    if carrier_with_partner_lang.product_id.description_sale:
                        so_description = '%s: %s' % (carrier_with_partner_lang.name,
                                                     extra_charge_id.product_id.description_sale)
                    else:
                        so_description = 'Extra Charges'

                    values = {
                        'order_id': self.id,
                        'name': so_description,
                        'product_uom_qty': 1,
                        'product_uom': extra_charge_id.product_id.uom_id.id,
                        'product_id': extra_charge_id.product_id.id,
                        'price_unit': extra_charge_id.price,
                        'tax_id': [(6, 0, taxes_ids)],
                        'is_delivery': True,
                    }
                    if self.order_line:
                        values['sequence'] = self.order_line[-1].sequence + 1
                    sol = SaleOrderLine.sudo().create(values)
        return res

class delivery_carrier(models.Model):
    _inherit = 'delivery.carrier'
    
    charge_line_ids = fields.One2many('charge.lines','carrier_id', string='Charge Lines')

class charge_lines(models.Model):
    _name = "charge.lines"
    _description = "Extra Charges"
    
    country_id = fields.Many2one('res.country', string='Country', required='1')
    product_id= fields.Many2one('product.product', domain="[('type','=','service')]", string='Product', required="1")
    price = fields.Float('Price', required="1")
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')