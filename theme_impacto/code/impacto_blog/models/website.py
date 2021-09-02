from odoo import api, fields, models


class MegamenuContent(models.Model):
    _inherit = "megamenu.content"
    
    megamenu_content_type = fields.Selection(selection_add=[('blog', 'Blog')])    
    megamenu_blog_ids = fields.Many2many("blog.post",string="Blog Post",domain=[('website_published','=',True)])
