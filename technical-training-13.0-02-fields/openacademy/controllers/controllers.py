from odoo import http 
from odoo.http import request 

class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teachers']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
        })
#     @http.route('/academy/<name>/', auth='public', website=True)
#     def teacher(self, name):
#         return '<h1>{}</h1>'.format(name)