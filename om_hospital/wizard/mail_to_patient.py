from odoo import api,fields, models

class MailToPatient(models.TransientModel):
    _name = "mail.to.patient"
    _description = "Mail To Patient"

    selected_fields_ids = fields.Many2many('ir.model.fields',domain=[('model','=','hospital.patient')] , string = 'Select Fields')

    def send_a_mail(self):
        lst = []
        for rec in self.selected_fields_ids:
            lst.append(rec.name)
        dict = {'var1' : lst }
        
        template = self.env.ref('om_hospital.view2_mail_to_patient')
        print("************************ This is template ************************", template)
        template.with_context(dict).send_mail(self.env.context['active_id'], force_send=True)  # force_send=True   "aanathi tatkalik mail sendthai jay "at a time"""
        print('***************selected_fields_ids****************',MailToPatient.selected_fields_ids)

        # ************ RELOAD THE PAGE ************
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }