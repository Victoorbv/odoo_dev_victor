from odoo import models, fields, api


class gestion_tareas_victor(models.Model):
    _name = 'gestion_tareas_victor.gestion_tareas_victor'
    _description = 'gestion_tareas_victor.gestion_tareas_victor'

    nombre = fields.Char()
    descripcion = fields.Text()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

