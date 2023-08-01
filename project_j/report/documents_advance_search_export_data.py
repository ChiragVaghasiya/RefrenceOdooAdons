from odoo import models, fields, api
from odoo import osv
from dateutil.rrule import rrule, DAILY
from datetime import datetime
import math
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_TIME_FORMAT


class DocumentsAdvanceSearcExport(models.AbstractModel):
    _name = 'report.project_j.advance_search_documents_xlsx'
    _description = 'Documents Advance Search Export'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        elements = (None, False)

        date = workbook.add_format({'text_wrap': True, 'font_size': 13, 'border': 1})
        titles = workbook.add_format({'bg_color': '#19FFFF', 'text_wrap': True, 'font_size': 13, 'border': 1})
        cells = workbook.add_format({'text_wrap': True, 'font_size': 9.5, 'border': 1})

        sheet = workbook.add_worksheet('Documents')

        sheet.write(0, 0, "Document", titles)
        sheet.write(0, 1, "Sr. No.", titles)
        sheet.write(0, 2, "Subject", titles)
        sheet.write(0, 3, "Description", titles)
        sheet.write(0, 4, "Tags", titles)
        sheet.write(0, 5, "Tharav", titles)
        sheet.write(0, 6, "Remark", titles)
        sheet.write(0, 7, "Star Rating", titles)

        for rec in partners:

            if rec.document_ids not in elements and len(rec.document_ids) > 0:

                x = 1
                for doc in rec.document_ids:

                    sheet.write(x, 0, dict(doc._fields['doc_type'].selection).get(doc.doc_type), cells)

                    sr_no = ''
                    if doc.doc_type == 'lekh':
                        sr_no = doc.sr_no
                    else:
                        sr_no = doc.sr_no_prefix

                    sheet.write(x, 1, sr_no, cells)

                    subject = ''
                    if doc.subject not in elements:
                        subject = doc.subject
                    sheet.write(x, 2, subject, cells)

                    description = ''
                    if doc.description not in elements:
                        subject = doc.description
                    sheet.write(x, 3, description, cells)

                    tags = ''
                    if doc.tags_id not in elements and len(doc.tags_id) > 0:
                        for tag in doc.tags_id:
                            tags += tag.lekh_tag_name + ","
                    sheet.write(x, 4, tags, cells)

                    tharavs = ''
                    if doc.tharav_id not in elements and len(doc.tharav_id) > 0:
                        for tharav in doc.tharav_id:
                            tharavs += tharav.tharav_subject_and_id + ","
                    sheet.write(x, 5, tharavs, cells)

                    remark = ''
                    if doc.remark not in elements:
                        remark = doc.remark
                    sheet.write(x, 6, remark, cells)

                    star_rating = ''
                    if doc.star_rating not in elements:
                        star_rating = dict(doc._fields['star_rating'].selection).get(doc.star_rating)
                    sheet.write(x, 7, star_rating, cells)

                    x += 1


