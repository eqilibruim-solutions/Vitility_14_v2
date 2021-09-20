{
    'name': 'Connector Transus - Purchase Order Send',
    'summary': 'Transus connection for purchases.',
    'license': 'AGPL-3',
    'author': 'GRIPICT',
    'website': '',
    'category': 'Purchases',
    'version': '14.0.1.0.0',
    'depends': [
        'purchase',
        'transus',
    ],
    'data': [
        'templates/transus.xml',
        'views/res_partner_view.xml',
    ],
}
