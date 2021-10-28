# coding=utf-8

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    """ Purchase Order modifier for vendor information """
    _inherit = "purchase.order.line"

    supplier_info = fields.Text("Supplier Information")

    @api.onchange('product_id')
    def onchange_product_id_for_vendor_info(self):
        """ Setting Vendor Info on change of product_id """
        for rec in self:
            if rec.product_id:
                seller = rec.product_id.with_company(rec.order_id.company_id)._select_seller(
                    partner_id=rec.order_id.partner_id,
                    quantity=rec.product_qty,
                    date=rec.order_id.date_order and rec.order_id.date_order.date(),
                    uom_id=rec.product_id.uom_po_id
                )
                rec.supplier_info = seller.vandor_product_information
            # for supplier in rec.product_id.seller_ids:
            #     if rec.order_id.partner_id.id == supplier.name.id:
            #         rec.supplier_info = supplier.vandor_product_information

    def get_additional_info(self):
        """ Getting additional information from """
        vendor_info_dict = {}
        for rec in self:
            seller = rec.product_id.with_company(rec.order_id.company_id)._select_seller(
                partner_id=rec.order_id.partner_id,
                quantity=rec.product_qty,
                date=rec.order_id.date_order and rec.order_id.date_order.date(),
                uom_id=rec.product_id.uom_po_id
            )
            if seller:
                vendor_info_dict['code'] = seller.product_code
                vendor_info_dict['product_name'] = seller.product_name
                vendor_info_dict['additional_info'] = seller.vandor_product_information
        return vendor_info_dict
    
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
        res = super(PurchaseOrderLine, self)._prepare_purchase_order_line(product_id, product_qty, product_uom,
                                                                          company_id, supplier, po)
        uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id.with_company(company_id)._select_seller(
            partner_id=supplier.name,
            quantity=uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id)
        if seller:
            res['supplier_info'] = seller.vandor_product_information
        return res


class SupplierInfoModifier(models.Model):
    """ Supplier information modifier """
    _inherit = "product.supplierinfo"

    vandor_product_information =fields.Text("Vendor Product Information")