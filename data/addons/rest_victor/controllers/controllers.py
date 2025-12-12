# from odoo import http


# class RestVictor(http.Controller):
#     @http.route('/rest_victor/rest_victor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rest_victor/rest_victor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rest_victor.listing', {
#             'root': '/rest_victor/rest_victor',
#             'objects': http.request.env['rest_victor.rest_victor'].search([]),
#         })

#     @http.route('/rest_victor/rest_victor/objects/<model("rest_victor.rest_victor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rest_victor.object', {
#             'object': obj
#         })

