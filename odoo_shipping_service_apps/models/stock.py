# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from collections import  Counter
from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api, _
from odoo.exceptions import Warning,ValidationError
import logging
_logger = logging.getLogger(__name__)
Delivery = [
    ('none','None'),
    ('fixed','Fixed'),
    ('base_on_rule','Base on Rule'),
    ('fedex','fedex'),
    ('ups','ups'),
    ('usps','USPS'),
    ('auspost','auspost'),

]
AmountOption=[
    ('fixed', 'Fixed Amount'),
    ('percentage', '%  of Product Price')
]

class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"
    height = fields.Integer(related='packaging_id.height')
    width = fields.Integer(related='packaging_id.width')
    length = fields.Integer(related='packaging_id.length')
    cover_amount = fields.Integer(string='Cover Amount',help='This is the declared value/cover amount for an individual package.')
    description = fields.Text(string='Description',help='The text describing the package.')
    order_id = fields.Many2one(comodel_name='sale.order')
    _sql_constraints = [
        ('positive_cover_amount', 'CHECK(cover_amount>=0)', 'Cover Amount must be positive (cover_amount>=0).'),
         ('positive_shipping_weight', 'CHECK(shipping_weight>=0)', 'Shipment weight must be positive (shipping_weight>=0).'),

    ]

    @api.multi
    def wk_write(self):
        if self.packaging_id.package_carrier_type not in ['none']:
            if self.shipping_weight<1:
                msz=_('Shipment weight must be positive (shipping_weight>0).')
                raise ValidationError(msz)
            elif self.packaging_id and (self.packaging_id.max_weight < self.shipping_weight):
                msz = _('Shipment weight should be less then {max_weight} kg  as {max_weight} kg is the max weight limit set  for {name}  .'.format(max_weight=self.packaging_id.max_weight,name=self.packaging_id.name))
                _logger.info("Weight Check: %s  ",msz)
                raise ValidationError(msz)

class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    @api.multi
    def manage_package_type(self):
        self.ensure_one()
        res = super(StockPackOperation,self).manage_package_type()
        if res:
            delivery_type = self.picking_id.carrier_id.delivery_type not in ['base_on_rule', 'fixed']  and self.picking_id.carrier_id.delivery_type or 'none'
            context = res.get('context') and res.get('context').copy() or dict()
            ctx={'no_description':
                        not(delivery_type in ['fedex','dhl','ups','auspost'] and delivery_type or False ),
                    'no_cover_amount' :
                        not(delivery_type in ['fedex','dhl','ups','usps','auspost'] and delivery_type or False ),}
            context.update(ctx)
            res['context']=context
            self.picking_id.wk_update_package(self.result_package_id)
        return res
