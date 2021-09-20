{
    'name': 'Transus',
    'summary': 'Base module of a Transus connector',
    'license': 'AGPL-3',
    'author': 'GRIPCIT',
    'website': '',
    'category': 'Technical Settings',
    'version': '14.0.1.0.0',
    'depends': [
        'base',
        # 'partner_identification_gln',  # TODO evaluate adoption of this OCA module
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/transus_security_rule.xml',
        'data/ir_config_parameter_data.xml',
        'data/ir_cron.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/transus_action.xml',
    ],
}
