from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from .logica_dronify import *

# Modelo USUARIOS****************************************************************
#********************************************************************************
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
    
    dron_autorizado_ids = fields.Many2many(
        comodel_name = 'dron_vic.drones_vic',
        relation = 'relacion_piloto_dron',
        column1 = 'piloto_id',
        column2 = 'dron_id',
        string = "Drones autorizados para el piloto",
        help = "Drones que el piloto está autorizado a volar"
    )

# Modelo DRONES****************************************************************
#******************************************************************************
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

    piloto_autorizado_ids = fields.Many2many(
        comodel_name = 'res.partner',
        relation = 'relacion_dron_piloto',
        column1 = 'dron_id',
        column2 = 'piloto_id',
        string = "Pilotos autorizados para el dron",
        help = "Pilotos que están autorizados a volar este dron",
        domain = [('es_piloto', '=', True)]
    )


# Modelo PAQUETES****************************************************************
#********************************************************************************
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
    # Cliente que envía el paquete, relación con res.partner, solo aquellos que sean clientes
    cliente_id = fields.Many2one(
        'res.partner',
        string = "Enviado por",
        help = "Cliente que envía el paquete",
        required = True,
        domain = [('es_cliente', '=', True)]
    )

    vuelo_id = fields.Many2one(
        'dron_vic.vuelos_vic',
        string = "Vuelo asignado",
        help = "Vuelo al que está asignado el paquete",
        readonly = True
    )
    
    dron_relacionado = fields.Char(
        string = "Nombre del dron",
        related = 'vuelo_id.dron_id.name',
        readonly = True
    )
# Modelo VUELOS****************************************************************
#******************************************************************************
class vuelos_vic(models.Model):
    _name = 'dron_vic.vuelos_vic'
    _description = "Modelo para representar los vuelos realizados por los drones, incluyendo información sobre el piloto, el dron utilizado, el paquete transportado y la fecha del vuelo"

    # Codigo generado automáticamente para cada vuelo, no se puede modificar, formato YYYYMMDDHHMMSS
    codigo = fields.Char(
        string = "Identificador único",
        help = "Identificador único que identifica el vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%H%M%S'),
        readonly = True
    ) 

    name = fields.Char(
        string = "Denominación de la misión",
        required = True,
        help = "Denominación de la misión o propósito del vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d') + "_Vuelo"
        
    )

    dron_id = fields.Many2one(
        'dron_vic.drones_vic',
        string = "Dron asignado",
        help = "Dron asignado para el vuelo",
        required = True
    )

    piloto_id = fields.Many2one(
        'res.partner',
        string = "Piloto asignado",
        help = "Piloto asignado para el vuelo",
        domain = [('es_piloto', '=', True)],
        required = True
    )
    
    paquetes_ids = fields.One2many(
        'dron_vic.paquetes_vic',
        'vuelo_id',
        string = "Paquetes a transportar",
        help = "Paquetes que se transportarán en el vuelo"
    )

    preparado = fields.Boolean(
        string = "Está preparado para el vuelo",
        help = "Indica si el vuelo está listo para ejecutarse"
    )

    realizado = fields.Boolean(
        string = "Vuelo realizado",
        help = "Indica si el vuelo ha sido realizado"
    )

    peso_total = fields.Float(
        string = "Suma del peso de todos los paquetes asignados",
        compute = '_compute_peso_total',
        store = True
    )

    consumo_estimado = fields.Float(
        string = "Consumo estimado de batería para el vuelo",
        compute = '_compute_consumo_estimado',
        store = True
    )

    @api.depends('paquetes_ids')
    def _compute_peso_total(self):
        for vuelo in self:
            vuelo.peso_total = sum(paquete.peso for paquete in vuelo.paquetes_ids)

    @api.depends('peso_total')
    def _compute_consumo_estimado(self):
        for vuelo in self:
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total, vuelo.piloto_id.es_vip)

    def _validar_preparacion(self):
        for vuelo in self:
            raise

    def action_preparar_vuelo(self):
        for vuelo in self:
            raise

    def action_desbloquear(self):
        for vuelo in self:
            raise
        
    def action_finalizar_vuelo(self):
        for vuelo in self:
            raise





    


