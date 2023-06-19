from odoo import api,fields, models
from odoo.exceptions import ValidationError
import random

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'      # aa name show kare uper Tital ma , jyare aapde patient ne search karine joie tyare 

    # _order = "id desc"   ####### treee view ni ander "id" field e "decrising-order" ma dekhase ######
    _order = "id desc"
    # _order = "id desc , xyz asd"   #### Multiple arguments Work with this syntax ####

    # patient_id = fields.Many2one('hospital.patient', string="Patient Name" , ondelete='cascade')   #  'cascade' & 'restrict'Aa banne Ek-Bijane Connected 6 ...
    patient_id = fields.Many2one('hospital.patient', string="Patient Name" , ondelete='restrict')
    # patient_id = fields.Many2one(string="Patient Name", comodel_name='hospital.patient')
    
    gender = fields.Selection(related='patient_id.gender')
    # gender = fields.Selection(related='patient_id.gender',readonly=False)  # this field editabale & it reflect on origanal field ........
    ref = fields.Char(string="Refrence")
    precription = fields.Html(string='Precription')
    # appointment_time = fields.Datetime(string="Appointment Time" , default=fields.Datetime.now)
    appointment_date = fields.Date(string="Appointment Date" , default=fields.Date.context_today)
    booking_date = fields.Date(string="Booking Date" , default=fields.Date.context_today)
    doctor_id = fields.Many2one('res.users', string="Dcotor")
    priority = fields.Selection([
        ('0','Normal'),
        ('1','Low'),
        ('2','High'),
        ('3','Very High')] , string='Priority' , tracking=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('in_consultation','In_Consultation'),
        ('done','Done'),
        ('cancel','Cancelled')] , default = 'draft' , tracking=True , string = 'Status' , required=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines') # ********* One2many field is  defining in a Main Model ............... ane vachma many2one field aave
    hide_sales_price = fields.Boolean(string="Hide-Sales Price")
    progress = fields.Integer(string="Progress" , compute='_compute_progress')
    amount = fields.Integer(string="Amount")
    duretion = fields.Float(string="Duretion")
    
    # currency_id = fields.Many2one('res.currency', required=True)



    # ******************** ONCHANGE ****************** #
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref


    # ************** This function is run when the button is click *************** #
    def action_test(self):
        # print("................action test.................")
        return {
            'type': 'ir.actions.act_url',
            'target' : 'new', 
            'url' : 'https://www.odoo.com'
        }
    
    # ************** OVERRIDE THE UNLINK FUNCTION ************** #
    def unlink(self):
        if self.state == 'done':
            raise ValidationError('You Can Not Delet Apoointment With Done Stats !!!')
        return super(HospitalAppointment,self).unlink()

    # ***************** This function is run when the button is click **************** #
    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Done !!!",
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        return self.env.ref('om_hospital.action_cancel_appointment').read()[0]
    
    # Add Dependency #
    @api.depends('state')
    def _compute_progress(self):
        for rec in self :
            if rec.state == 'draft':
                progress = random.randrange(0,25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25,99)
            elif rec.state == 'done':
                progress = 100
            else :
                progress = 0
            rec.progress = progress

    # *********** Whatsapp ***********
    def action_share_whatsapp(self):

        if not self.patient_id.phone :
            raise ValidationError("Missing Phone Number in Patient record !!!")

        massage = 'Hi *%s* , Your *appointment* number is : %s , Thank You' % (self.patient_id.name,self.patient_id.name)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone , massage)

        return{
            'type': 'ir.actions.act_url',
            'target' : 'new', 
            'url' : whatsapp_api_url
        }
                
class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product' , required=True)
    price_unit = fields.Float(string = "Price" , related='product_id.list_price')
    qty = fields.Integer(string = "Quantity", default="1")
    # *********** This fields is required for  use a One2many field ,,,,,,, and This field iss given a name of the appoint patient name
    appointment_id = fields.Many2one('hospital.appointment' , string='Appointment')
    # price_subtotal = fields.Monetary(string = "Subtotal")