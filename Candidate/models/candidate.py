from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
import re


class RecruitmentCandidate(models.Model):
    _name = "recruitment.candidate"
    _description = "Recruitment Candidate"

    name = fields.Char(string="Candidate Name", required=True)
    email = fields.Char(string="Email", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    degree = fields.Selection(
        [('graduate', 'Graduate'),
         ('bachelor_degree ', 'Permanante Employee'),
         ('master_degree', 'Master Degree'),
         ('doctoral_degree', 'Doctoral Degree')], string="Degree")
    applied_job = fields.Char(string="Applied Job")
    current_company = fields.Char(string="Current Company")
    current_city = fields.Char(string="Current City")
    skills = fields.Many2many(comodel_name="hr.applicant.category", required=True)
    current_salary = fields.Integer(string="Current Salary")
    expected_salary = fields.Integer(string="Expected Salary")
    referred_by = fields.Many2one(comodel_name="res.users", string="Referred By")
    experience_in_months = fields.Integer(string="Experience in Months")
    current_experience = fields.Float(string="Current Experience", compute="_compute_current_experience")
    # current_experience = fields.Integer(string="Current Experience")

    @api.constrains('mobile', 'email')
    def validation(self):
        for rec in self:
            # print(rec.mobile)
            regex_mobile = "^\d{10}$"
            regex_mail = "^\w([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$"
            check_mobile = re.findall(regex_mobile, rec.mobile)
            check_mail = re.findall(regex_mail, rec.email)
            # print(check_mobile)
            if not check_mobile:
                raise ValidationError(_("Enter valid 10 digit mobile number"))
            if not check_mail:
                raise ValidationError(_("Enter valid Email"))

    @api.depends('experience_in_months')
    def _compute_current_experience(self):
        for rec in self:
            if rec.experience_in_months:
                rec.current_experience = (rec.experience_in_months / 12)
            else:
                rec.current_experience = 0
        # total_months = 23
        # years, months = divmod(total_months, 12)
        # print(f"{years} years, {months} months")