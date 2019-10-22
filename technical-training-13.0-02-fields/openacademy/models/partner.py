# -*- coding: utf-8 -*-, api
from odoo import api, fields, models


class Partner(models.Model):
    _name = 'openacademy.partner'
    _description = 'Partner'

    x_user = fields.Many2many('res.users', string="Name")

    x_instructor = fields.Selection([('instructor', 'Instructor'), ('maestro', ' Maestro'), ('alumno', 'Alumno')], default='alumno')
    x_phone = fields.Char(string='phone')
    x_adress = fields.Char(string='Adress')
    x_city = fields.Char(strin='City')
    x_session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
    x_name = fields.Char(compute="_get_name_partner", string="Full Name")
    
    @api.depends('x_user') #capture the name of res.user
    def _get_name_partner(self):
        for user in self:
            user.x_name=user.x_user.name