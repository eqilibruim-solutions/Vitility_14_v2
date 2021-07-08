from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    bam_product_keyword1 = fields.Char('keyword1')
    bam_product_keyword2 = fields.Char('keyword2')
    bam_product_keyword3 = fields.Char('keyword3')
    bam_product_keyword4 = fields.Char('keyword4')
    bam_product_keyword5 = fields.Char('keyword5')