# -*- coding: utf-8 -*-
##############################################################################
#
#    Business Agility Masters
#    Copyright (C) 2018-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Sale order line stock',
    'summary': 'Sale order line stock',
    'description': '''
Add a field in sale order line to show quantity on hand in selected warehouse and amount of products in package.
''',
    'author': 'Busines Agility Masters',
    'website': 'https://www.businessagilitymasters.nl',
    'category': 'Sales',
    'version': '1.0.0',
    'depends': [
        'sale_stock',
        'stock',
        'stock_available'
    ],
    'data': [
        'views/sale_order_view.xml'
    ],
    'installable': True,
}
