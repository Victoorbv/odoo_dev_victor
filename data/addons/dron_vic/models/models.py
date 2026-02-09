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

class drones_vic(models.Model):
    _name = 'dron_vic.drones_vic'
    _description = 'Modelo para representar los activos físicos de la empresa y su estado operativo'

    name = fields.Char(
        string = "Nombre del dron",
        required = True,
        help = "Nombre identificativo del dron"
    )
    capacidad_max = fields.Float(
        string = "Capacidad máxima en kilogramas",
        required = True,
        help = "Capacidad máxima en kilogramas que el dron puede transportar"
    )

    bateria = fields.Integer(
        string = "Nivel de carga actual",
        default = 100,
        help = "Nivel de batería del dron, expresado en porcentaje"
    )

    estado = fields.Selection(
        string = "Estado operativo del dron",
        selection = [
            ('disponible', 'Disponible'),
            ('en_uso', 'En uso'),
            ('mantenimiento', 'Mantenimiento')
        ],
        default = 'disponible',
        help = "Estado operativo del dron"
    )


class paquetes_vic(models.Model):
    _name = 'dron_vic.paquetes_vic'
    _description = 'Modelo para representar los activos físicos de la empresa y su estado operativo'
    
    # Codigo generado automáticamente para cada paquete, no se puede modificar, formato YYYYMMDDHHMMSS
    codigo = fields.Char(
        string = "Identificador único",
        help = "Identificador único que identifica al paquete",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%H%M%S'),
        readonly = True
    ) 

    name = fields.Char(
        string = "Descripción del contenido",
        required = True,
        help = "Descripción del contenido del paquete"
    )
   
    peso = fields.Float(
        string = "Peso en kilogramos",
        required = True,
        help = "Peso del paquete en kilogramos"
    )

class vuelos_vic(models.Model):
    _name = 'dron_vic.vuelos_vic'
    _description = "Modelo para representar los vuelos realizados por los drones, incluyendo información sobre el piloto, el dron utilizado, el paquete transportado y la fecha del vuelo"
  
     # Codigo generado automáticamente para cada vuelo, no se puede modificar, formato YYYYMMDDHHMMSS
    codigo = fields.Char(
        string = "Identificador único",
        help = "Identificador único que identifica el vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%H%M%S'),
        readonly = True,
        store=True
    ) 

    name = fields.Char(
        string = "Denominación de la misión",
        required = True,
        help = "Denominación de la misión o propósito del vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%') + "_Vuelo",
        store=True
    )

    preparado = fields.Boolean(
        string = "Está preparado para el vuelo",
        help = "Indica si el vuelo está preparado para ser realizado",
        store=True
    )

    realizado = fields.Boolean(
        string = "Vuelo realizado",
        help = "Indica si el vuelo ha sido realizado",
        store=True
    )




    


