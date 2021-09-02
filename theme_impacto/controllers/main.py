# -*- coding: utf-8 -*-
from odoo import fields,http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main
from odoo.addons.website.controllers.main import Website

import math
import os
import logging

_logger = logging.getLogger(__name__)
main.PPG = 18
PPG=main.PPG


class Website(Website):

    @http.route()
    def theme_customize(self, enable=None, disable=None, get_bundle=False):
        """ enable or Disable lists of ``xml_id`` of the inherit templates """

        self._get_customize_views(disable).write({'active': False})
        self._get_customize_views(enable).write({'active': True})
       
                
        if enable:
            for i in enable:
                _logger.info('temp %s ', i)
                if i.startswith('theme_impacto.header_style_'):
                     if  not i.endswith('_css'):
                         tempteml = i+'_css'
                         themeviews = request.env['ir.ui.view'].search([('key','ilike','theme_impacto.header_style_')])
                         for v in themeviews:
                            if v.key.endswith('_css'):
                                self._get_customize_views([v.key]).write({'active': False})
                         self._get_customize_views([tempteml]).write({'active': True})
        if get_bundle:
            context = dict(request.context)
            return {
                'web.assets_common': request.env['ir.qweb']._get_asset_link_urls('web.assets_common', options=context),
                'web.assets_frontend': request.env['ir.qweb']._get_asset_link_urls('web.assets_frontend', options=context),
                'website.assets_editor': request.env['ir.qweb']._get_asset_link_urls('website.assets_editor', options=context),
            }

        return True
        