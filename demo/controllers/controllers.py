# -*- coding: utf-8 -*-
from odoo import http   
from odoo.http import request


class Demo(http.Controller):

    @http.route('/demo/demo', website=True , auth='user')
    def index(self, **kw):
        # return "Hello , world"
        patients = request.env['hospital.patient'].sudo().search([])
        print(patients)
        return request.render("demo.aspire_dashboard",{
            'patients':patients
        })

    @http.route('/hosptal/form', website=True , auth='user')    
    def web(self, **kw):
        # print("*****************KW*****************",kw)
        request.env['hospital.patient'].sudo().create(kw)
        return request.render("demo.hospital_patient_form",{})

