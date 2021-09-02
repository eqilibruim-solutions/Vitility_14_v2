# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class BlogCollection(models.Model):
    _name = 'blogcollection'
    _description = 'BlogCollection for blog snippets'    

    name= fields.Char("Blog Collection Title",traslate=True)
    blog_ids=fields.Many2many("blog.post",string="Blog Post",domain=[('website_published','=',True)])
    active=fields.Boolean("Active")
