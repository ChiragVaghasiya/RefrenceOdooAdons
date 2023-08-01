# -*- coding: utf-8 -*-
# from odoo import http


# class TestOne(http.Controller):
#     @http.route('/project_j/project_j/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_j/project_j/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_j.listing', {
#             'root': '/project_j/project_j',
#             'objects': http.request.env['project_j.project_j'].search([]),
#         })

#     @http.route('/project_j/project_j/objects/<model("project_j.project_j"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_j.object', {
#             'object': obj
#         })
