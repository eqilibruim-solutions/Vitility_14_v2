# -*- coding: utf-8 -*-

from odoo import api, fields, models
import os

class Website(models.Model):
    _inherit = 'website'
    
    @api.model
    def get_category_ids(self,category):
        parent_category = []
        if category:
            category = self.env['product.public.category'].search([('id', '=', int(category))])
            parent_category = [category]
            current_category = category
            while current_category.parent_id:
                parent_category.append(current_category.parent_id)
                current_category = current_category.parent_id
            parent_category.reverse()
        return parent_category