class DocumentsAdvanceSearcSavedExport(models.AbstractModel):
    _name = 'report.project_j.advance_search_documents_saved_xlsx'
    _description = 'Documents Advance Search Saved Export'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        elements = (None, False)

        date = workbook.add_format({'text_wrap': True, 'font_size': 13, 'border': 1})
        titles = workbook.add_format({'bg_color': '#19FFFF', 'text_wrap': True, 'font_size': 13, 'border': 1})
        cells = workbook.add_format({'text_wrap': True, 'font_size': 9.5, 'border': 1})

        if partners.result_type == 'doc':
            sheet_name = 'Documents'

            sheet = workbook.add_worksheet(sheet_name)

            sheet.write(0, 0, "Document", titles)
            sheet.write(0, 1, "Sr. No.", titles)
            sheet.write(0, 2, "Subject", titles)
            sheet.write(0, 3, "Description", titles)
            sheet.write(0, 4, "Tags", titles)
            sheet.write(0, 5, "Tharav", titles)
            sheet.write(0, 6, "Remark", titles)
            sheet.write(0, 7, "Star Rating", titles)

            for rec in partners:

                if rec.document_ids not in elements and len(rec.document_ids) > 0:

                    x = 1
                    for doc in rec.document_ids:

                        sheet.write(x, 0, dict(doc._fields['doc_type'].selection).get(doc.doc_type), cells)

                        sr_no = ''
                        if doc.doc_type == 'lekh':
                            sr_no = doc.sr_no
                        else:
                            sr_no = doc.sr_no_prefix

                        sheet.write(x, 1, sr_no, cells)

                        subject = ''
                        if doc.subject not in elements:
                            subject = doc.subject
                        sheet.write(x, 2, subject, cells)

                        description = ''
                        if doc.description not in elements:
                            subject = doc.description
                        sheet.write(x, 3, description, cells)

                        tags = ''
                        if doc.tags_id not in elements and len(doc.tags_id) > 0:
                            for tag in doc.tags_id:
                                tags += tag.lekh_tag_name + ","
                        sheet.write(x, 4, tags, cells)

                        tharavs = ''
                        if doc.tharav_id not in elements and len(doc.tharav_id) > 0:
                            for tharav in doc.tharav_id:
                                tharavs += tharav.tharav_subject_and_id + ","
                        sheet.write(x, 5, tharavs, cells)

                        remark = ''
                        if doc.remark not in elements:
                            remark = doc.remark
                        sheet.write(x, 6, remark, cells)

                        star_rating = ''
                        if doc.star_rating not in elements:
                            star_rating = dict(doc._fields['star_rating'].selection).get(doc.star_rating)
                        sheet.write(x, 7, star_rating, cells)

                        x += 1

        else:
            sheet_name = 'Magazines'

            sheet = workbook.add_worksheet(sheet_name)

            sheet.write(0, 0, "Name", titles)
            sheet.write(0, 1, "Type", titles)
            sheet.write(0, 2, "State", titles)
            sheet.write(0, 3, "Publication Date", titles)
            sheet.write(0, 4, "Magazine Start Date", titles)
            sheet.write(0, 5, "Start of publication year (ઈ.સ)", titles)
            sheet.write(0, 6, "End of publication year (ઈ.સ)", titles)
            sheet.write(0, 7, "Start of publication year (વિ.સં)", titles)
            sheet.write(0, 8, "End of publication year (વિ.સં)", titles)
            sheet.write(0, 9, "Description", titles)
            sheet.write(0, 10, "Reading Catagory", titles)
            sheet.write(0, 11, "Referring Catagory", titles)
            sheet.write(0, 12, "Severity", titles)
            sheet.write(0, 13, "Is Magazine Avaiilable in GG?", titles)
            sheet.write(0, 14, "Is Magazine Coming to GG?", titles)
            sheet.write(0, 15, "Monitor For Abusive Contents", titles)
            sheet.write(0, 16, "Magazine Group", titles)
            sheet.write(0, 17, "Editor", titles)
            sheet.write(0, 18, "Reader", titles)
            sheet.write(0, 19, "Receiver", titles)
            sheet.write(0, 20, "Link Magazine", titles)
            sheet.write(0, 21, "Paksh", titles)
            sheet.write(0, 22, "Person", titles)
            sheet.write(0, 23, "Sanstha", titles)
            sheet.write(0, 24, "Mahatma", titles)
            sheet.write(0, 25, "Tags", titles)

            for rec in partners:

                if rec.magazine_ids not in elements and len(rec.magazine_ids) > 0:

                    x = 1
                    for doc in rec.magazine_ids:

                        sheet.write(x, 0, doc.name, cells)
                        sheet.write(x, 1, dict(doc._fields['magazine_type'].selection).get(doc.magazine_type), cells)

                        state = ''
                        if doc.magazine_state not in elements:
                            state = dict(doc._fields['magazine_state'].selection).get(doc.magazine_state)
                        sheet.write(x, 2, state, cells)

                        publication_date = ''
                        if doc.magazine_type in ['trimasik', 'dvimasik', 'ardhamasik', 'varsik']:
                            if doc.publication_date not in elements:
                                publication_date = str(doc.publication_date)
                        elif doc.magazine_type == 'mashik':
                            if doc.publication_date_days not in elements:
                                publication_date = doc.publication_date_days
                        elif doc.magazine_type == 'saptahik':
                            if doc.publication_date_days not in elements:
                                publication_date = dict(doc._fields['publication_date_days'].selection).get(
                                    doc.publication_date_days)
                        sheet.write(x, 3, publication_date, cells)

                        magazine_start_date = ''
                        if doc.magazine_start_date not in elements:
                            magazine_start_date = str(doc.magazine_start_date)
                        sheet.write(x, 4, magazine_start_date, cells)

                        publication_start_year = ''
                        if doc.publication_start_year not in elements:
                            publication_start_year = doc.publication_start_year
                        sheet.write(x, 5, publication_start_year, cells)

                        publication_end_year = ''
                        if doc.publication_end_year not in elements:
                            publication_end_year = doc.publication_end_year
                        sheet.write(x, 6, publication_end_year, cells)

                        publication_start_year_vikram_samvant = ''
                        if doc.publication_start_year_vikram_samvant not in elements:
                            publication_start_year_vikram_samvant = doc.publication_start_year_vikram_samvant
                        sheet.write(x, 7, publication_start_year_vikram_samvant, cells)

                        publication_end_year_vikram_samvant = ''
                        if doc.publication_end_year_vikram_samvant not in elements:
                            publication_end_year_vikram_samvant = doc.publication_end_year_vikram_samvant
                        sheet.write(x, 8, publication_end_year_vikram_samvant, cells)

                        description = ''
                        if doc.description not in elements:
                            description = doc.description
                        sheet.write(x, 9, description, cells)

                        reading_category = ''
                        if doc.reading_category not in elements:
                            reading_category = dict(doc._fields['reading_category'].selection).get(doc.reading_category)
                        sheet.write(x, 10, reading_category, cells)

                        referring_category = ''
                        if doc.referring_category not in elements:
                            referring_category = dict(doc._fields['referring_category'].selection).get(
                                doc.referring_category)
                        sheet.write(x, 11, referring_category, cells)

                        severity = ''
                        if doc.severity not in elements:
                            severity = dict(doc._fields['severity'].selection).get(doc.severity)
                        sheet.write(x, 12, severity, cells)

                        is_magazine_available_in_gg = ''
                        if doc.is_magazine_available_in_gg not in elements:
                            is_magazine_available_in_gg = dict(
                                doc._fields['is_magazine_available_in_gg'].selection).get(
                                doc.is_magazine_available_in_gg)
                        sheet.write(x, 13, is_magazine_available_in_gg, cells)

                        is_magazine_coming_to_gg = ''
                        if doc.is_magazine_coming_to_gg not in elements:
                            is_magazine_coming_to_gg = dict(doc._fields['is_magazine_coming_to_gg'].selection).get(
                                doc.is_magazine_coming_to_gg)
                        sheet.write(x, 14, is_magazine_coming_to_gg, cells)

                        monitor_for_abusive_contents = ''
                        if doc.monitor_for_abusive_contents in [True, False]:
                            monitor_for_abusive_contents = str(doc.monitor_for_abusive_contents)
                        sheet.write(x, 15, monitor_for_abusive_contents, cells)

                        magazine_group = ''
                        if doc.magazine_group not in elements:
                            magazine_group = doc.magazine_group
                        sheet.write(x, 16, magazine_group, cells)

                        editor = ''
                        if doc.editor not in elements:
                            editor = doc.editor
                        sheet.write(x, 17, editor, cells)

                        reader = ''
                        if doc.reader not in elements and len(doc.reader) > 0:
                            for data in doc.reader:
                                reader += data.user_name + ","
                        sheet.write(x, 18, reader, cells)

                        receiver = ''
                        if doc.receiver not in elements and len(doc.receiver) > 0:
                            for data in doc.receiver:
                                receiver += data.user_name + ","
                        sheet.write(x, 19, receiver, cells)

                        link_magazine = ''
                        if doc.link_magazine not in elements and len(doc.link_magazine) > 0:
                            for data in doc.link_magazine:
                                link_magazine += data.name + ","
                        sheet.write(x, 20, link_magazine, cells)

                        paksh_id = ''
                        if doc.paksh_id not in elements and len(doc.paksh_id) > 0:
                            for data in doc.paksh_id:
                                paksh_id += data.paksh_name_gujarati + ","
                        sheet.write(x, 21, paksh_id, cells)

                        person_id = ''
                        if doc.person_id not in elements and len(doc.person_id) > 0:
                            for data in doc.person_id:
                                person_id += data.person_name + ","
                        sheet.write(x, 22, person_id, cells)

                        sanstha_id = ''
                        if doc.sanstha_id not in elements and len(doc.sanstha_id) > 0:
                            for data in doc.sanstha_id:
                                sanstha_id += data.sanstha_name + ","
                        sheet.write(x, 23, sanstha_id, cells)

                        mahatma_id = ''
                        if doc.mahatma_id not in elements and len(doc.mahatma_id) > 0:
                            for data in doc.mahatma_id:
                                mahatma_id += data.complete_mahatma_name + ","
                        sheet.write(x, 24, mahatma_id, cells)

                        tags_id = ''
                        if doc.tags_id not in elements and len(doc.tags_id) > 0:
                            for tag in doc.tags_id:
                                tags_id += tag.lekh_tag_name + ","
                        sheet.write(x, 25, tags_id, cells)

                        x += 1
