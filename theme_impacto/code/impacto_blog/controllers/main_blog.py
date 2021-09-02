# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlog(WebsiteBlog):

    @http.route(['/blog/get_blog_content'], type='json', auth='public', website=True, csrf=False,cache=600)
    def get_blog_content_data(self, template=False, collection_id=False,limit=10):
        new_contxt = dict(request.env.context)
        res = request.env['blogcollection'].browse(int(collection_id))
     
        request.env.context = new_contxt
        values = {'blog_slider_collection':res }
        return request.env['ir.ui.view'].render_template(template, values)
