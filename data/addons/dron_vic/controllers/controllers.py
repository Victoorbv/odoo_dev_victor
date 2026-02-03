# from odoo import http


# class DronVic(http.Controller):
#     @http.route('/dron_vic/dron_vic', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dron_vic/dron_vic/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dron_vic.listing', {
#             'root': '/dron_vic/dron_vic',
#             'objects': http.request.env['dron_vic.dron_vic'].search([]),
#         })

#     @http.route('/dron_vic/dron_vic/objects/<model("dron_vic.dron_vic"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dron_vic.object', {
#             'object': obj
#         })

