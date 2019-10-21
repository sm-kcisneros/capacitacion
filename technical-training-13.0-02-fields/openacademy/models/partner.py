# -*- coding: utf-8 -*-, api
from odoo import api, fields, models


class Partner(models.Model):
    _name = 'openacademy.partner'
    _description = 'Partner'

    x_user = fields.Many2many('res.users', string="Name")

    instructor = fields.Selection([('instructor', 'Instructor'), ('maestro', ' Maestro'), ('alumno', 'Alumno')], default='alumno')
    phone = fields.Char(string='phone')
    adress = fields.Char(string='Adress')
    city = fields.Char(strin='City')
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
    x_name = fields.Char(compute="_get_name_partner", string="Full Name")
    
    @api.depends('x_user')
    def _get_name_partner(self):
        for user in self:
            user.x_name=user.x_user.name
        
        
#     instructor_type= fields.Char(compute="_get_instructor_type", string="User type", store=True)
            
          
#     @api.depends('instructor')
#     def _get_instructor_type(self):
#         for partner in self:
#             if partner.instructor == True:
#                 partner.instructor_type="Instructor"
#             else:
#                 partner.instructor_type="Attendee"
            