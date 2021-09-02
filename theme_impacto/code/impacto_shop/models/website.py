from odoo import api, fields, models


class MegamenuContent(models.Model):
    _inherit = "megamenu.content"
    
    megamenu_content_type = fields.Selection(selection_add=[('products', 'Products listing'),('product_grid','Product Grid'),
                                           ('category', 'Category listing'),('category_grid','Category Grid')])  
    megamenu_product_ids = fields.Many2many('product.template', string='Products')
    megamenu_categ_ids = fields.Many2many('product.public.category', string='Product Category')

