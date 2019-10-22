# -*- coding: utf-8 -*-
from odoo import tools, fields, models, api, _
from odoo.exceptions import ValidationError

#total = fields.Float(compute='_compute_cantidad')

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    x_name = fields.Char(string='Title', required=True)
    x_description = fields.Text()

    x_responsible_id = fields.Many2one('openacademy.partner', string="Responsible", ondelete='set null', index=True, domain=[('x_instructor','=','instructor')])

    x_level = fields.Selection([('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], string="Difficulty Level")
    
    x_session_ids = fields.One2many('openacademy.session', 'x_course_id', string="Sessions")
    
    x_course_name=fields.Char(compute='_get_name_user')
    
    @api.depends('x_responsible_id')
    def _get_name_user(self):
        """
        get responsible of openacademy.partner model        
        
        """
        for user in self:
            user.x_course_name=user.x_responsible_id.x_user 
        
    
    # RESTRINGIR CON SQL
    # course name and session name must be different
    _sql_constraints = [
        ('name_descrption_check', 'CHECK(x_name!=x_description)', 'Course name and session name must be different'),
        ('name_unique', 'UNIQUE(x_name)', "The course title must be unique")
    ]

#SSESION MODEL

class Session(models.Model):
    _name = 'openacademy.session'
    _inherit  =  [ 'mail.thread', 'mail.activity.mixin'] 
    _description = 'Session'

    x_name = fields.Char(required=True)
    x_active = fields.Boolean(default=True)
    x_state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")], default='draft')

    x_start_date = fields.Date(default=fields.Date.context_today)
    x_duration = fields.Float(digits=(6, 2), help="Duration in days", default=1, track_visibility="onchange")

    x_instructor_id = fields.Many2one('openacademy.partner', string="Instructor", domain=[('x_instructor','=','maestro')])
    x_course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    x_attendee_ids = fields.Many2many('openacademy.partner', string="Attendees", domain=[('x_instructor','=','alumno')])
    
    x_taken_quantity = fields.Float(compute='_compute_taken_quantity', store=True)#calculate the porcentage of attendees
    x_attendees_count = fields.Integer(compute='_get_attendees_count', store=True)#count the quantity of attendees
    
    x_quantity=fields.Float( string="Quantity")
    
#computed field for calculate the porcentange of attendee
    @api.depends('x_quantity', 'x_attendee_ids')
    def _compute_taken_quantity(self):
        for session in self:
            if not session.x_quantity:
                session.x_taken_quantity = 0.0
            else:
                session.x_taken_quantity = 100.0 * len(session.x_attendee_ids) / session.x_quantity
                

#computed field for capture the quantity of atendees
    @api.depends('x_attendee_ids')
    def _get_attendees_count(self):
        for session in self:
            session.x_attendees_count = len(session.x_attendee_ids)
            
#limiting with constraint
    @api.constrains('attendee_ids')
    def _check_constrains(self):
            if len(self.x_attendee_ids) > self.x_quantity:#limit the quntity of attendees who can register
                raise ValidationError("Increase seats or remove excess attendees")
            if self.x_instructor_id in self.x_attendee_ids:#the instructor cannot register in the session
                raise ValidationError("the instructor cannot be as a student")
            if len(self.x_attendee_ids) >= self.x_quantity/2:#change the state to confirmed
                self.write({
                    'x_state': 'confirmed',
                })
                
        
    @api.multi
    def open_wizard(self):
        ### New code
        _openacademy_wizard = self.env.ref('openacademy.wizard_form_view').read()[0]
         
        return {

            'views': [
                [_openacademy_wizard['id'], 'form'],
            ],
            
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy.wizard',
            'name': 'Add Attendee',
            'target': 'new',

        }
