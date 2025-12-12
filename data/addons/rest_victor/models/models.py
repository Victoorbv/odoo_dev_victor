from odoo import models, fields, api


class platos_victor(models.Model):
    _name = 'rest_victor.platos_victor'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    nombre = fields.Char()
    descripcion = fields.Text()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
   
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

