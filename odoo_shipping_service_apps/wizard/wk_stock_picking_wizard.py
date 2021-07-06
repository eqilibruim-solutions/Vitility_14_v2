# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import models, fields, api
class wk_stock_picking_wizard(models.TransientModel):
	_name= 'wk.stock.picking.wizard'
	picking_count = fields.Integer(strnig='Total Effected Picking ', readonly=1)

	@api.model
	def default_get(self, fields):
		return {'picking_count':len(self._context['active_ids']) }


	@api.multi
	def generate_shipment_label(self):
		picking_ids=[]
		for picking  in self.env['stock.picking'].browse(self._context['active_ids']):
			if picking.carrier_id.delivery_type not in ['fixed','based_on_rule']:
				picking.send_to_shipper()
				picking_ids=picking.ids
		if picking_ids:
			return {
				'name': ('Requested Pickings'),
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'tree,form',
				'res_model': 'stock.picking',
				'view_id': False,
				'domain': [('id', 'in', picking_ids)],
				'target':'current',
			}

	@api.multi
	def void_shipment(self):
		picking_ids=[]
		for picking  in self.env['stock.picking'].browse(self._context['active_ids']):
			if picking.carrier_id.delivery_type not in ['fixed','based_on_rule']:
				picking.cancel_shipment()
				picking_ids=picking.ids
		if picking_ids:
			return {
				'name': ('Requested Pickings'),
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'tree,form',
				'res_model': 'stock.picking',
				'view_id': False,
				'domain': [('id', 'in', picking_ids)],
				'target':'current',
			}
