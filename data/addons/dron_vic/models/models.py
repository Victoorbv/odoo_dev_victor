from odoo import models, fields, api


class usuarios_vic(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    es_cliente = fields.Boolean(
        string = "Es Cliente"
    )

    es_vip = fields.Boolean(
        string = "Es Vip"
    )

    es_piloto = fields.Boolean(
        string = "Es Piloto"
    )

    licencia = fields.Char(
        string = "Licencia que tiene el piloto"
       
    )


