# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from urllib.request import urlopen,Request
import json
import uuid
import base64
# try:
#     import urllib.request as urllib2
# except ImportError:
#     import urllib2


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    carrier_delivery_type = fields.Selection(related='carrier_id.delivery_type')
    tracker_code = fields.Char("Tracker Code")

    def button_print_dhl_label(self):
        self.ensure_one()

        to_check = [
            (self.carrier_id, 'Carrier'),
            (self.partner_id, 'Partner'),
            (self.company_id, 'Company'),
            (self.number_of_packages, 'Number of Packages'),
            (self.origin, 'Source Document'),
            (self.carrier_id.dhl_user_id, _('DHL User ID on Carrier')),
            (self.carrier_id.dhl_password, _('DHL Password on Carrier')),
            (self.carrier_id.dhl_parcel_type, _('DHL Parcel Type on Carrier')),
            (self.carrier_id.dhl_account_id, _('DHL Account ID on Carrier')),
            (self.carrier_id.dhl_shipment_option,
             _('DHL Shipment Option on Carrier')),
            (self.partner_id.country_id, _('Country ID on Partner')),
            (self.partner_id.zip, _('Postal Code on Partner')),
            (self.partner_id.street_name, _('Street Name on Partner')),
            (self.partner_id.street_number, _('Street Number on Partner')),
            (self.partner_id.city, _('City on Partner')),
            (self.partner_id.email, _('e-mail on Partner')),
            (self.partner_id.phone, _('Phone on Partner')),
            (self.company_id.partner_id.country_id, _('Country on Company')),
            (self.company_id.partner_id.zip, _('Postal Code on Company')),
            (self.company_id.partner_id.street_name,
             _('Street Name on Company')),
            (self.company_id.partner_id.street_number,
             _('Street Number on Company')),
            (self.company_id.partner_id.city, _('City on Company')),
            (self.company_id.email, _('e-mail on Company')),
            (self.company_id.phone, _('Phone on Company')),
        ]

        for item in to_check:
            if not item[0]:
                raise ValidationError(_("Field ") + item[1] + _(
                    " not found! Please, set it and retry."))

        is_return = False
        for move in self.move_lines:
            if move.origin_returned_move_id:
                is_return = True
                break

        if not self.partner_id.is_company and self.partner_id.parent_id:
            to_check.append(self.partner_id.firstname)
            to_check.append(self.partner_id.lastname)
            to_check.append(self.partner_id.parent_id.name)
        else:
            to_check.append(self.partner_id.name)

        carrier = self.carrier_id
        partner = self.partner_id
        company = self.company_id

        if not partner.is_company and partner.parent_id:
            firstname = partner.firstname
            lastname = partner.lastname
            company_name = partner.parent_id.name
        else:
            firstname = ''
            lastname = ''
            company_name = partner.name

        if carrier.prod_environment:
            api_base_url = 'https://api-gw.dhlparcel.nl/'
        else:
            api_base_url = 'https://api-gw-accept.dhlparcel.nl/'

        try:
            request_xml = json.dumps({
                "userId": carrier.dhl_user_id,
                "key": carrier.dhl_password,
            })

            auth_req = Request(
                url=api_base_url + 'authenticate/api-key',
                data=request_xml,
                headers={'Content-Type': 'application/json'}
            )
            access_token = json.loads(urlopen(auth_req).read())['accessToken']
        except Exception as e:
            raise ValidationError(_("Error during authentication: ") + e.msg)

        tracker_codes = []
        for i in range(0, self.number_of_packages):

            labelId = uuid.uuid4().urn[9:]

            request_xml = {
                "labelId": labelId,
                "orderReference": self.origin,
                "parcelTypeKey": carrier.dhl_parcel_type,
                "receiver": {
                    "name": {
                        "firstName": firstname,
                        "lastName": lastname,
                        "companyName": company_name,
                    },
                    "address": {
                        "countryCode": partner.country_id.code,
                        "postalCode": partner.zip,
                        "city": partner.city,
                        "street": partner.street_name,
                        "additionalAddressLine": partner.street2 or '',
                        "number": partner.street_number,
                        "isBusiness": self.number_of_packages > 1 and True or partner.is_company,
                    },
                    "email": partner.email,
                    "phoneNumber": partner.phone,
                },
                "shipper": {
                    "name": {
                        "firstName": "",
                        "lastName": "",
                        "companyName": company.name,
                    },
                    "address": {
                        "countryCode": company.partner_id.country_id.code,
                        "postalCode": company.partner_id.zip,
                        "city": company.partner_id.city,
                        "street": company.partner_id.street_name,
                        "number": company.partner_id.street_number,
                        "isBusiness": True,
                    },
                    "email": company.email,
                    "phoneNumber": company.phone,
                },
                "accountId": carrier.dhl_account_id,
                "options": [
                    {
                        "key": carrier.dhl_shipment_option,
                    },
                    {
                        "key": "REFERENCE",
                        "input": self.origin,
                    }
                ],
                "returnLabel": is_return,
                "pieceNumber": i + 1,
                "quantity": self.number_of_packages,
                "automaticPrintDialog": True
            }

            if carrier.saturday_delivery:
                request_xml["options"].append({
                    "key": "S",
                })
            if carrier.evening_delivery:
                request_xml["options"].append({
                    "key": "EVE",
                })

            request_xml = json.dumps(request_xml)

            try:

                labels_req = Request(
                    url=api_base_url + 'labels',
                    data=request_xml,
                    headers={'Content-Type': 'application/json'}
                )

                labels_req.add_header("Authorization",
                                      "Bearer %s" % access_token)
                labels_req.add_header("Accept", "application/pdf")
                label_data = urlopen(labels_req).read()
                label_data = base64.b64encode(label_data)

            except Exception as e:
                raise ValidationError(
                    _("Error during label creation: ") + e.msg)

            try:

                retrieve_req = Request(
                    url=api_base_url + 'labels/' + labelId,
                    headers={'Content-Type': 'application/json'}
                )
                retrieve_req.add_header("Authorization",
                                        "Bearer %s" % access_token)

                retrieve_data = urlopen(retrieve_req).read()
                tracker_codes.append(json.loads(retrieve_data)['trackerCode'])
            except Exception as e:
                raise ValidationError(
                    _("Error during label retrieval: ") + e.msg)

            self.env['ir.attachment'].create({
                'name': self.name + '-' + str(i + 1) + '/' + str(
                    self.number_of_packages) + '.pdf',
                'datas': label_data,
                'datas_fname': self.name + '-' + str(i + 1) + '/' + str(
                    self.number_of_packages) + '.pdf',
                'res_model': 'stock.picking',
                'res_id': self.id,
            })

        self.tracker_code = '; '.join(tracker_codes)

        return

    def button_print_dhl_custom_declartion(self):
        self.ensure_one()
        invoices = self.env['account.invoice'].search([('origin', 'ilike', self.origin)], limit=1, order="id desc")
        to_check = [
            (self.carrier_id, 'Carrier'),
            (self.partner_id, 'Partner'),
            (self.company_id, 'Company'),
            (self.number_of_packages, 'Number of Packages'),
            (self.origin, 'Source Document'),
            (self.carrier_id.dhl_user_id, _('DHL User ID on Carrier')),
            (self.carrier_id.dhl_password, _('DHL Password on Carrier')),
            (self.carrier_id.dhl_parcel_type, _('DHL Parcel Type on Carrier')),
            (self.carrier_id.dhl_account_id, _('DHL Account ID on Carrier')),
            (self.carrier_id.dhl_shipment_option,
             _('DHL Shipment Option on Carrier')),
            (self.partner_id.country_id, _('Country ID on Partner')),
            (self.partner_id.zip, _('Postal Code on Partner')),
            (self.partner_id.street_name, _('Street Name on Partner')),
            (self.partner_id.street_number, _('Street Number on Partner')),
            (self.partner_id.city, _('City on Partner')),
            (self.partner_id.email, _('e-mail on Partner')),
            (self.partner_id.phone, _('Phone on Partner')),
            (self.company_id.partner_id.country_id, _('Country on Company')),
            (self.company_id.partner_id.zip, _('Postal Code on Company')),
            (self.company_id.partner_id.street_name,
             _('Street Name on Company')),
            (self.company_id.partner_id.street_number,
             _('Street Number on Company')),
            (self.company_id.partner_id.city, _('City on Company')),
            (self.company_id.email, _('e-mail on Company')),
            (self.company_id.phone, _('Phone on Company')),
            (self.company_id.vat, _('VAT on Company')),
            (invoices.number, _('Invoice'))
        ]

        for item in to_check:
            if not item[0]:
                raise ValidationError(_("Field ") + item[1] + _(" not found! Please, set it and retry."))

        if not self.partner_id.is_company and self.partner_id.parent_id:
            to_check.append(self.partner_id.firstname)
            to_check.append(self.partner_id.lastname)
            to_check.append(self.partner_id.parent_id.name)
        else:
            to_check.append(self.partner_id.name)

        carrier = self.carrier_id
        partner = self.partner_id
        company = self.company_id

        if not partner.is_company and partner.parent_id:
            firstname = partner.firstname
            lastname = partner.lastname
            company_name = partner.parent_id.name
        else:
            firstname = ''
            lastname = ''
            company_name = partner.name

        if carrier.prod_environment:
            api_base_url = 'https://api-gw.dhlparcel.nl/'
        else:
            api_base_url = 'https://api-gw-accept.dhlparcel.nl/'

        try:
            request_xml = json.dumps({
                "userId": carrier.dhl_user_id,
                "key": carrier.dhl_password,
                "accountNumbers": [
                    carrier.dhl_account_id
                ]
            })

            auth_req = Request(
                url=api_base_url + 'authenticate/api-key',
                data=request_xml,
                headers={'Content-Type': 'application/json'}
            )
            access_token = json.loads(urlopen(auth_req).read())['accessToken']
        except Exception as e:
            raise ValidationError(_("Error during authentication: ") + e.msg)
        customsGoods = []
        shippingFee = {
            "currency": self.sale_id.currency_id.name,
            "value": 0.0
        }
        for move_line in self.move_lines:
            price = move_line.group_id.sale_line_id.price_reduce_taxinc
            if move_line.weight > 0.0:
                customsGoods.append({
                    "code": move_line.product_id.hs_code or '',
                    "description": move_line.product_id.display_name,
                    "origin": move_line.product_id.x_Country_of_origin.code or '',
                    "quantity": move_line.product_uom_qty,
                    "value": price,
                    "weight": move_line.product_id.x_product_detail_package_gross_weight
                })
                shippingFee['value'] += price
        for i in range(0, self.number_of_packages):
            generated_attachment_ids = []
            custom_declartion_id = uuid.uuid4().urn[9:]
            request_xml = {
                "id": custom_declartion_id,
                "orderReference": self.origin,
                "createDocuments": True,
                "accountId": carrier.dhl_account_id,
                "shipper": {
                    "name": {
                        "firstName": "",
                        "lastName": "",
                        "companyName": company.name,
                    },
                    "address": {
                        "countryCode": company.partner_id.country_id.code,
                        "postalCode": company.partner_id.zip,
                        "city": company.partner_id.city,
                        "street": company.partner_id.street_name,
                        "number": company.partner_id.street_number,
                        "isBusiness": True,
                    },
                    "email": company.email,
                    "phoneNumber": company.phone,
                    "vatNumber": company.vat or '',
                    "eoriNumber": company.x_eori_number or ''
                },
                "receiver": {
                    "name": {
                        "firstName": firstname,
                        "lastName": lastname,
                        "companyName": company_name,
                    },
                    "address": {
                        "countryCode": partner.country_id.code,
                        "postalCode": partner.zip,
                        "city": partner.city,
                        "street": partner.street_name,
                        "additionalAddressLine": partner.street2 or '',
                        "number": partner.street_number,
                        "isBusiness": partner.is_company,
                    },
                    "email": partner.email,
                    "phoneNumber": partner.phone,
                    "vatNumber": partner.vat or '',
                    "eoriNumber": partner.x_eori_number or ''
                },
                "currency": company.currency_id.name,
                "invoiceNumber": invoices.number or '',
                # "remarks": "string",
                "invoiceType": "Commercial",
                "exportType": "Permanent",
                "exportReason": 'SaleOfGoods',
                "customsGoods": customsGoods,
                "incoTerms": self.sale_id.incoterm.code or '',
                "incoTermsCity": self.partner_id.city or '',
                "shippingFee": shippingFee,
                "product": "EPL-INT",
                "importerOfRecord": {
                    "name": {
                        "firstName": firstname,
                        "lastName": lastname,
                        "companyName": company_name,
                    },
                    "address": {
                        "countryCode": partner.country_id.code,
                        "postalCode": partner.zip,
                        "city": partner.city,
                        "street": partner.street_name,
                        "additionalAddressLine": partner.street2 or '',
                        "number": partner.street_number,
                        "isBusiness": partner.is_company,
                    },
                    "email": partner.email,
                    "phoneNumber": partner.phone,
                    "vatNumber": partner.vat or '',
                    "eoriNumber": partner.x_eori_number or ''
                },
                "defermentAccountDuties": "GB078457372000",
                "defermentAccountVat": "385694146",
                "vatReverseCharge": False,
                "airWaybillNumber": '',
                "pieceCount": i + 1,
                "trackerCode": self.tracker_code
            }

            request_xml = json.dumps(request_xml)

            try:

                declarations_req = Request(
                    url=api_base_url + 'customs/declarations',
                    data=request_xml,
                    headers={'Content-Type': 'application/json'}
                )

                declarations_req.add_header("Authorization", "Bearer %s" % access_token)
                declaration_data = urlopen(declarations_req).read()
                generated_attachment_ids = [a_dict['id'] for a_dict in
                                            json.loads(declaration_data)['generatedAttachments']]
            except Exception:
                generated_attachment_ids.append(custom_declartion_id)
                pass
            try:
                for attachment_id in generated_attachment_ids:
                    retrieve_req = Request(
                        url=api_base_url + 'customs/attachments/' + attachment_id,
                        headers={'Content-Type': 'application/pdf'}
                    )
                    retrieve_req.add_header("Authorization", "Bearer %s" % access_token)
                    retrieve_req.add_header("Accept", "application/pdf")
                    retrieve_data = urlopen(retrieve_req).read()
                    retrieve_data = base64.b64encode(retrieve_data)
                    self.env['ir.attachment'].create({
                        'name': self.name + '-' + str(i + 1) + '/' + str(
                            self.number_of_packages) + '_CD_invoice' + '.pdf',
                        'datas': retrieve_data,
                        'datas_fname': self.name + '-' + str(i + 1) + '/' + str(
                            self.number_of_packages) + '_CD_invoice' + '.pdf',
                        'res_model': 'stock.picking',
                        'res_id': self.id,
                    })

            except Exception as e:
                raise ValidationError(_("Error during Custom Declaration Creation/Attachment retrieval : [%s: %s]\n\n"
                                        "Data Uploaded are: \n\n %s") % (e.code, e.msg, request_xml))
        return

