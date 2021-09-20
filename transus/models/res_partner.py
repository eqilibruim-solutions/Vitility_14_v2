# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    transus_gln = fields.Char(string='GLN')

    _sql_constraints = [
        ('name_uniq', 'unique(transus_gln, company_id)', 'Partner GLN must be unique per company!'),
    ]

    @api.constrains('transus_gln')
    def check_transus_gln(self):
        for partner in self:
            if partner.transus_gln and len(partner.transus_gln) != 13:
                raise ValidationError("The entered GLN is not correct for partner [%s]" % partner.name)