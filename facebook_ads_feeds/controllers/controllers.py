# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################
from odoo import http
from odoo.http import request,Response
import werkzeug
import base64

def binary_content(xmlid=None, model='ir.attachment', id=None, field='datas', unique=False,
                   filename=None, filename_field='datas_fname', download=False, mimetype=None,
                   default_mimetype='application/octet-stream', access_token=None, env=None):
    return request.registry['ir.http'].binary_content(
        xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
        filename_field=filename_field, download=download, mimetype=mimetype,
        default_mimetype=default_mimetype, access_token=access_token)

class FacebookShop(http.Controller):
    @http.route(['/shop/<int:id>/content','/shop/<int:id>/content/<string:filename>'], csrf=False, type='http', auth="public",website=True)
    def view_data(self,id=None, filename=None, download=None, mimetype=None, access_token=None, token=None, **kw):
        shop = request.env['fb.facebook.shop'].sudo().browse(id)
        if shop.feeds_security == 'manual' and request.env['res.users'].browse(request.uid)._is_public():
            return request.not_found()
        if shop.feeds_security == "automatic" and shop.enable_token:
            if not token or shop.feed_token != token:
                return request.not_found()
        rec = http.request.env["fb.attachment.mapping"].sudo().search([('fb_shop','=',id),('latest','=',True)],limit=1)
        if rec:
            att_id=rec.attachment_id
            status, headers, content = request.env['ir.http'].binary_content(
                xmlid=None, model='ir.attachment', id=att_id, field='datas', unique=None, filename=filename,
                filename_field='datas_fname', download=download, mimetype=mimetype,
                access_token=access_token)
            if status == 304:
                response = werkzeug.wrappers.Response(status=status, headers=headers)
            elif status == 301:
                return werkzeug.utils.redirect(content, code=301)
            elif status != 200:
                response = request.not_found()
            else:
                content_base64 = base64.b64decode(content)
                headers.append(('Content-Length', len(content_base64)))
                response = request.make_response(content_base64, headers)
                rec.write({'updated':True})
            if token:
                response.set_cookie('fileToken', token)
            return response
        else:
            return request.not_found()

