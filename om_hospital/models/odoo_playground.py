from odoo import api,fields, models
from odoo.tools.safe_eval import safe_eval

class OdooPlayground(models.Model):
    _name = "odoo.playground"
    _description = "Odoo Playground"

    DEFAULT_ENV_VARIABALES = """# Enter Your Python Code here\n\n"""

    model_id = fields.Many2one('ir.model',string = "Model")
    code = fields.Text(string = "Code" , default = DEFAULT_ENV_VARIABALES)
    result = fields.Text(string = "Result")

    def action_execute(self):
        print("************ SELF ***********",self)
        print("************ SELF.CODE***********",self.code)
        print("************ SELF.ENV ***********",self.env)
        print("************ SELF.ENV.USER ***********",self.env.user)
        print("************ SELF.ENV.USER.LOGIN ***********",self.env.user.login)
        print("************ SELF.ENV.CONTEXT ***********",self.env.context)
        print("************ SELF.ENV.CONTEXT.GET('key-value') ***********",self.env.context.get('params'))
        # appointment_idd=self.env.context.get('params').get('id')       **** AA BAY VASTU SEM J 6 ****
        # appointment_idd=self.env.context['params']['id']           **** AA BAY VASTU SEM J 6 ****
        print("************ SELF.ENV.REF('EXTERNAL_ID')#ke je 'VIEW MATADATA' na 'xml_id' ma hse ***********",self.env.ref('om_hospital.patient_tags_vvip'))
        print("************ SELF.ENV.REF('EXTERNAL_ID')#ke je 'VIEW MATADATA' na 'xml_id' ma hse ***********",self.env.ref('om_hospital.patient_tags_vvip').tags)
        print("************ SELF.ENV['MODEL_NAME'] ***********",self.env['hospital.patient'])
        print("************ SELF.ENV['MODEL_NAME'].browse(id_no) ***********",self.env['hospital.patient'].browse(1).date_of_birth)
        print("************ SELF.ENV['MODEL_NAME'].browse(id_no) ***********",self.env['hospital.patient'].browse(1).name)
        print("************ SELF.ENV['MODEL_NAME'].browse(id_no) ***********",self.env['hospital.appointment'].browse(8).action_cancel())
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else :
                model = self
                self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)



##### ************* Odoo create ORM MEthods ************* #####

# self.env['hospital.patient'].create({'name':'BILALA','email':"jhjhjkhjkhkjh"})   aanathi patien view ma aa data create thai jase ...

# self.env['hospital.patient'].browse(id)   aanathi current_id na data malse ...
# Browse Tyare Vaparvanu ke jyare aapanne ID Khabar Hoy 

# self.env['hospital.patient'].browse(id).get_metadata()   aanathi Aa id na Meta-data malse ...
# self.env['hospital.patient'].browse(id).get_metadata().get('id')

# self.env['hospital.patient'].search([])   Aanathi aa Model ni Badhi j ID show karse  ...
# self.env['hospital.patient'].search([ CONDITIONS ]) 
# self.env['hospital.patient'].search([   ('gender','=','male')   ])
# self.env['hospital.patient'].search([   ('gender','=','male') , (Onther Conditions)  ])   aa "& condtion" ma jase...
# self.env['hospital.patient'].search([  '|' , ('gender','=','male') , (Onther Conditions)  ])   aa "OR condtion" ma jase...
# self.env['hospital.patient'].search([] , limit=1)   Aanathi Ek j ID Shiw karse !!!
# Search Tyare Vaparvanu ke jyare aapanne ID Khabar na Hoy 

# self.env['hospital.patient'].search_count([])   Aanathi jetli ID hase , Eni Total Show karse !!!
# self.env['hospital.patient'].search_count([ Condition ])   

# self.env['hospital.patient'].browse(current_id).write({'field_nu_name':'je_change_karvu_hoy_te'})   aanathi je field ma change karvo hoy te thai jase ...

# self.env['hospital.patient'].browse(current_id).unlink()   aanathi id no data delet karvo hoy te data delet thhai jase ...

# self.env['hospital.patient'].fields_get()   Aanathi Aa Model ni Badhi j Fields Show Karse !!!
# self.env['hospital.patient'].fields_get( [ 'Je_fielld_joti_hoy_te' ,'Je_fielld_joti_hoy_te' ] )   Aanathi Aa Model ni Aa fileds(Selected) j Fields Show Karse !!!
# self.env['hospital.patient'].fields_get( [ 'Je_fielld_joti_hoy_te' ,'Je_fielld_joti_hoy_te' ] , ['type' , 'string'] )   