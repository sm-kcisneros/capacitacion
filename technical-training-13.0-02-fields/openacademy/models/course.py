# -*- coding: utf-8 -*-
from odoo import tools, fields, models, api, _
from odoo.exceptions import ValidationError

#total = fields.Float(compute='_compute_cantidad')

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('openacademy.partner', string="Responsible", ondelete='set null', index=True, domain=[('instructor','=','maestro')])

    level = fields.Selection([('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], string="Difficulty Level")
    
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    
    # RESTRINGIR CON SQL
    #se restringe que el nombre del curso y la descripcion tienen que ser diferentes
    _sql_constraints = [
        ('name_descrption_check', 'CHECK(name!=description)', 'tiene que ser diferente el nombre del curo y la descrpcion'),
        ('name_unique', 'UNIQUE(name)', "The course title must be unique")
    ]

#SSESION MODEL

class Session(models.Model):
    _name = 'openacademy.session'
    _inherit  =  [ 'mail.thread', 'mail.activity.mixin'] 
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")], default='draft')

    start_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1, track_visibility="onchange")

    instructor_id = fields.Many2one('openacademy.partner', string="Instructor", domain=[('instructor','=','instructor')])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('openacademy.partner', string="Attendees", domain=[('instructor','=','alumno')])
    
    taken_quantity = fields.Float(compute='_compute_taken_quantity', store=True)#contar cuantos asistentes hay
    attendees_count = fields.Integer(compute='_get_attendees_count', store=True)#contar cuantos asistentes hay
    
    quantity=fields.Float( string="Quantity")
    
#limitando con Onchange
#      @api.onchange("attendee_ids")
#      def check_change(self):
#          if len(self.attendee_ids)>self.quantity:
#              raise ValidationError(
#                      "Increase seats or remove excess attendees")

#campo computarizado para calcular el porcentaje de asistentes estan inscritos
    @api.depends('quantity', 'attendee_ids')
    def _compute_taken_quantity(self):
        for session in self:
            if not session.quantity:
                session.taken_quantity = 0.0
            else:
                session.taken_quantity = 100.0 * len(session.attendee_ids) / session.quantity
                

#campo computarizado para capturar la cantidad de asistentes que estan inscritos
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for session in self:
            session.attendees_count = len(session.attendee_ids)
            
#limitando con constrains
    @api.constrains('attendee_ids')
    def _check_constrains(self):
            if len(self.attendee_ids) > self.quantity:#se limita la cantidad de asistentes para que no pase la cantidad que se pueden inscribir
                raise ValidationError("Increase seats or remove excess attendees")
            if self.instructor_id in self.attendee_ids:# se restringe que un instrunctor pueda inscribir al mismo curos que enseña como asistente
                raise ValidationError("the instructor cannot be as a student")
            if len(self.attendee_ids) >= self.quantity/2:
                self.write({
                    'state': 'confirmed',
                })
                

    #This function is triggered when the user clicks on the button 'Set to concept'
    @api.one
    def draft_progressbar(self):
        self.write({
            'state': 'draft',
        })

    #This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def confirmed_progressbar(self):
        self.write({
            'state': 'confirmed'
        })

    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    def done_progressbar(self):
        self.write({
            'state': 'done',
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
