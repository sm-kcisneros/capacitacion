from odoo import http 
from odoo.http import request 
from odoo.exceptions import ValidationError

class Academy(http.Controller):
    @http.route('/academy', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teachers']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
        })
    
    @http.route('/academy/<model("openacademy.teachers"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })
    
class CourseAcademy(http.Controller):
#     @http.route('/Courses', auth='public', website=True)
#     def index(self, **kw):
#         Course = http.request.env['openacademy.course']
#         return http.request.render('openacademy.courses', {
#             'courses': Course.search([])
#         })
    
#     @http.route('/Courses/<model("openacademy.course"):sessions>/', auth='public', website=True)
    @http.route('/sessions', auth='public', website=True)
    def sessions(self, **kw):
        session = http.request.env['openacademy.session']
        return http.request.render('openacademy.sessions', {
            'sessions': session.search([])
        })
    
    @http.route('/sessions/<model("openacademy.session"):x_sessions>/', auth='public', website=True)
    def x_sessions(self, x_sessions):
        return http.request.render('openacademy.description', {
            'x_session': x_sessions
        })