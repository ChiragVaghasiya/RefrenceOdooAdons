from odoo import api,fields, models
from odoo.exceptions import ValidationError
import random

class GenerateJob(models.Model):
    _name = 'generate.job'
    _description = 'Generate Job'

    name = fields.Char(string = "Opening Kick-off ", help="Enter Your Name !!!!")
    skills = fields.Many2many('hr.applicant.category', string = "Skills") 
    min_exp_req = fields.Integer(string = "Minimum Exp. Req.",default="0" , help="Enter Exp. Of Year !!!!")   #  **********
    max_exp_req = fields.Integer(string = "Maximum Exp. Req.",default="0" , help="Enter Exp. Of Year !!!!")   #  **********
    priority = fields.Selection([
        ('0','Normal'),
        ('1','Low'),
        ('2','High'),
        ('3','Very High')] , string='Requied Priority' , tracking=True)
    open_date = fields.Date(string="Opened Date" , default=fields.Date.context_today)
    expected_end_date = fields.Date(string="Expected End Date")
    expected_new_employee = fields.Integer(string = "Expected New Employee", default="1" )
    approver = fields.Many2one('res.users', string="Approver")
    description = fields.Text(string="Job Description")
    state = fields.Selection([
        ('draft','Draft'),
        ('submiteed','Submiteed'),
        ('approved','Approved'),
        ('refuced','Refuced')] , default = 'draft' , string = 'Status' , required=True)
    
    # ***************** This function is run when the button is click **************** #
    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_submiteed(self):
        for rec in self:
            rec.state = "submiteed"

    def action_approved(self):
        for rec in self:
            rec.state = "approved"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Approved !!!",
                'type': 'rainbow_man',
            }
        }

    def action_refuced(self):
        for rec in self:
            rec.state = "refuced"

    # ***********************  METHOD-1   ***********************
    # def action_send(self):
    #     candidate_data = self.env['recruitment.candidate'].search([])
    #     application_data = self.env['hr.applicant'].search([])

    #     for j in candidate_data :

    #         if ((self.skills == j.skills ) and (self.min_exp_req <= j.current_experience) and (self.max_exp_req >= j.current_experience) ):
    #             flag = 0
    #             for i in application_data :
    #                 if ( j.name != i.partner_name ):
    #                     flag =0
    #                 else :
    #                     flag = 1
    #                     break

    #             if flag == 0:
    #                 self.env['hr.applicant'].create({
    #                     'name':self.name ,
    #                     'partner_name':j.name ,
    #                     'email_from':j.email , 
    #                     'partner_phone':j.mobile , 
    #                     'salary_expected':j.expected_salary 
    #                     })

    # ***********************  METHOD-2   ***********************
    def action_send(self):
        Job_skills=[]
        candidate_data = self.env['recruitment.candidate'].search([])

        for i in self.skills:
            Job_skills.append(i.id)

        for j in candidate_data :
            candidate_skills = []
            count = 1

            for k in j.skills:
                candidate_skills.append(k.id)

            for m in candidate_skills :
                if count == 0:
                    break
                for n in Job_skills :
                    if m == n :
                        count = 0
                        break
                       
            if ( (count == 0) and (self.min_exp_req <= j.current_experience) and (self.max_exp_req >= j.current_experience) ):

                if ( self.env['hr.applicant'].search([( 'partner_name', '=', j.name )]) ):
                    continue 

                else :
                    self.env['hr.applicant'].create({
                        'name':self.name ,
                        'partner_name':j.name ,
                        'email_from':j.email , 
                        'partner_phone':j.mobile , 
                        'salary_expected':j.expected_salary 
                        })
            count = 1
            candidate_skills = []

        Job_skills=[]

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Application Send Successfully !!!",
                'type': 'rainbow_man',
            }
        }