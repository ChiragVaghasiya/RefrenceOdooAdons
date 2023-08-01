from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AdvanceSearchOptions(models.Model):
    _name = 'advance.search.options'
    _description = 'Advance Search Options'
    _rec_name = 'name'

    name = fields.Char("Name")
    color = fields.Integer("")


class DocumentTypes(models.Model):
    _name = 'document.types'
    _description = 'Document Types'
    _rec_name = 'name'

    name = fields.Char("Name")


class AdvanceSearch(models.TransientModel):
    _name = 'advance.search'
    _description = 'Advance Search'

    like_opts = [('is_like', 'Like'), ('not_like', 'Not Like'), ('set', 'Set'), ('not_set', 'Not Set')]
    contain_opts = [('contains', 'Contains'), ('not_contains', 'Not Contains'), ('set', 'Set'), ('not_set', 'Not Set')]
    date_opts = [('gt', '>'), ('lt', '<'), ('eq', '='), ('btw', 'Between'), ('set', 'Set'), ('not_set', 'Not Set')]

    fields_selection = fields.Many2many('advance.search.options', string="Select Fields")
    or_operation = fields.Boolean("Or Operation")
    document_type = fields.Many2many('document.types', string="Document Type")

    all_doc = fields.Boolean("All", default=True)
    lekh = fields.Boolean("Lekh")
    nirnaami_lekh = fields.Boolean("Nirnaami Lekh")
    book = fields.Boolean("Book")
    video = fields.Boolean("Video")

    sr_no_options = fields.Selection(like_opts, "", default='is_like')
    subject_options = fields.Selection(contain_opts, "", default='contains')
    tags_options = fields.Selection(contain_opts, "", default='contains')
    tharav_options = fields.Selection(contain_opts, "", default='contains')
    description_options = fields.Selection(contain_opts, "", default='contains')
    person_options = fields.Selection(contain_opts, "", default='contains')
    sanstha_options = fields.Selection(contain_opts, "", default='contains')
    mahatma_options = fields.Selection(contain_opts, "", default='contains')
    samuday_options = fields.Selection(contain_opts, "", default='contains')
    vikram_samvat_options = fields.Selection(like_opts, "", default='is_like')
    publishing_date_options = fields.Selection(date_opts, "Should Be")
    occurence_date_options = fields.Selection(date_opts, "Should Be")
    category_options = fields.Selection(like_opts, "", default='is_like')
    link_with_field_options = fields.Selection(contain_opts, "Contains", default='contains')
    remark_options = fields.Selection(contain_opts, "", default='contains')
    star_rating_options = fields.Selection(like_opts, "", default='is_like')
    samiti_options = fields.Selection(contain_opts, "", default='contains')

    need_sr_no = fields.Boolean("Sr. No.")
    need_subject = fields.Boolean("Subject")
    need_tags = fields.Boolean("Tag")
    need_tharav = fields.Boolean("Tharav")
    need_description = fields.Boolean("Description")
    need_person = fields.Boolean("Person")
    need_sanstha = fields.Boolean("Sanstha")
    need_mahatma = fields.Boolean("Mahatma")
    need_samuday = fields.Boolean("Samuday")
    need_vikram_samvat = fields.Boolean("Vikram Samvat of Publishing")
    need_publishing_date = fields.Boolean("Date Of Publishing")
    need_occurence_date = fields.Boolean("Date Of Occurrence")
    need_category = fields.Boolean("Category")
    need_link_with_field = fields.Boolean("Link With Field")
    need_remark = fields.Boolean("Remark")
    need_star_rating = fields.Boolean("Star Rating For Importance Of Utility")
    need_samiti = fields.Boolean("Samiti")

    advance_search = fields.Boolean("Advanced Conditional Search")

    sr_no = fields.Char("Sr. No.")
    subject = fields.Char("Subject")
    tags_id = fields.Many2many('lekh.tags.model', string="Tags")
    tharav_id = fields.Many2many('tharav.model', string="Tharav")
    description = fields.Char("Description")
    person = fields.Many2many('person.model', string="Person")
    sanstha = fields.Many2many('sanstha.model', string="Sanstha")
    mahatma = fields.Many2many('mahatma.model', string="Mahatma")
    samuday = fields.Many2many('samuday.model', string="Samuday")
    vikram_samvat = fields.Char("Vikram Samvat of Publishing")
    category = fields.Selection([('original', 'Original Documents'), ('photo_copy', 'Photo Copy Or Xeroxx'),
                                 ('partial', 'Partial Documents (With No Reference)')
                                    , ('high', 'High'), ('low', 'Low')], "Category")
    link_with_field = fields.Many2many('documents.model', string="Link With Field")
    remark = fields.Char("Remark")
    star_rating = fields.Selection([('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')],
                                   "Star Ratings for Importance Of Utility")
    samiti = fields.Many2many('samiti.model', string="Samiti")
    occurance_date = fields.Date("Occurance Date")
    occurance_start_date = fields.Date("Start Date")
    occurance_end_date = fields.Date("End Date")
    publishing_date = fields.Date("Publishing Date")
    publishing_start_date = fields.Date("Start Date")
    publishing_end_date = fields.Date("End Date")
    global_search = fields.Char("Global Search")
    # global_search2 = fields.Char("Global Search")
    # global_search_and = fields.Boolean("Global Search And")

    tags_bool = fields.Boolean("AND")
    tharav_bool = fields.Boolean("AND")
    person_bool = fields.Boolean("AND")
    sanstha_bool = fields.Boolean("AND")
    mahatma_bool = fields.Boolean("AND")
    samuday_bool = fields.Boolean("AND")
    link_with_bool = fields.Boolean("AND")
    samiti_bool = fields.Boolean("AND")

    def search_globally(self):

        elements = [None, False]
        if self.all_doc == False and self.lekh == False and self.nirnaami_lekh == False and self.book == False and self.video == False:
            raise ValidationError("Please Select document Type First")

        lst = [False, None, "", " ", ""]
        if self.global_search in lst or not len(self.global_search) > 0:
            raise ValidationError("Please Enter Something to search for...")

        doc_typ = []
        if self.all_doc:
            doc_typ = ['lekh', 'nirnaami_lekh', 'book', 'video']
        else:

            if self.lekh:
                doc_typ.append('lekh')
            if self.nirnaami_lekh:
                doc_typ.append('nirnaami_lekh')
            if self.book:
                doc_typ.append('book')
            if self.video:
                doc_typ.append('video')

        docs_ids = []

        DocSearch0 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('subject', 'ilike', self.global_search)])
        if DocSearch0 not in elements and len(DocSearch0) > 0:
            for doc in DocSearch0:
                docs_ids.append(doc.id)

        DocSearch1 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('sr_no_prefix', 'ilike', self.global_search)])
        if DocSearch1 not in elements and len(DocSearch1) > 0:
            for doc in DocSearch1:
                docs_ids.append(doc.id)

        DocSearch2 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('tags_id.lekh_tag_name', '=', self.global_search)])
        if DocSearch2 not in elements and len(DocSearch2) > 0:
            for doc in DocSearch2:
                docs_ids.append(doc.id)

        DocSearch3 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('tharav_id.tharav_id', 'ilike', self.global_search)])
        if DocSearch3 not in elements and len(DocSearch3) > 0:
            for doc in DocSearch3:
                docs_ids.append(doc.id)

        DocSearch4 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('description', 'ilike', self.global_search)])
        if DocSearch4 not in elements and len(DocSearch4) > 0:
            for doc in DocSearch4:
                docs_ids.append(doc.id)

        DocSearch5 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.vikram_samvat', '=', self.global_search)])
        if DocSearch5 not in elements and len(DocSearch5) > 0:
            for doc in DocSearch5:
                docs_ids.append(doc.id)

        DocSearch6 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_publishing', 'ilike', self.global_search)])
        if DocSearch6 not in elements and len(DocSearch6) > 0:
            for doc in DocSearch6:
                docs_ids.append(doc.id)

        DocSearch7 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_occurance', 'ilike', self.global_search)])
        if DocSearch7 not in elements and len(DocSearch7) > 0:
            for doc in DocSearch7:
                docs_ids.append(doc.id)

        DocSearch8 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.category', '=', self.global_search)])
        if DocSearch8 not in elements and len(DocSearch8) > 0:
            for doc in DocSearch8:
                docs_ids.append(doc.id)

        DocSearch9 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('remark', 'ilike', self.global_search)])
        if DocSearch9 not in elements and len(DocSearch9) > 0:
            for doc in DocSearch9:
                docs_ids.append(doc.id)

        DocSearch10 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('star_rating', '=', self.global_search)])
        if DocSearch10 not in elements and len(DocSearch10) > 0:
            for doc in DocSearch10:
                docs_ids.append(doc.id)

        DocSearch11 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.person_id.person_name', '=', self.global_search)])
        if DocSearch11 not in elements and len(DocSearch11) > 0:
            for doc in DocSearch11:
                docs_ids.append(doc.id)

        DocSearch12 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.sanstha_id.sanstha_name', '=', self.global_search)])
        if DocSearch12 not in elements and len(DocSearch12) > 0:
            for doc in DocSearch12:
                docs_ids.append(doc.id)

        DocSearch13 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
            'doc_related_info_lines.mahatma_id.mahatma_name', 'ilike', self.global_search)])
        DocSearch133 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
            'doc_related_info_lines.samiti_id.samiti_mahatma_id.mahatma_id.mahatma_name', 'ilike', self.global_search)])

        if DocSearch13 not in elements and len(DocSearch13) > 0:
            for doc in DocSearch13:
                docs_ids.append(doc.id)

        if DocSearch133 not in elements and len(DocSearch133) > 0:
            for doc in DocSearch133:
                docs_ids.append(doc.id)

        DocSearch14 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samuday_id.samuday_name', '=', self.global_search)])
        if DocSearch14 not in elements and len(DocSearch14) > 0:
            for doc in DocSearch14:
                docs_ids.append(doc.id)

        DocSearch15 = self.env['documents.model'].search(
            [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samiti_id.name', '=', self.global_search)])
        if DocSearch15 not in elements and len(DocSearch15) > 0:
            for doc in DocSearch15:
                docs_ids.append(doc.id)

        if len(docs_ids) > 0:

            message_id = self.env['advance.search.result'].create({'document_ids': docs_ids})
            return {
                'name': _('Advance Documents Global Search Results'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'advance.search.result',
                'res_id': message_id.id,
                'target': 'new'
            }

        else:

            message_id = self.env['message.wizard'].create({'message': _("There're no Document found!...")})
            return {
                'name': _('Advance Documents Global Search Results!'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

        # raise ValidationError("Under Developement")

    @api.onchange('fields_selection')
    def _get_fields_selection(self):

        if self.fields_selection:

            if len(self.fields_selection) > 0:
                display_fields = []

                for rec in self.fields_selection:
                    display_fields.append(rec.name)

                if "Sr. No." in display_fields:
                    self.need_sr_no = True
                else:
                    self.need_sr_no = False
                    self.sr_no = False

                if "Subject" in display_fields:
                    self.need_subject = True
                else:
                    self.need_subject = False
                    self.subject = False

                if "Tags" in display_fields:
                    self.need_tags = True
                else:
                    self.need_tags = False
                    self.tags_id = False

                if "Tharav" in display_fields:
                    self.need_tharav = True
                else:
                    self.need_tharav = False
                    self.tharav_id = False

                if "Description" in display_fields:
                    self.need_description = True
                else:
                    self.need_description = False
                    self.description = False

                if "Vikram Samvat of Publishing" in display_fields:
                    self.need_vikram_samvat = True
                else:
                    self.need_vikram_samvat = False
                    self.vikram_samvat = False

                if "Date Of Publishing" in display_fields:
                    self.need_publishing_date = True
                else:
                    self.need_publishing_date = False
                    self.publishing_start_date = False
                    self.publishing_end_date = False

                if "Date Of Occurrence" in display_fields:
                    self.need_occurence_date = True
                else:
                    self.need_occurence_date = False
                    self.occurance_start_date = False
                    self.occurance_end_date = False

                if "Category" in display_fields:
                    self.need_category = True
                else:
                    self.need_category = False
                    self.category = False

                if "Remark" in display_fields:
                    self.need_remark = True
                else:
                    self.need_remark = False
                    self.remark = False

                if "Star Rating For Importance Of Utility" in display_fields:
                    self.need_star_rating = True
                else:
                    self.need_star_rating = False
                    self.star_rating = False

                if "Person" in display_fields:
                    self.need_person = True
                else:
                    self.need_person = False
                    self.person = False

                if "Sanstha" in display_fields:
                    self.need_sanstha = True
                else:
                    self.need_sanstha = False
                    self.sanstha = False

                if "Mahatma" in display_fields:
                    self.need_mahatma = True
                else:
                    self.need_mahatma = False
                    self.mahatma = False

                if "Samuday" in display_fields:
                    self.need_samuday = True
                else:
                    self.need_samuday = False
                    self.samuday = False

                if "Samiti" in display_fields:
                    self.need_samiti = True
                else:
                    self.need_samiti = False
                    self.samiti = False

                if "Link With Field" in display_fields:
                    self.need_link_with_field = True
                else:
                    self.need_link_with_field = False
                    self.link_with_field = False

            else:
                self.reset_all_elements(self)

        else:
            self.reset_all_elements(self)

    @api.onchange('advance_search')
    def _clear_all_global_search(self):
        if self.advance_search:
            self.global_search = False
            # self.global_search2 = False
            # self.global_search_and = False
        else:
            self.or_operation = False
            self.fields_selection = False

    # @api.onchange('global_search_and')
    # def _clear_global_search2(self):
    #     if not self.global_search_and:
    #         self.global_search2 = False

    def search_documents(self):

        elements = [None, False]
        if self.all_doc == False and self.lekh == False and self.nirnaami_lekh == False and self.book == False and self.video == False:
            raise ValidationError("Please Select document Type First")

        if self.fields_selection not in elements and len(self.fields_selection) > 0:
            fields_list = []
            for field in self.fields_selection:
                fields_list.append(field.name)
        else:
            raise ValidationError("Please select fields you wish to search in ...")

        doc_typ = []
        if self.all_doc:
            doc_typ = ['lekh', 'nirnaami_lekh', 'book', 'video']
        else:

            if self.lekh:
                doc_typ.append('lekh')
            if self.nirnaami_lekh:
                doc_typ.append('nirnaami_lekh')
            if self.book:
                doc_typ.append('book')
            if self.video:
                doc_typ.append('video')

        docs_ids = []
        if self.or_operation:
            domain = [('doc_type', 'in', doc_typ)]
            lmd_fun = lambda x: [doc.id for doc in x]

            if 'Sr. No.' in fields_list:

                DocSearch1 = []
                if self.sr_no_options == 'is_like':
                    DocSearch1 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('sr_no_prefix', 'ilike', self.sr_no)])
                elif self.sr_no_options == 'not_like':
                    DocSearch1 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('sr_no_prefix', 'not like', self.sr_no)])
                elif self.sr_no_options == 'set':
                    DocSearch1 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('sr_no_prefix', '!=', False)])
                elif self.sr_no_options == 'not_set':
                    DocSearch1 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('sr_no_prefix', '=', False)])

                if DocSearch1 not in elements and len(DocSearch1) > 0:
                    for doc in DocSearch1:
                        docs_ids.append(doc.id)

            if 'Subject' in fields_list:

                DocSearch01 = []
                if self.subject_options == 'contains':
                    DocSearch01 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('subject', 'ilike', self.subject)])
                elif self.subject_options == 'not_contains':
                    DocSearch01 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('subject', 'not like', self.subject)])
                elif self.subject_options == 'set':
                    DocSearch01 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('subject', '=', False)])
                elif self.subject_options == 'not_set':
                    DocSearch01 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('subject', '!=', False)])

                if DocSearch01 not in elements and len(DocSearch01) > 0:
                    for doc in DocSearch01:
                        docs_ids.append(doc.id)

            if 'Tags' in fields_list:
                ids_of_tag = []
                if len(self.tags_id) > 0:
                    for tag in self.tags_id:
                        ids_of_tag.append(tag.id)

                DocSearch2 = []
                if self.tags_options == 'contains':
                    DocSearch2 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tags_id.id', 'in', ids_of_tag)])
                    if self.tags_bool:
                        for tag in self.tags_id:
                            domain.append(('tags_id.id', '=', tag.id))
                        DocSearch2 = self.env['documents.model'].search(domain)

                elif self.tags_options == 'not_contains':
                    DocSearch2 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tags_id.id', 'not in', ids_of_tag)])
                    if self.tags_bool:

                        list_of_doc_ids = lmd_fun(DocSearch2)

                        if DocSearch2:
                            m = 0
                            for doc in DocSearch2:
                                if doc.tags_id not in elements and len(doc.tags_id) > 0:
                                    for tag in doc.tags_id:
                                        a = tag.id
                                        if a in ids_of_tag:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch2 = self.env['documents.model'].browse(list_of_doc_ids)

                elif self.tags_options == 'set':
                    DocSearch2 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tags_id', '!=', False)])
                elif self.tags_options == 'not_set':
                    DocSearch2 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tags_id', '=', False)])

                if DocSearch2 not in elements and len(DocSearch2) > 0:
                    for doc in DocSearch2:
                        docs_ids.append(doc.id)

            if 'Tharav' in fields_list:
                ids_of_tharav = []
                if len(self.tharav_id) > 0:
                    for record in self.tharav_id:
                        ids_of_tharav.append(record.id)

                DocSearch3 = []
                if self.tharav_options == 'contains':
                    DocSearch3 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tharav_id.id', 'in', ids_of_tharav)])
                    if self.tharav_bool:
                        for tharav in self.tharav_id:
                            domain.append(('tharav_id.id', '=', tharav.id))
                        DocSearch3 = self.env['documents.model'].search(domain)
                elif self.tharav_options == 'not_contains':
                    DocSearch3 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tharav_id.id', 'not in', ids_of_tharav)])
                    if self.tharav_bool:

                        list_of_doc_ids = lmd_fun(DocSearch3)

                        if DocSearch3:
                            m = 0
                            for doc in DocSearch3:
                                if doc.tharav_id not in elements and len(doc.tharav_id) > 0:
                                    for tharav in doc.tharav_id:
                                        a = tharav.id
                                        if a in ids_of_tharav:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch3 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.tharav_options == 'set':
                    DocSearch3 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tharav_id', '!=', False)])
                elif self.tharav_options == 'not_set':
                    DocSearch3 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('tharav_id', '=', False)])

                if DocSearch3 not in elements and len(DocSearch3) > 0:
                    for doc in DocSearch3:
                        docs_ids.append(doc.id)

            if 'Description' in fields_list:

                DocSearch4 = []
                if self.description_options == 'contains':
                    DocSearch4 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('description', 'ilike', self.description)])
                elif self.description_options == 'not_contains':
                    DocSearch4 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('description', 'not like', self.description)])
                elif self.description_options == 'set':
                    DocSearch4 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('description', '!=', False)])
                elif self.description_options == 'not_set':
                    DocSearch4 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('description', '=', False)])

                if DocSearch4 not in elements and len(DocSearch4) > 0:
                    for doc in DocSearch4:
                        docs_ids.append(doc.id)

            if 'Vikram Samvat of Publishing' in fields_list:

                DocSearch5 = []
                if self.vikram_samvat_options == 'is_like':
                    DocSearch5 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.vikram_samvat', '=', self.vikram_samvat)])
                elif self.vikram_samvat_options == 'not_like':
                    DocSearch5 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.vikram_samvat', '!=', self.vikram_samvat)])
                elif self.vikram_samvat_options == 'set':
                    DocSearch5 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.vikram_samvat', '!=', False)])
                elif self.vikram_samvat_options == 'not_set':
                    DocSearch5 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.vikram_samvat', '=', False)])

                if DocSearch5 not in elements and len(DocSearch5) > 0:
                    for doc in DocSearch5:
                        docs_ids.append(doc.id)

            if 'Date Of Publishing' in fields_list:

                DocSearch6 = []
                if self.publishing_date_options == 'gt':
                    DocSearch6 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_publishing', '>=', self.publishing_date)])
                elif self.publishing_date_options == 'lt':
                    DocSearch6 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_publishing', '<=', self.publishing_date)])
                elif self.publishing_date_options == 'eq':
                    DocSearch6 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_publishing', '=', self.publishing_date)])
                elif self.publishing_date_options == 'btwn':
                    DocSearch6 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_publishing', '>=', self.publishing_start_date), (
                                                                         'doc_related_info_lines.date_of_publishing',
                                                                         '<=',
                                                                         self.publishing_end_date)])
                elif self.publishing_date_options == 'set':
                    DocSearch6 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_publishing', '!=', False)])
                elif self.publishing_date_options == 'not_set':
                    DocSearch6 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_publishing', '=', False)])

                if DocSearch6 not in elements and len(DocSearch6) > 0:
                    for doc in DocSearch6:
                        docs_ids.append(doc.id)

            if 'Date Of Occurrence' in fields_list:

                DocSearch7 = []
                if self.occurence_date_options == 'gt':
                    DocSearch7 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_occurance', '>=', self.occurance_date)])
                elif self.occurence_date_options == 'lt':
                    DocSearch7 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_occurance', '<=', self.occurance_date)])
                elif self.occurence_date_options == 'eq':
                    DocSearch7 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_occurance', '=', self.occurance_date)])
                elif self.occurence_date_options == 'btwn':
                    DocSearch7 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.date_of_occurance', '>=', self.occurance_start_date), (
                                                                         'doc_related_info_lines.date_of_publishing',
                                                                         '<=',
                                                                         self.occurance_end_date)])
                elif self.occurence_date_options == 'set':
                    DocSearch7 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_occurance', '!=', False)])
                elif self.occurence_date_options == 'not_set':
                    DocSearch7 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.date_of_occurance', '=', False)])

                if DocSearch7 not in elements and len(DocSearch7) > 0:
                    for doc in DocSearch7:
                        docs_ids.append(doc.id)

            if 'Category' in fields_list:

                DocSearch8 = []
                if self.category_options == 'is_like':
                    DocSearch8 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.category', '=', self.category)])
                elif self.category_options == 'not_like':
                    DocSearch8 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.category', '!=', self.category)])
                elif self.category_options == 'set':
                    DocSearch8 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.category', '!=', False)])
                elif self.category_options == 'not_set':
                    DocSearch8 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.category', '=', False)])

                if DocSearch8 not in elements and len(DocSearch8) > 0:
                    for doc in DocSearch8:
                        docs_ids.append(doc.id)

            if 'Remark' in fields_list:

                DocSearch9 = []
                if self.remark_options == 'is_like':
                    DocSearch9 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('remark', 'ilike', self.remark)])
                elif self.remark_options == 'not_like':
                    DocSearch9 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('remark', 'not like', self.remark)])
                elif self.remark_options == 'set':
                    DocSearch9 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('remark', '!=', False)])
                elif self.remark_options == 'not_set':
                    DocSearch9 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('remark', '=', False)])

                if DocSearch9 not in elements and len(DocSearch9) > 0:
                    for doc in DocSearch9:
                        docs_ids.append(doc.id)

            if 'Star Rating For Importance Of Utility' in fields_list:

                DocSearch10 = []
                if self.star_rating_options == 'is_like':
                    DocSearch10 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('star_rating', '=', self.star_rating)])
                elif self.star_rating_options == 'not_like':
                    DocSearch10 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('star_rating', '!=', self.star_rating)])
                elif self.star_rating_options == 'set':
                    DocSearch10 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('star_rating', '!=', False)])
                elif self.star_rating_options == 'not_set':
                    DocSearch10 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('star_rating', '=', False)])

                DocSearch10 = self.env['documents.model'].search(
                    [('doc_type', 'in', doc_typ), ('star_rating', a, self.star_rating)])

                if DocSearch10 not in elements and len(DocSearch10) > 0:
                    for doc in DocSearch10:
                        docs_ids.append(doc.id)

            if 'Person' in fields_list:
                ids_of_person = []
                if len(self.person) > 0:
                    for record in self.person:
                        ids_of_person.append(record.id)

                DocSearch11 = []
                if self.person_options == 'contains':
                    DocSearch11 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.person_id.id', 'in', ids_of_person)])
                    if self.person_bool:
                        for person in self.person_id:
                            domain.append(('doc_related_info_lines.person_id.id', '=', person.id))
                        DocSearch11 = self.env['documents.model'].search(domain)
                elif self.person_options == 'not_contains':
                    DocSearch11 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.person_id', 'not in', ids_of_person)])
                    if self.person_bool:

                        list_of_doc_ids = lmd_fun(DocSearch11)

                        if DocSearch11:
                            m = 0
                            for doc in DocSearch11:
                                if doc.doc_related_info_lines.person_id not in elements and len(
                                        doc.doc_related_info_lines.person_id) > 0:
                                    for person in doc.doc_related_info_lines.person_id:
                                        a = person.id
                                        if a in ids_of_person:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch11 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.person_options == 'set':
                    DocSearch11 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.person_id', '!=', False)])
                elif self.person_options == 'not_set':
                    DocSearch11 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.person_id', '=', False)])

                if DocSearch11 not in elements and len(DocSearch11) > 0:
                    for doc in DocSearch11:
                        docs_ids.append(doc.id)

            if 'Sanstha' in fields_list:
                ids_of_sanstha = []
                if len(self.sanstha) > 0:
                    for record in self.sanstha:
                        ids_of_sanstha.append(record.id)

                DocSearch12 = []
                if self.sanstha_options == 'contains':
                    DocSearch12 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.sanstha_id.id', 'in', ids_of_sanstha)])
                    if self.sanstha_bool:
                        for sanstha in self.sanstha_id:
                            domain.append(('doc_related_info_lines.sanstha_id.id', '=', sanstha.id))
                        DocSearch12 = self.env['documents.model'].search(domain)
                elif self.sanstha_options == 'not_contains':
                    DocSearch12 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.sanstha_id', 'not in', ids_of_sanstha)])
                    if self.sanstha_bool:

                        list_of_doc_ids = lmd_fun(DocSearch12)

                        if DocSearch12:
                            m = 0
                            for doc in DocSearch12:
                                if doc.doc_related_info_lines.sanstha_id not in elements and len(
                                        doc.doc_related_info_lines.sanstha_id) > 0:
                                    for sanstha in doc.doc_related_info_lines.sanstha_id:
                                        a = sanstha.id
                                        if a in ids_of_sanstha:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch12 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.sanstha_options == 'set':
                    DocSearch12 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.sanstha_id', '!=', False)])
                elif self.sanstha_options == 'not_set':
                    DocSearch12 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.sanstha_id', '=', False)])

                if DocSearch12 not in elements and len(DocSearch12) > 0:
                    for doc in DocSearch12:
                        docs_ids.append(doc.id)

            if 'Samuday' in fields_list:
                ids_of_samuday = []
                if len(self.samuday) > 0:
                    for record in self.samuday:
                        ids_of_samuday.append(record.id)

                DocSearch14 = []
                if self.samuday_options == 'contains':
                    DocSearch14 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samuday_id.id', 'in', ids_of_samuday)])
                    if self.samuday_bool:
                        for samuday in self.samuday_id:
                            domain.append(('doc_related_info_lines.samuday_id.id', '=', samuday.id))
                        DocSearch14 = self.env['documents.model'].search(domain)
                elif self.samuday_options == 'not_contains':
                    DocSearch14 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samuday_id', 'not in', ids_of_samuday)])
                    if self.samuday_bool:

                        list_of_doc_ids = lmd_fun(DocSearch14)

                        if DocSearch14:
                            m = 0
                            for doc in DocSearch14:
                                if doc.doc_related_info_lines.samuday_id not in elements and len(
                                        doc.doc_related_info_lines.samuday_id) > 0:
                                    for samuday in doc.doc_related_info_lines.samuday_id:
                                        a = samuday.id
                                        if a in ids_of_samuday:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch14 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.samuday_options == 'set':
                    DocSearch14 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samuday_id', '!=', False)])
                elif self.samuday_options == 'not_set':
                    DocSearch14 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samuday_id', '=', False)])

                if DocSearch14 not in elements and len(DocSearch14) > 0:
                    for doc in DocSearch14:
                        docs_ids.append(doc.id)

            if 'Samiti' in fields_list:
                ids_of_samiti = []
                if len(self.samiti) > 0:
                    for record in self.samiti:
                        ids_of_samiti.append(record.id)

                DocSearch15 = []
                if self.samiti_options == 'contains':
                    DocSearch15 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samiti_id.id', 'in', ids_of_samiti)])
                    if self.samiti_bool:
                        for samiti in self.samiti_id:
                            domain.append(('doc_related_info_lines.samiti_id.id', '=', samiti.id))
                        DocSearch15 = self.env['documents.model'].search(domain)
                elif self.samiti_options == 'not_contains':
                    DocSearch15 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samiti_id', 'not in', ids_of_samiti)])
                    if self.samiti_bool:

                        list_of_doc_ids = lmd_fun(DocSearch15)

                        if DocSearch15:
                            m = 0
                            for doc in DocSearch15:
                                if doc.doc_related_info_lines.samiti_id not in elements and len(
                                        doc.doc_related_info_lines.samiti_id) > 0:
                                    for samiti in doc.doc_related_info_lines.samiti_id:
                                        a = samiti.id
                                        if a in ids_of_samiti:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch15 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.samiti_options == 'set':
                    DocSearch15 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samiti_id', '!=', False)])
                elif self.samiti_options == 'not_set':
                    DocSearch15 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.samiti_id', '=', False)])

                # DocSearch15 = self.env['documents.model'].search([('doc_type','in',doc_typ), ('doc_related_info_lines.samiti_id.id',a,ids_of_samiti)])

                if DocSearch15 not in elements and len(DocSearch15) > 0:
                    for doc in DocSearch15:
                        docs_ids.append(doc.id)

            if 'Mahatma' in fields_list:
                ids_of_mahatma = []
                if len(self.mahatma) > 0:
                    for record in self.mahatma:
                        ids_of_mahatma.append(record.id)

                DocSearch13 = []
                DocSearch133 = []
                if self.mahatma_options == 'contains':
                    DocSearch13 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.mahatma_id.id', 'in', ids_of_mahatma)])
                    if self.mahatma_bool:
                        for mahatma in self.mahatma_id:
                            domain.append(('doc_related_info_lines.mahatma_id.id', '=', mahatma.id))
                        DocSearch13 = self.env['documents.model'].search(domain)
                    DocSearch133 = self.env['documents.model'].search([('doc_type', 'in', doc_typ), (
                        'doc_related_info_lines.samiti_id.samiti_mahatma_id.mahatma_id.id', 'in', ids_of_mahatma)])
                    if self.mahatma_bool:
                        for mahatma in self.mahatma_id:
                            domain.append(
                                ('doc_related_info_lines.samiti_id.samiti_mahatma_id.mahatma_id.id', '=', mahatma.id))
                        DocSearch133 = self.env['documents.model'].search(domain)
                elif self.mahatma_options == 'not_contains':
                    DocSearch13 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.mahatma_id', 'not in', ids_of_mahatma)])
                    if self.mahatma_bool:

                        list_of_doc_ids = lmd_fun(DocSearch13)

                        if DocSearch13:
                            m = 0
                            for doc in DocSearch13:
                                if doc.doc_related_info_lines.mahatma_id not in elements and len(
                                        doc.doc_related_info_lines.mahatma_id) > 0:
                                    for mahatma in doc.doc_related_info_lines.mahatma_id:
                                        a = mahatma.id
                                        if a in ids_of_mahatma:
                                            m += 1
                                            list_of_doc_ids.remove(doc.id)
                            if m > 0:
                                DocSearch13 = self.env['documents.model'].browse(list_of_doc_ids)
                elif self.mahatma_options == 'set':
                    DocSearch13 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.mahatma_id', '!=', False)])
                elif self.mahatma_options == 'not_set':
                    DocSearch13 = self.env['documents.model'].search(
                        [('doc_type', 'in', doc_typ), ('doc_related_info_lines.mahatma_id', '=', False)])

                if DocSearch13 not in elements and len(DocSearch13) > 0:
                    for doc in DocSearch13:
                        docs_ids.append(doc.id)

                if DocSearch133 not in elements and len(DocSearch133) > 0:
                    for doc in DocSearch133:
                        docs_ids.append(doc.id)

            if 'Link With Field' in fields_list:

                list_of_recs = self.get_link_with_field_records(self, self.link_with_field_options, self.link_with_bool,
                                                                doc_types=('doc_type', 'in', doc_typ))

                if list_of_recs not in elements and len(list_of_recs) > 0:
                    for rec in list_of_recs:
                        docs_ids.append(rec)

            if len(docs_ids) > 0:

                message_id = self.env['advance.search.result'].create({'document_ids': docs_ids})
                return {
                    'name': _('Advance Documents Search Results'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'advance.search.result',
                    'res_id': message_id.id,
                    'target': 'new'
                }

            else:

                message_id = self.env['message.wizard'].create({'message': _("There're no Document found!...")})
                return {
                    'name': _('Advance Documents Search Results!'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    'res_id': message_id.id,
                    'target': 'new'
                }

        else:
            search_domain = [('doc_type', 'in', doc_typ)]

            if 'Sr. No.' in fields_list:

                if self.sr_no_options == 'is_like':
                    search_domain.append(('sr_no_prefix', 'ilike', self.sr_no))
                elif self.sr_no_options == 'not_like':
                    search_domain.append(('sr_no_prefix', 'not like', self.sr_no))
                elif self.sr_no_options == 'set':
                    search_domain.append(('sr_no_prefix', '!=', False))
                elif self.sr_no_options == 'not_set':
                    search_domain.append(('sr_no_prefix', '=', False))

            if 'Subject' in fields_list:

                if self.subject_options == 'contains':
                    search_domain.append(('subject', 'ilike', self.subject))
                elif self.subject_options == 'not_contains':
                    search_domain.append(('subject', 'not like', self.subject))
                elif self.subject_options == 'set':
                    search_domain.append(('subject', '!=', False))
                elif self.subject_options == 'not_set':
                    search_domain.append(('subject', '=', False))

            if 'Tags' in fields_list:

                ids_of_tag = []
                if len(self.tags_id) > 0:
                    for tag in self.tags_id:
                        ids_of_tag.append(tag.id)

                if self.tags_options == 'contains':
                    if self.tags_bool:
                        if len(ids_of_tag) > 0:
                            for tag_id in ids_of_tag:
                                search_domain.append(('tags_id.id', '=', tag_id))
                    else:
                        search_domain.append(('tags_id.id', 'in', ids_of_tag))

                elif self.tags_options == 'not_contains':
                    search_domain.append(('tags_id', 'not in', ids_of_tag))
                elif self.tags_options == 'set':
                    search_domain.append(('tags_id', '!=', False))
                elif self.tags_options == 'not_set':
                    search_domain.append(('tags_id', '=', False))

            if 'Tharav' in fields_list:

                ids_of_tharav = []
                if len(self.tharav_id) > 0:
                    for record in self.tharav_id:
                        ids_of_tharav.append(record.id)

                if self.tharav_options == 'contains':
                    if self.tharav_bool:
                        if len(ids_of_tharav) > 0:
                            for tharav_id in ids_of_tharav:
                                search_domain.append(('tharav_id.id', '=', tharav_id))
                    else:
                        search_domain.append(('tharav_id.id', 'in', ids_of_tharav))

                elif self.tharav_options == 'not_contains':
                    search_domain.append(('tharav_id', 'not in', ids_of_tharav))
                elif self.tharav_options == 'set':
                    search_domain.append(('tharav_id', '!=', False))
                elif self.tharav_options == 'not_set':
                    search_domain.append(('tharav_id', '=', False))

            if 'Description' in fields_list:

                if self.description_options == 'contains':
                    search_domain.append(('description', 'ilike', self.description))
                elif self.description_options == 'not_contains':
                    search_domain.append(('description', 'not like', self.description))
                elif self.description_options == 'set':
                    search_domain.append(('description', '!=', False))
                elif self.description_options == 'not_set':
                    search_domain.append(('description', '=', False))

            if 'Vikram Samvat of Publishing' in fields_list:

                if self.vikram_samvat_options == 'contains':
                    search_domain.append(('doc_related_info_lines.vikram_samvat', '=', self.vikram_samvat))
                elif self.vikram_samvat_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.vikram_samvat', '!=', self.vikram_samvat))
                elif self.vikram_samvat_options == 'set':
                    search_domain.append(('doc_related_info_lines.vikram_samvat', '!=', False))
                elif self.vikram_samvat_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.vikram_samvat', '=', False))

            if 'Date Of Publishing' in fields_list:

                if self.publishing_date_options == 'gt':
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '>=', self.publishing_date))
                elif self.publishing_date_options == 'lt':
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '<=', self.publishing_date))
                elif self.publishing_date_options == 'eq':
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '=', self.publishing_date))
                elif self.publishing_date_options == 'btwn':
                    search_domain.append(
                        ('doc_related_info_lines.date_of_publishing', '>=', self.publishing_start_date))
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '<=', self.publishing_end_date))
                elif self.publishing_date_options == 'set':
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '!=', False))
                elif self.publishing_date_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.date_of_publishing', '=', False))

            if 'Date Of Occurrence' in fields_list:

                if self.occurance_date_options == 'gt':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '>=', self.occurance_date))
                elif self.occurance_date_options == 'lt':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '<=', self.occurance_date))
                elif self.occurance_date_options == 'eq':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '=', self.occurance_date))
                elif self.occurance_date_options == 'btwn':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '>=', self.occurance_start_date))
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '>=', self.occurance_end_date))
                elif self.occurance_date_options == 'set':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '!=', False))
                elif self.occurance_date_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.date_of_occurance', '=', False))

            if 'Category' in fields_list:

                if self.category_options == 'is_like':
                    search_domain.append(('doc_related_info_lines.category', '=', self.category))
                elif self.category_options == 'not_like':
                    search_domain.append(('doc_related_info_lines.category', '!=', self.category))
                elif self.category_options == 'set':
                    search_domain.append(('doc_related_info_lines.category', '!=', False))
                elif self.category_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.category', '=', False))

            if 'Remark' in fields_list:

                if self.remark_options == 'contains':
                    search_domain.append(('remark', 'ilike', self.remark))
                elif self.remark_options == 'not_contains':
                    search_domain.append(('remark', 'not like', self.remark))
                elif self.remark_options == 'set':
                    search_domain.append(('remark', '!=', False))
                elif self.remark_options == 'not_set':
                    search_domain.append(('remark', '=', False))

            if 'Star Rating For Importance Of Utility' in fields_list:

                if self.star_rating_options == 'is_like':
                    search_domain.append(('star_rating', '=', self.star_rating))
                elif self.star_rating_options == 'not_like':
                    search_domain.append(('star_rating', '!=', self.star_rating))
                elif self.star_rating_options == 'set':
                    search_domain.append(('star_rating', '!=', False))
                elif self.star_rating_options == 'not_set':
                    search_domain.append(('star_rating', '=', False))

            if 'Person' in fields_list:

                ids_of_person = []
                if len(self.person) > 0:
                    for record in self.person:
                        ids_of_person.append(record.id)

                if self.person_options == 'contains':
                    if self.person_bool:
                        if len(ids_of_person) > 0:
                            for person_id in ids_of_person:
                                search_domain.append(('doc_related_info_lines.person_id.id', '=', person_id))
                    else:
                        search_domain.append(('doc_related_info_lines.person_id.id', 'in', ids_of_person))

                elif self.person_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.person_id', 'not in', ids_of_person))
                elif self.person_options == 'set':
                    search_domain.append(('doc_related_info_lines.person_id', '!=', False))
                elif self.person_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.person_id', '=', False))

            if 'Sanstha' in fields_list:

                ids_of_sanstha = []
                if len(self.sanstha) > 0:
                    for record in self.sanstha:
                        ids_of_sanstha.append(record.id)

                if self.sanstha_options == 'contains':
                    if self.sanstha_bool:
                        if len(ids_of_sanstha) > 0:
                            for sanstha_id in ids_of_sanstha:
                                search_domain.append(('doc_related_info_lines.sanstha_id.id', '=', sanstha_id))
                    else:
                        search_domain.append(('doc_related_info_lines.sanstha_id.id', 'in', ids_of_sanstha))

                elif self.sanstha_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.sanstha_id', 'not in', ids_of_sanstha))
                elif self.sanstha_options == 'set':
                    search_domain.append(('doc_related_info_lines.sanstha_id', '!=', False))
                elif self.sanstha_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.sanstha_id', '=', False))

            if 'Samuday' in fields_list:

                ids_of_samuday = []
                if len(self.samuday) > 0:
                    for record in self.samuday:
                        ids_of_samuday.append(record.id)

                if self.samuday_options == 'contains':
                    if self.samuday_bool:
                        if len(ids_of_samuday) > 0:
                            for samuday_id in ids_of_samuday:
                                search_domain.append(('doc_related_info_lines.samuday_id.id', '=', samuday_id))
                    else:
                        search_domain.append(('doc_related_info_lines.samuday_id.id', 'in', ids_of_samuday))

                elif self.samuday_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.samuday_id', 'not in', ids_of_samuday))
                elif self.samuday_options == 'set':
                    search_domain.append(('doc_related_info_lines.samuday_id', '!=', False))
                elif self.samuday_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.samuday_id', '=', False))

            if 'Samiti' in fields_list:

                ids_of_samiti = []
                if len(self.samiti) > 0:
                    for record in self.samiti:
                        ids_of_samiti.append(record.id)

                if self.samiti_options == 'contains':
                    if self.samiti_bool:
                        if len(ids_of_samiti) > 0:
                            for samiti_id in ids_of_samiti:
                                search_domain.append(('doc_related_info_lines.samiti_id.id', '=', samiti_id))
                    else:
                        search_domain.append(('doc_related_info_lines.samiti_id.id', 'in', ids_of_samiti))

                elif self.samiti_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.samiti_id', 'not in', ids_of_samiti))
                elif self.samiti_options == 'set':
                    search_domain.append(('doc_related_info_lines.samiti_id', '!=', False))
                elif self.samiti_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.samiti_id', '=', False))

            if 'Mahatma' in fields_list:

                ids_of_mahatma = []
                if len(self.mahatma) > 0:
                    for record in self.mahatma:
                        ids_of_mahatma.append(record.id)

                second_domain = search_domain

                if self.mahatma_options == 'contains':
                    if self.mahatma_bool:
                        if len(ids_of_mahatma) > 0:
                            for mahatma_id in ids_of_mahatma:
                                search_domain.append(('doc_related_info_lines.mahatma_id.id', '=', mahatma_id))
                                second_domain.append((
                                    'doc_related_info_lines.samiti_id.samiti_mahatma_id.mahatma_id.id',
                                    '=', mahatma_id))

                    else:
                        search_domain.append(('doc_related_info_lines.mahatma_id.id', 'in', ids_of_mahatma))
                        second_domain.append(
                            ('doc_related_info_lines.samiti_id.samiti_mahatma_id.mahatma_id.id', 'in', ids_of_mahatma))

                elif self.mahatma_options == 'not_contains':
                    search_domain.append(('doc_related_info_lines.mahatma_id', 'not in', ids_of_mahatma))
                elif self.mahatma_options == 'set':
                    search_domain.append(('doc_related_info_lines.mahatma_id', '!=', False))
                elif self.mahatma_options == 'not_set':
                    search_domain.append(('doc_related_info_lines.mahatma_id', '=', False))

            doc_results = []

            AndDocSearch = self.env['documents.model'].search(search_domain)

            if AndDocSearch not in elements and len(AndDocSearch) > 0:
                for doc in AndDocSearch:
                    doc_results.append(doc.id)

            if 'Mahatma' in fields_list:
                SecondDocSearch = self.env['documents.model'].search(second_domain)

                if SecondDocSearch not in elements and len(SecondDocSearch) > 0:
                    for doc in SecondDocSearch:
                        if doc.id not in doc_results:
                            doc_results.append(doc.id)

            if 'Link With Field' in fields_list:

                if 'Link With Field' in fields_list and len(fields_list) == 1:
                    doc_results = []

                    list_of_recs = self.get_link_with_field_records(self, self.link_with_field_options,
                                                                    doc_types=('doc_type', 'in', doc_typ))

                    if list_of_recs not in elements and len(list_of_recs) > 0:
                        for rec in list_of_recs:
                            doc_results.append(rec)

                else:

                    if len(doc_results) > 0:
                        domain = doc_results
                        type_of_doc = False

                    else:
                        type_of_doc = ('doc_type', 'in', doc_typ)
                        domain = False

                    doc_results = self.get_link_with_field_records(self, self.link_with_field_options,
                                                                   search_domain=domain, doc_types=type_of_doc)

            if len(doc_results) > 0:

                message_id = self.env['advance.search.result'].create({'document_ids': doc_results})
                return {
                    'name': _('Advance Documents Search Results'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'advance.search.result',
                    'res_id': message_id.id,
                    'target': 'new'
                }

            else:

                message_id = self.env['message.wizard'].create({'message': _("There're no Document found.")})
                return {
                    'name': _('Advance Documents Search Results'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    'res_id': message_id.id,
                    'target': 'new'
                }

    def clear_wiz(self):
        message_id = self.env['advance.search'].create({})
        return {
            'name': _('Documents Advance Search'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'advance.search',
            'res_id': message_id.id,
            'target': 'new'
        }

    def reset_all_elements(self, a):

        a.need_sr_no = False
        a.sr_no = False
        a.need_subject = False
        a.subject = False
        a.need_tags = False
        a.tags_id = False
        a.need_tharav = False
        a.tharav_id = False
        a.need_description = False
        a.description = False
        a.need_person = False
        a.person = False
        a.need_sanstha = False
        a.sanstha = False
        a.need_mahatma = False
        a.mahatma = False
        a.need_samuday = False
        a.samuday = False
        a.need_vikram_samvat = False
        a.vikram_samvat = False
        a.need_publishing_date = False
        a.publishing_start_date = False
        a.publishing_end_date = False
        a.publishing_date = False
        a.need_occurence_date = False
        a.occurence_date_options = False
        a.occurance_start_date = False
        a.occurance_end_date = False
        a.need_category = False
        a.category = False
        a.need_link_with_field = False
        a.link_with_field = False
        a.need_remark = False
        a.remark = False
        a.need_star_rating = False
        a.star_rating = False
        a.need_samiti = False
        a.samiti = False

    def get_link_with_field_records(self, self_obj, field_option, and_condition_bool, search_domain=False,
                                    doc_types=False):

        elements = [False, None]
        link_with_field_ids = []

        ids_of_link_with_field = []
        if len(self_obj.link_with_field) > 0:
            for record in self_obj.link_with_field:
                ids_of_link_with_field.append(record.id)

        if field_option in ['set', 'not_set']:
            if field_option == 'set':
                a = '!='
            else:
                a = '='

            domain_for_lekh = [('lekh_ids.link_with_field', a, False)]
            domain_for_nirnaami_lekh = [('nirnaami_lekh_ids.link_with_field', a, False)]
            domain_for_book = [('book_ids.link_with_field', a, False)]
            domain_for_video = [('video_ids.link_with_field', a, False)]

        else:
            if field_option == 'contains':
                m = 'lekh_ids.link_with_field.id'
                n = 'in'

            else:
                m = 'lekh_ids.link_with_field'
                n = 'not in'

            domain_for_lekh = [(m, n, ids_of_link_with_field)]
            domain_for_nirnaami_lekh = [(m, n, ids_of_link_with_field)]
            domain_for_book = [(m, n, ids_of_link_with_field)]
            domain_for_video = [(m, n, ids_of_link_with_field)]

            # if and_condition_bool:
            #     for rec in 0

        search_domain_list = [domain_for_lekh, domain_for_nirnaami_lekh, domain_for_book, domain_for_video]

        if not doc_types:
            pass
        else:
            for element in search_domain_list:
                element.insert(0, doc_types)

        if not search_domain:
            pass
        else:
            x = ('id', 'in', search_domain)
            for element in search_domain_list:
                element.insert(0, x)

        for domain_element in search_domain_list:

            DocSearchObjForLinkWithField = self.env['documents.model'].search(domain_element)
            if DocSearchObjForLinkWithField not in elements and len(DocSearchObjForLinkWithField) > 0:
                for rec in DocSearchObjForLinkWithField:
                    if rec.id not in link_with_field_ids:
                        link_with_field_ids.append(rec.id)

        return link_with_field_ids


class AdvanceSearchResult(models.TransientModel):
    _name = 'advance.search.result'
    _description = 'Advance Search Result'

    document_ids = fields.One2many('documents.model', 'doc_ref_field', string="Documents", readonly=True)

    def go_to_previous_wizard(self):
        return {
            'name': _('Advance Documents Search'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'advance.search',
            'res_id': self._context['active_id'],
            'target': 'new'
        }

    def open_search_name(self):
        wiz_id = self.env['search.name'].create({})
        return {
            'name': _('Add Name for Search'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'search.name',
            'res_id': wiz_id.id,
            'target': 'new'
        }

    # def download_attachments(self):

    #     if self.document_ids in [False, None] or len(self.document_ids)>0:
    #         raise ValidationError("There's no data to export.")

    #     import os, zipfile
    #     def isBase64_decodestring(s):
    #         try:
    #             return base64.decodestring(s)
    #         except Exception as e:
    #             raise ValidationError('Error:' + str(e))

    #         path = os.path.dirname(os.path.realpath(__file__))

    #         for rec in self.document_ids:
    #             if rec.doc_type == 'lekh':
    #                 binary_field_name = rec.lekh_ids.lekh_realated_info_lines.lekh_image
    #             elif rec.doc_type == 'nirnaami_lekh':
    #                 binary_field_name = rec.nirnaami_lekh_ids.nirnaami_related_info_lines.lekh_image
    #             elif rec.doc_type == 'book':
    #                 binary_field_name = rec.book_ids.book_realated_info_lines.lekh_image
    #             elif rec.doc_type == 'video':
    #                 binary_field_name = rec.lekh_ids.video_realated_info_lines.lekh_image

    #             file_name = "static\\src\\any_folder" + str(rec.subject.strip().replace(' ', '_').replace('-', '_'))
    #             file_name_zip = file_name+".rar"
    #             zipfilepath = os.path.join(path, file_name_zip)
    #             zip_archive = zipfile.ZipFile(zipfilepath, "w")

    #             object_name = binary_field_name
    #             object_handel = open(object_name, "w")
    #             object_handel.write(isBase64_decodestring(rec.attachment))
    #             object_handel.close()

    #             zip_archive.write(object_name)
    #             zip_archive.close()

    #             return {
    #                 'type': 'ir.actions.act_url',
    #                 'url':str('project_j/static/src/any_folder')+str('zip_file_name_with_rar_extention'),
    #                 'target':'new',
    #             }
