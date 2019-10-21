from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.users'

    name = fields.Char()

    user_type = fields.Selection([('instructor', 'Instructor'), ('maestro', ' Maestro'), ('alumno', 'Alumno')], default='alumno')
    phone = fields.Integer(string='phone')
    adress = fields.Char(string='Adress')
    city = fields.Char(strin='City')
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)