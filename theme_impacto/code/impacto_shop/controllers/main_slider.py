from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers import main


class Product_Snippet(http.Controller):

    def review_rating_stat(self, product, context=None):
        rating_product = product.rating_get_stats(
            [('website_published', '=', True)])
        return rating_product

    @http.route(['/slider/get_data'], type='json',auth='public', website=True, csrf=False, cache=600)
    def render_product_slider(self, template=False, collection_id=False,objects_in_slide=4, slidertype='', limit=10):
        new_contxt = dict(request.env.context)
        res = request.env['product.template'].get_slider_product(collection_id=collection_id, limit=limit)

        if not new_contxt.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
        else:
            pricelist = request.env['product.pricelist'].browse(new_contxt['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id

        def compute_currency(price):
            return from_currency.compute(price, to_currency)
        
        new_contxt['compute_currency'] = compute_currency
        new_contxt['pricelist'] = pricelist.id
        new_contxt['review_rating_stat'] = self.review_rating_stat

        request.env.context = new_contxt
        values = {'objects': res['objects'],'title': res['name'],'slidertype' : slidertype }
        return request.env['ir.ui.view'].render_template(template, values)