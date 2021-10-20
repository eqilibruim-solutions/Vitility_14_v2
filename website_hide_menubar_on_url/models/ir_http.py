# -*- coding: utf-8 -*-

import werkzeug
from odoo.http import request
from odoo import models
from odoo.tools.translate import _


class ir_http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        try:
            if request.httprequest.method == 'GET' and '//' in request.httprequest.path:
                new_url = request.httprequest.path.replace('//', '/') + '?' + request.httprequest.query_string
                return werkzeug.utils.redirect(new_url, 301)
            func, arguments = cls._find_handler()
            request.website_enabled = func.routing.get('website', False)
        except werkzeug.exceptions.NotFound:
            # either we have a language prefixed route, either a real 404
            # in all cases, website processes them
            request.website_enabled = True

        if request.website_enabled:
            urls = request.env['hide.menu.url'].sudo().search_read([], ['name'])
            request.urls_to_hide_menubar = [str(data.get('name')) for data in urls]

        return super(ir_http, cls)._dispatch()