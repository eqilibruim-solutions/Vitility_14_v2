from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.public.category'

    menu_ids = fields.Many2many('website.menu', string="Main menu", help="Added this category one or more Menu")
    mm_description = fields.Text(string="Description", translate=True,
        help="Short description which can be used in mega menu.")
    category_image = fields.Binary(string="Category Image" ,readonly=False)
