from odoo import api,fields, models

class PatientTags(models.Model):
    _name = "patient.tags"
    _description = "Patient Tags"
    _rec_name = 'tags'

    tags = fields.Char(string = "Tags")
    color = fields.Integer(string = "Color")
    color_2 = fields.Char(string = "Color 2")
    sequence = fields.Integer(string = "Sequence")


# ********** SQL CONSTRAINTS ************ #
    _sql_constraints = [
        ('unique_tags' , 'unique(tags)' , 'Tag-Name Must be a Unique !'),
        ('check_sequence' , 'check(sequence > 0)' , 'Sequence Must be Non Zero or Nagative Number!')
    ]

# ****************************************************
# Many2One Fields na Data Ne AA rite Access Kari sakay :
#         many2one_field_name.eni_ander_nu_name