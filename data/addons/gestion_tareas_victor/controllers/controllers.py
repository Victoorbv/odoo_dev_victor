# from odoo import http


# class GestionTareasVictor(http.Controller):
#     @http.route('/gestion_tareas_victor/gestion_tareas_victor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_victor/gestion_tareas_victor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_victor.listing', {
#             'root': '/gestion_tareas_victor/gestion_tareas_victor',
#             'objects': http.request.env['gestion_tareas_victor.gestion_tareas_victor'].search([]),
#         })

#     @http.route('/gestion_tareas_victor/gestion_tareas_victor/objects/<model("gestion_tareas_victor.gestion_tareas_victor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_victor.object', {
#             'object': obj
#         })

