from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning


class SocialInfo(models.Model):
    _name = 'social.info'
    _description = 'Social Info'
    # _rec_name = 'samiti_id'

    contact_person = fields.Char("Contact Person")
    email = fields.Char("Email", track_visibility='always')
    phone_no = fields.Char("Phone No", track_visibility='always')
    whatsapp_no = fields.Char("Whatsapp No", track_visibility='always')
    Website = fields.Char("Website", track_visibility='always')
    # you_tube = fields.Char("YouTube Channel", track_visibility='always')
    you_tube_channel_name = fields.Char("YouTube Channel Name")
    you_tube_channel_link = fields.Char("YouTube Channel Link")
    twitter_account_name = fields.Char("Twitter Account Name")
    twitter_account_link = fields.Char("Twitter Account Link")
    facebook_field = fields.Char("Facebook", track_visibility='always')
    instagram = fields.Char("Instagram")
    instagram_link = fields.Char("Instagram Link")
    blog = fields.Char("Blog")
    address = fields.Text("Address")
    ref_field = fields.Integer("")

    @api.constrains('address')
    def _check_address(self):
        if self.address != False and self.address != None:
            if len(self.address) > 2000:
                raise ValidationError("Address should must be of 2000 character Max.")

    @api.constrains('phone_no')
    def _check_phone_no(self):
        if self.phone_no != False and self.phone_no != None:
            if len(str(self.phone_no)) > 75:
                raise ValidationError("Phone No should must be of 75 character Max.")

    @api.constrains('whatsapp_no')
    def _check_whatsapp_no(self):
        if self.whatsapp_no != False and self.whatsapp_no != None:
            if len(self.whatsapp_no) > 75:
                raise ValidationError("Whatsapp No should must be of 75 character Max.")

    @api.constrains('email')
    def _check_email(self):
        if self.email != False and self.email != None:

            if '@' not in self.email:
                raise ValidationError("Please enter Valid Email.")
            if '.in' not in self.email and '.com' not in self.email:
                raise ValidationError("Please enter Valid Email.")

            if len(self.email) > 500:
                raise ValidationError("Email should must be of 500 character Max.")

    @api.constrains('facebook_field')
    def _check_facebook_field(self):
        if self.facebook_field != False and self.facebook_field != None:
            if len(self.facebook_field) > 2200:
                raise ValidationError("Facebook should must be of 2200 character Max.")

    @api.constrains('Website')
    def _check_website(self):
        if self.Website != False and self.Website != None:
            if len(self.Website) > 2200:
                raise ValidationError("Website should must be of 2200 character Max.")

    @api.constrains('you_tube')
    def _check_you_tube(self):
        if self.you_tube != False and self.you_tube != None:
            if len(self.you_tube) > 2200:
                raise ValidationError("YouTube should must be of 2200 character Max.")

    @api.constrains('twitter_account_name')
    def _check_twitter_account_name(self):
        if self.twitter_account_name != False and self.twitter_account_name != None:
            if len(self.twitter_account_name) > 200:
                raise ValidationError("Twitter Account Name should must be of 200 character Max.")

    @api.constrains('twitter_account_link')
    def _check_twitter_account_link(self):
        if self.twitter_account_link != False and self.twitter_account_link != None:
            if len(self.twitter_account_link) > 2200:
                raise ValidationError("Twitter Account Link should must be of 2200 character Max.")

    @api.constrains('blog')
    def _check_blog(self):
        if self.blog != False and self.blog != None:
            if len(self.blog) > 2200:
                raise ValidationError("Blog should must be of 2200 character Max.")
