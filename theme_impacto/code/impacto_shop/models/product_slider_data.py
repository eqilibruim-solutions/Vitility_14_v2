from odoo.osv import osv
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models, _, tools

class product_slider_data(osv.osv):
    _name = 'product.slider'
    _Slider_data = True

    def get_slider_product(self, collection_id, limit, context=None):
        collection_data = self.get_slider_collection_data(collection_id)
        if collection_data:
            object_ids = request.env[collection_data['model']].sudo().search(collection_data['domain'],limit=limit,order=collection_data['order'], )
            return {'objects': object_ids,'name': 'name' in collection_data and collection_data['name'] or _("All Products")}
        
    def get_slider_collection_data(self, collection_id):
        if collection_id:
            res = {'order': False}
            collection_data = request.env['website.filter'].sudo().browse(collection_id)
            res['domain'] = safe_eval(collection_data.collection_id.domain, {'uid': request.uid})
            res['model'] = collection_data.collection_id.model_id
            res['name'] = collection_data.name
            return res
        else:
            return {'domain': [], 'model': 'product.template', 'order': False}


class ProductFilter(models.Model):
    _name = "website.filter"
    _rec_name = "name"

    collection_id = fields.Many2one("ir.filters", "Select Filter")
    name = fields.Char("Filter Name")
    Is_published = fields.Boolean("Is Published")

class ProductTemplateExt(models.Model):
    _inherit = ['product.template', 'product.slider' ]
    _name = 'product.template'
    
    is_best_seller_product = fields.Boolean(string='Is Best Seller ?')
    is_discount_product = fields.Boolean(string='Offer Discount ?')
    is_special_product = fields.Boolean(String='Is Special Product?')
    is_new_arrival = fields.Boolean(string='New Arrival ?')
    ribbon_title = fields.Char(string='Ribbon Title', size=25, translate=True)
