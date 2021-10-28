# coding=utf-8
{
    'name': "Purchase Order Modifier",
    'description': "Purchase Order modifier to add new columns in Supplier Information(on Products) to provide more information on supplier side. As well as report changes of Purchase Order.",
    'author': 'Petit B.V.',
    'website': 'www.bepetit.nl',
    'category': 'Purchase',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'purchase', 'purchase_stock'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_purchase_order_modifier.xml',
        'views/purchase_order_modifier.xml',
    ],
}
