import json
from difflib import SequenceMatcher

from odoo import http, tools, _
from odoo.http import request

class WebsiteSale(http.Controller):
    @http.route(['/shop/get_suggest'], type='http', auth="public", methods=['GET'], website=True)
    def get_suggest_json(self, **kw):
        query = kw.get('query')
        names = query.split(' ')
        domain_name = ['|' for k in range(len(names) - 1)] + [('name', 'ilike', name) for name in names]
        domain_default_code = ['|' for k in range(len(names) - 1)] + [('default_code', 'ilike', name) for name in names]
        domain_keyword1 = ['|' for k in range(len(names) - 1)] + [('bam_product_keyword1', 'ilike', name) for name in names]
        domain_keyword2 = ['|' for k in range(len(names) - 1)] + [('bam_product_keyword2', 'ilike', name) for name in names]
        domain_keyword3 = ['|' for k in range(len(names) - 1)] + [('bam_product_keyword3', 'ilike', name) for name in names]
        domain_keyword4 = ['|' for k in range(len(names) - 1)] + [('bam_product_keyword4', 'ilike', name) for name in names]
        domain_keyword5 = ['|' for k in range(len(names) - 1)] + [('bam_product_keyword5', 'ilike', name) for name in names]
        domain = domain_name + domain_default_code
        domain.insert(0, '|')
        domain += domain_keyword1
        domain.insert(0, '|')
        domain += domain_keyword2
        domain.insert(0, '|')
        domain += domain_keyword3
        domain.insert(0, '|')
        domain += domain_keyword4
        domain.insert(0, '|')
        domain += domain_keyword5
        domain.insert(0, '|')
        products = request.env['product.template'].search(domain)
        products = sorted(products, key=lambda x: SequenceMatcher(None, query.lower(), x.name.lower()).ratio(),
                          reverse=True)
        results = []
        for product in products:
            value = product.name
            if product.default_code:
                value = '['+ product.default_code +'] '+ product.name
            results.append({'value': value, 'data': {'id': product.id, 'after_selected': product.name}})
        return json.dumps({
            'query': 'Unit',
            'suggestions': results
        })