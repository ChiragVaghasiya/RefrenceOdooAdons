from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition


class Binary(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self, file_dictionary, **kw):
        file_dict = file_dictionary

        zip_filename = datetime.now()
        zip_filename = "%s.zip" % zip_filename
        bitIO = BytesIO()
        zip_file = zipfile.ZipFile(bitIO, "w", zipfile.ZIP_DEFLATED)
        for file_info in file_dict.values():
            zip_file.write(file_info["path"], file_info["name"])
        zip_file.close()
        return request.make_response(bitIO.getvalue(),
                                     headers=[('Content-Type', 'application/x-zip-compressed'),
                                              ('Content-Disposition', content_disposition(zip_filename))])
