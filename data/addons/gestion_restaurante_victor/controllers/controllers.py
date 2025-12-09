# from odoo import http


# class GestionRestauranteVictor(http.Controller):
#     @http.route('/gestion_restaurante_victor/gestion_restaurante_victor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_victor/gestion_restaurante_victor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_victor.listing', {
#             'root': '/gestion_restaurante_victor/gestion_restaurante_victor',
#             'objects': http.request.env['gestion_restaurante_victor.gestion_restaurante_victor'].search([]),
#         })

#     @http.route('/gestion_restaurante_victor/gestion_restaurante_victor/objects/<model("gestion_restaurante_victor.gestion_restaurante_victor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_victor.object', {
#             'object': obj
#         })

