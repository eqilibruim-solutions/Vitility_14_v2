{
    'name': 'Delivery Charge Extended',
    'version': '11.0.1.0',
    'sequence': 1,
    'category': 'Stock',
    'description':
        """
        This Module help to add extra changes in delivery

    """,
    'summary': 'add extra changes in delivery',
    'author': 'Mayur Maheshwari',
    'depends': ['delivery'],
    'data': [
        'security/ir.model.access.csv',
        'views/view_product_template.xml',
        'views/delivery_carrier_views.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
