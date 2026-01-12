from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

# Modelo tareas ********************************************************************
# **********************************************************************************
class tareas_victor(models.Model):
    _name = 'gestion_tareas_victor.tareas_victor'
    _description = 'gestion_tareas_victor.tareas_victor'

    codigo = fields.Char(
       compute="_get_codigo",
    )
    
    nombre = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")
    fecha_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")
    
    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")

    finalizado = fields.Boolean(
        string="Finalizado", 
        help="Indica si la tarea ha sido finalizada o no")
    
    sprint = fields.Many2one(
        'gestion_tareas_victor.sprints_victor',
        string='Sprint relacionado', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')
    
    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_victor.tecnologias_victor',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')
            
    def _get_codigo(self):
        _logger.info("Iniciando generación de códigos de tareas")
        for tarea in self:
            try:
                if tarea.sprint:
                    tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)
                    _logger.debug(f"Código generado: {tarea.codigo}")
                else:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                    tarea.codigo = "SIN_SPRINT_" + str(tarea.id)

            except Exception as e:
                _logger.error(f"Error generando código para tarea {tarea.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")

   
    
# Modelo sprints ********************************************************************
# **********************************************************************************
class sprints_victor(models.Model):
    _name = 'gestion_tareas_victor.sprints_victor'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del sprint")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del sprint")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del sprint")
      
    duracion = fields.Integer(
       string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")
        

    tareas = fields.One2many(
    'gestion_tareas_victor.tareas_victor', 
    'sprint',
    string='Tareas del Sprint')

    # DEPENDS ******************************************************************************
    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            try:
                if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                    sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
                else:
                    sprint.fecha_fin = sprint.fecha_ini
            except Exception as e:
                raise ValidationError(f"Error al calcular la fecha de fin: {str(e)}")

    # CONSTRAINS ******************************************************************************
    @api.constrains('fecha_ini', 'fecha_fin')
    def _check_fechas(self):
        for sprint in self:
            if sprint.fecha_fin and sprint.fecha_ini:
                if sprint.fecha_fin < sprint.fecha_ini:
                    raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
      

# Modelo tecnologías ********************************************************************
# ***************************************************************************************
class tecnologias_victor(models.Model):
    _name = 'gestion_tareas_victor.tecnologias_victor'
    _description = 'Modelo de Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología")
    
    rel_tareas = fields.Many2many(
        comodel_name='gestion_tareas_victor.tareas_victor',
        relation='relacion_tareas_tecnologias',
        column1='rel_tecnologias',
        column2='rel_tareas',
        string='Tareas')