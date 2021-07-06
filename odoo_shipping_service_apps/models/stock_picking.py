# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from collections import  Counter
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


class product_package(models.Model):
    _name = "product.package"
    @api.one
    @api.depends('order_id', 'packaging_id')
    def _complete_name(self):
        name = self.picking_id.name
        if self.order_id:
            name = self.order_id.name + "[%s]" % (name)
        self.complete_name = name
    @api.model
    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search([('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)

    complete_name = fields.Char(compute=_complete_name, string="Package Name",)

    packaging_id = fields.Many2one(comodel_name='product.packaging',string='Packaging',required=True)
    order_id = fields.Many2one(comodel_name='sale.order')
    carrier_id = fields.Many2one(related='order_id.carrier_id')
    delivery_type = fields.Selection(selection=Delivery)
    full_capacity  =fields.Boolean()
    height = fields.Integer(default=1)
    width = fields.Integer(default=1)
    length = fields.Integer(default=1)
    weight = fields.Float(default=1,string='Weight(kg)')
    weight_uom_id = fields.Many2one('product.uom', string='Unit of Measure', readonly=True, help="Unit of Measure (Unit of Measure) is the unit of measurement for Weight",
     default=lambda self:self._default_uom)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def get_picking_price(self,package_id):
        pack_operation_ids = self.env['stock.pack.operation'].search(
            [('result_package_id', '=', package_id.id)])
        return  sum([x.qty_done * x.product_id.list_price for x in pack_operation_ids])


    @api.model
    def wk_update_package(self,package_id=None):
        if self.carrier_id.delivery_type not in ['base_on_rule', 'fixed']:
            packaging_id = package_id.packaging_id
            if package_id and (not packaging_id):
                packaging_id = self.carrier_id.packaging_id
                package_id.packaging_id = packaging_id.id
            amount =self.get_picking_price(package_id)
            package_id.cover_amount = packaging_id.get_cover_amount(amount)
        return True


    @api.multi
    def put_in_pack(self):
        self.ensure_one()
        res = super(StockPicking,self).put_in_pack()
        if res:
            carrier_id = self.carrier_id
            if res.get('res_id'):
                package_id = self.env["stock.quant.package"].browse(res.get('res_id'))

            delivery_type = self.carrier_id.delivery_type not in ['base_on_rule', 'fixed']  and self.carrier_id.delivery_type or 'none'
            context = res.get('context') and res.get('context').copy() or dict()
            ctx={'no_description':
                        not(delivery_type in ['fedex','dhl','ups','auspost'] and delivery_type or False ),
                    'no_cover_amount' :
                        not(delivery_type in ['fedex','dhl','ups','usps','auspost'] and delivery_type or False ),}
            context.update(ctx)
            res['context']=context
            self.wk_update_package(package_id)
        return res
    @api.one
    @api.depends('package_ids')
    def _compute_cover_amount(self):
        self.cover_amount = sum(self.package_ids.mapped('cover_amount'))

    label_genrated = fields.Boolean(string='Label Generated', copy=False)
    shipment_uom_id = fields.Many2one(related='carrier_id.uom_id', readonly="1",
                                      help="Unit of measurement for use by Delivery method", copy=False)

    date_delivery = fields.Date(string='Expected Date Of Delivery',
                                help='Expected Date Of Delivery :The delivery time stamp provided by Shipment Service', copy=False, readonly=1)
    weight_shipment = fields.Float(
        string='Send Weight', copy=False, readonly=1)
    cover_amount = fields.Float(
        string='Cover Amount',
        compute='_compute_cover_amount',
        copy=False, readonly=1)


    @api.multi
    def action_cancel(self):
        if self.label_genrated == True:
            raise ValidationError(
                'Please cancel the shipment before canceling  picking! ')
        return super(StockPicking, self).action_cancel()

    @api.cr_uid_ids_context
    def do_enter_transfer_details(self, cr, uid, picking, context=None):
        picking_obj = self.browse(cr, uid, picking)
        if picking_obj.carrier_id and picking_obj.carrier_id.delivery_type not in ['fixed', 'base_on_rule'] and picking_obj.carrier_id.genrate_label and not picking_obj.label_genrated:
            msg = 'You must have generate the shipment label  before transferring the delivery. '
            self.message_post(cr, uid, picking, body=msg,
                              subject="Must Generate the Label")
            return self.pool['delivery.carrier']._shipping_genrated_message(cr, uid, picking, msg, context=None)
        else:
            res = super(StockPicking, self).do_enter_transfer_details(
                cr, uid, picking, context=None)
            return res

    @api.multi
    def do_new_transfer(self):
        for pick in self:
            carrier_id = pick.carrier_id
            if carrier_id and (carrier_id.delivery_type not in ['base_on_rule', 'fixed']):
                if not len(pick.package_ids):
                    raise ValidationError('Create the package first for picking %s before sending to shipper.'%(pick.name))
        return super(StockPicking, self).do_new_transfer()

    @api.multi
    def send_to_shipper(self):
        self.ensure_one()
        if self.carrier_id.delivery_type and (self.carrier_id.delivery_type not in ['base_on_rule', 'fixed']):
            if not len(self.package_ids):
                raise ValidationError('Create the package first for picking %s before sending to shipper.'%(self.name))
            else:
                try:
                    res = self.carrier_id.send_shipping(self)[0]
                    self.carrier_price = res.get('exact_price')
                    self.carrier_tracking_ref = res.get(
                        'tracking_number') and res.get('tracking_number').strip(',')
                    self.label_genrated = True
                    self.date_delivery = res.get('date_delivery')
                    self.weight_shipment = float(res.get('weight'))
                    msg = _("Shipment sent to carrier %s for expedition with tracking number %s") % (
                        self.carrier_id.delivery_type, self.carrier_tracking_ref)
                    self.message_post(
                        body=msg,
                        subject="Attachments of tracking",
                        attachments=res.get('attachments')
                    )
                except Exception as e:
                    return self.carrier_id._shipping_genrated_message(e)

    @api.model
    def unset_fields_prev(self):
        self.carrier_tracking_ref = False
        self.carrier_price = False
        self.label_genrated = False
        self.date_delivery = False
        self.weight_shipment = False
        self.number_of_packages = False
        return True

    @api.multi
    def cancel_shipment(self):
        self.ensure_one()
        try:
            if self.carrier_id.void_shipment:
                self.carrier_id.cancel_shipment(self)
                msg = "Shipment of  %s  has been canceled" % self.carrier_tracking_ref
                self.message_post(body=msg)
                self.unset_fields_prev()

            else:
                msg = 'You are not allowed to Void  the Shipment , please contact your Admin to enable the  Void Shipment. '
                self.message_post(
                    body=msg, subject="Not allowed to Void the Shipment.")
                return self.carrier_id._shipping_genrated_message(msg)
        except Exception as e:
            return self.carrier_id._shipping_genrated_message(e)
