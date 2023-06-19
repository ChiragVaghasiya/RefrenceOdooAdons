from odoo import api,fields, models

class LabAssistence(models.Model):
    _name = "lab.assistence"
    _description = "Lab Assistence"
    _rec_name = 'name'
    _log_access = False  ######### Aanathi model ni field Show nai thase (Ke jyare aapde technicalesni ander joie tyare) #########
    # _order = "name"        ####### treee view ni ander "name" field e order ma dekhase ######
    # _order = "name desc"
    _order = "sequence,id"   ########### id :- field od ma pan aplied thase ############

    name = fields.Char(string = "Lab Tag" , trim=False)
    user_id = fields.Many2one('res.users', string="Dcotor")
    refrence_record = fields.Reference(selection = [
                                                    ('hospital.patient','Patient'),
                                                    ('hospital.appointment','Appointment')
                                                    ] ,
                                                    string = "Record")
    sequence = fields.Integer(string="Sequence" , default=10)