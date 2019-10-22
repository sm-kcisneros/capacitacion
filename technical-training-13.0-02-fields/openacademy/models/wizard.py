from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"
    
    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    x_session_ids = fields.Many2many('openacademy.session',string="Session", required=True, default=_default_sessions)
    x_attendee_ids = fields.Many2many('openacademy.partner', string="Attendees", domain =[('x_instructor','=','alumno')])
    
    @api.multi
    
    def subscribe(self):
    
#     Registered the atendees in sessions
    
        for session in self.x_session_ids:
            session.x_attendee_ids |= self.x_attendee_ids
            
        return {}