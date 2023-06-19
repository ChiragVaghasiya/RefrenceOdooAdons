# -*- coding: utf-8 -*-
# from odoo import http


# class TempOdoomodule(http.Controller):
#     @http.route('/temp_odoomodule/temp_odoomodule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/temp_odoomodule/temp_odoomodule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('temp_odoomodule.listing', {
#             'root': '/temp_odoomodule/temp_odoomodule',
#             'objects': http.request.env['temp_odoomodule.temp_odoomodule'].search([]),
#         })

#     @http.route('/temp_odoomodule/temp_odoomodule/objects/<model("temp_odoomodule.temp_odoomodule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('temp_odoomodule.object', {
#             'object': obj
#         })
