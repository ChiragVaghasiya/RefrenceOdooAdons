from odoo import api,fields, models
from datetime import date
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"    #creating a datbase tabale  with this name "hospital_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']      #inheriting the module in the our py files
    _description = "Hospital Patient"

    name = fields.Char(string = "Name", tracking=True , help="Help Massage!!!!!")
    date_of_birth = fields.Date(string = "Date Of Birth")
    age = fields.Integer(string = "Age", compute = '_compute_age' , tracking=True , store=True)      # "computed fields" is not stor in a our postgress database ...
    ref = fields.Char(string = "Refrence", tracking=True)
    parent = fields.Char(string = "Parent", tracking=True )
    active = fields.Boolean(string = "Active" , default=True, tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string ='Gender', tracking=True , default='male')
    image = fields.Image(string="Image")
    tags_ids = fields.Many2many('patient.tags', string = "Tags")   # many 2 many filed e database ni ander tenu potanu seprate table banave ....... ane tene access karva mate ui ma jaine jovu many2many relations ma ... 
    is_birthday = fields.Boolean(string = "Birthday ?" , compute = '_compute_is_birthday')
    email = fields.Char(string = "Email", tracking=True )
    phone = fields.Integer(string = "Phone", tracking=True )
    website = fields.Char(string = "Website", tracking=True )
    # tracking=1
    # tracking=2   Aa rite Lakhavthi UI ma 1,2,3,4.... aa rite positions ma Dekhase ....
    # tracking=3    
    # tracking=4
    # tracking=5

    @api.model
    def test_cron_job(self):
        print("****************** You next Activity is Schedual on ******************")

    @api.model
    def create(self , values):
        print("Manually Created Functions" , values)
        return super(HospitalPatient,self).create(values)
    
    def write(self,values):
        if not self.ref and not values.get('ref'):
            values['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).write(values)

    # *********** on_delet Function ************ #
    @api.ondelete(at_uninstall=False)    # aani nichenu function tyare Run thase ke jyare koi delet thase ...
    def _check_tags(self):
        for rec in self:
            if rec.tags_ids:
                raise ValidationError('You can not delet a paientt with tags !!!!!!!!!')


    # ************ Python Constraints ************* #
    @api.constrains('date_of_birth')   # Validation for Date of Birth #
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError('The Enterd Date of Birth is Not Acceptable !!!!')

    # **************** add dependencies *******************
    @api.depends('date_of_birth')   # at a time a function has been a run ....
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0
    
    def action_test(self):
        print("***************clickes*************")
        return

    # **************** Add dependencies ******************* #
    @api.depends('date_of_birth')   # At a time a function has been a run ....
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if ( ( today.day == rec.date_of_birth.day ) and ( today.month == rec.date_of_birth.month ) ):
                    is_birthday = True
            rec.is_birthday = is_birthday