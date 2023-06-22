from odoo import models, fields, api


class UsersRole(models.Model):
    _name = 'users.role'
    _description = 'Users Role'
    _rec_name = 'role_name'

    role_name = fields.Char("Role", required=True)
    color = fields.Integer("")


class Users(models.Model):
    _name = 'users.model'
    _description = 'Users'
    _rec_name = 'user_name'

    # _inherit = 'mail.thread'

    @api.onchange('first_name', 'last_name')
    def _get_user_name(self):
        for rec in self:
            result = ""
            if rec.first_name:
                result += rec.first_name + " "
            if rec.last_name:
                result += rec.last_name

            rec.user_name = result

    first_name = fields.Char("First Name", required=True)
    last_name = fields.Char("Last Name", required=True)
    user_name = fields.Char("Name", compute='_get_user_name', readonly=True, store=True)
    phone_no = fields.Integer("Phone Number")
    password_domain = fields.Char("Password")
    email = fields.Char("Email Address", required=True)
    address1 = fields.Char("Address1")
    address2 = fields.Char("Address2")
    country = fields.Many2one('res.country', "Country")
    state = fields.Many2one('res.country.state', "State")
    city = fields.Char("City")
    role = fields.Many2many('users.role', string="Role", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], "Gender", default='male', required=True)
    active_user = fields.Selection([('', ''), ('green', 'Green'), ('red', 'Red')], "User")
    active_user2 = fields.Boolean("User Status", copy=False)
    fix_email = fields.Char("Fix Email", required=True, default="sagar.panchal@aspiresoftserv.com")
    color = fields.Integer("")

    @api.model
    def create(self, values):
        group_roles = {'Admin': "project_j_admin", 'Approver/Master': "project_j_approver",
                       'Data Entry': "project_j_data_entry", 'Document Reviewer': "project_j_document_reviewer",
                       'Magazine Reviewer': "project_j_magazine_reviewer", 'Reviewer': "project_j_reviewer"}

        if 'user_name' in values:
            name = values['user_name']
        if 'password_domain' in values:
            password = values['password_domain']
        if 'email' in values:
            email = values['email']

        vals = {
            'name': name,
            'login': email
        }

        user = self.env['res.users'].create(vals)

        roles = []
        roles = self.env['users.role']
        if 'role' in values:
            for rec in values['role'][0][2]:
                role = roles.browse(rec)
                if role:
                    grp = group_roles[role.role_name]
                    ref = "project_j." + grp
                    group_id = self.env.ref(ref)
                    group_id.users = [(4, user.id)]

        # name = values['']
        # name = values['']
        # name = values['']
        # name = values['']
        # name = values['']

        # template_id = self.env.ref('project_j.password_set_up_mail_template').id
        # mail_id = self.pool.get('mail.template').send_mail(self._cr,self._uid,template_id,self.id, force_send=True)
        # mail_template = self.env.ref('project_j.password_set_up_mail_template')
        # mail_template.send_mail(self.id, force_send=True)

        record = super(Users, self).create(values)
        return record
