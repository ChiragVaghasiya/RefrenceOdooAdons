from odoo import api,fields, models
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta

class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment"
    _description = "Cancel Appointment"

# ****** Default name mate ( Default Filed Name Aavi Jase ) ******
    @api.model
    def default_get(self,fields):
        res = super(CancelAppointment , self).default_get(fields)
        res['appointment_idd'] = self.env.context.get('active_id')
        return res

    appointment_idd =fields.Many2one("hospital.appointment" , string = "Appointment Idd")
    reason =fields.Text(string = "Reason")
    date_cancel =fields.Date(string = "Cancellation Date", default = fields.Date.context_today)

    def action_cancel(self):
        ###### Cheking for the Date Or Not ######
        if (self.appointment_idd.appointment_date == datetime.date.today() ):
            raise ValidationError("Sorry, Cancellation is not allowed on th Same day of Appointment !!!!!")
        else :
            appointment_id = self.env.context['active_id']
            appointment = self.env['hospital.appointment'].browse(appointment_id)
            appointment.state = 'cancel'
        ######

        ########### Access the "ResConfigSettings" fields ###########
        canel_day = self.env['ir.config_parameter'].get_param('om_hosptal.cancel_day')
        print("**********Cancel_day*********",canel_day)
        allowed_date = self.appointment_idd.appointment_date - relativedelta(days=int(canel_day))
        print("**********allowed_date************",allowed_date)

        if allowed_date < datetime.date.today():
            raise ValidationError('Sorry , Cancellation is not allowed for this Appointment !!!!!')
        ############
        
        return
    