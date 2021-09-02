from odoo import api, fields, models



class MegamenuContent(models.Model):
    _name = 'megamenu.content'
    _description = 'Website Megamenu Content'
    name=fields.Char(string='Megamenu Content Name',translate=True)    
    megamenu_type = fields.Selection([('2_col', '2 Columns'),
                                      ('3_col', '3 Columns'),
                                      ('4_col', '4 Columns'),('5_col', '5 Columns'), ('6_col', '6 Columns')],
                                     default='3_col',
                                     string="Megamenu type")

    megamenu_bg_image = fields.Binary(string="Background image for megamenu")
    display_menu_header = fields.Boolean(string="Display menu header", default=False,
                                         help="For displaying header in megamenu")
    menu_header = fields.Html(string="Header content", translate=True,
                              help="Header name for megamenu")
    display_menu_footer = fields.Boolean(string="Display menu footer", default=False,
                                         help="For displaying footer in megamenu")
    menu_footer = fields.Html(string="Footer content", translate=True,
                              help="Footer name for megamenu")

    megamenu_content_type = fields.Selection([('static', 'Static Content')],
                                          default="static",
                                          help="Change megamenu behaviour",
                                          string="Content type")

    megamenu_static_content = fields.Html(string='Static Content')
    

class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    is_megamenu = fields.Boolean(string='Is Dynamic megamenu...?')
    megamenu_content_id=fields.Many2one('megamenu.content',string='Content')




class Website(models.Model):
    _inherit = 'website'


    def get_megamenu_pages(self, submenu):
        menus = self.env['website.menu'].sudo().search(
            [('parent_id', '=', submenu.id)])
        return menus
