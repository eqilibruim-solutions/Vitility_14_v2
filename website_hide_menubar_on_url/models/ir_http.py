# -*- coding: utf-8 -*-

import werkzeug
from odoo.http import request
from odoo import models, api, SUPERUSER_ID


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        request.routing_iteration = getattr(request, 'routing_iteration', 0) + 1
        # handle // in url
        if request.httprequest.method == 'GET' and '//' in request.httprequest.path:
            new_url = request.httprequest.path.replace('//', '/') + '?' + request.httprequest.query_string.decode(
                'utf-8')
            return werkzeug.utils.redirect(new_url, 301)

        try:
            default_lg_id = cls._get_default_lang()
            env = api.Environment(request.env.cr, SUPERUSER_ID, {})
            request.website_routing = env['website'].get_current_website().id
            request.lang = default_lg_id
            rule, arguments = cls._match(request.httprequest.path)
            func = rule.endpoint
            request.is_frontend = func.routing.get('website', False)
        except werkzeug.exceptions.NotFound:
            path_components = request.httprequest.path.split('/')
            request.is_frontend = len(path_components) < 3 or path_components[2] != 'static' or not '.' in \
                                                                                                    path_components[-1]

        if request.is_frontend:
            urls = request.env['hide.menu.url'].sudo().search_read([], ['name'])
            request.urls_to_hide_menubar = [str(data.get('name')) for data in urls]
        return super(IrHttp, cls)._dispatch()