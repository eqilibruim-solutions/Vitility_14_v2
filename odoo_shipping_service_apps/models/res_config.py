# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import fields ,models
ComputeWeight = [
    ('volume','Using Volumetric Weight'),
    ('weight','Using Weight')
]
class base_config_settings(models.TransientModel):
	_inherit='base.config.settings'
	module_fedex_delivery_carrier=fields.Boolean(
		string = "FedEx Shipping Service"
	)
	module_usps_delivery_carrier=fields.Boolean(
		string = "USPS Shipping Service"
	)
	module_ups_delivery_carrier=fields.Boolean(
		string = "UPS Shipping Service"
	)
	module_dhl_delivery_carrier=fields.Boolean(
		string = "DHL Shipping Service"
	)
	module_auspost_delivery_carrier = fields.Boolean(
		string = "Australia Post"
	)
	module_dhl_intraship_delivery_carrier=fields.Boolean(
		string = "DHL Intraship Shipping Service"
	)
	module_aramex_delivery_carrier = fields.Boolean(
		string = "Aramex Shipping Service"
	)
	compute_weight = fields.Selection(
		selection = ComputeWeight,
		default='weight',
		string= 'Compute Weight'
	)
	default_product_weight = fields.Float(
		default=1,
		string='Default Product  Weight',
		help="Default  weight  will use in  package if product not have weight"
	)
