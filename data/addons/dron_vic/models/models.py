from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from .logica_dronify import *

#********************************************************************************
# Modelo USUARIOS****************************************************************
#********************************************************************************
class usuarios_vic(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    es_cliente = fields.Boolean(
        string = "¿Es Cliente?"
    )

    es_vip = fields.Boolean(
        string = "Cliente Vip"
    )

    es_piloto = fields.Boolean(
        string = "¿Es Piloto?"
    )

    licencia = fields.Char(
        string = "Nº de Licencia"
    )
    
    # -----------------------------
    # Relaciones
    # -----------------------------
    dron_autorizado_ids = fields.Many2many(
        comodel_name = 'dron_vic.drones_vic',
        relation = 'relacion_piloto_dron',
        column1 = 'piloto_id',
        column2 = 'dron_id',
        string = "Drones Autorizados",
        help = "Drones que el piloto está autorizado a volar"
    )

#********************************************************************************
# Modelo DRONES******************************************************************
#********************************************************************************
class drones_vic(models.Model):
    _name = 'dron_vic.drones_vic'
    _description = 'Modelo para representar los activos físicos de la empresa y su estado operativo'

    name = fields.Char(
        string = "Nombre del Dron",
        required = True,
        help = "Nombre identificativo del dron"
    )
    capacidad_max = fields.Float(
        string = "Capacidad Carga (kg)",
        required = True,
        help = "Capacidad máxima en kilogramas que el dron puede transportar"
    )

    bateria = fields.Integer(
        string = "Nivel de Batería (%)",
        default = 100,
        help = "Nivel de batería del dron, expresado en porcentaje"
    )

    estado = fields.Selection(
        string = "Estado",  
        selection = [
            ('disponible', 'Disponible'),
            ('vuelo', 'En Vuelo'),
            ('taller', 'En Taller')
        ],
        default = 'disponible',
        help = "Estado operativo del dron"
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    piloto_autorizado_ids = fields.Many2many(
        comodel_name = 'res.partner',
        relation = 'relacion_piloto_dron',
        column1 = 'dron_id',
        column2 = 'piloto_id',
        string = "Pilotos Autorizados",
        help = "Pilotos que están autorizados a volar este dron",
        domain = [('es_piloto', '=', True)]
    )

#********************************************************************************
# Modelo PAQUETES****************************************************************
#********************************************************************************
class paquetes_vic(models.Model):
    _name = 'dron_vic.paquetes_vic'
    _description = 'Modelo para representar los activos físicos de la empresa y su estado operativo'
    
    # Codigo generado automáticamente para cada paquete, no se puede modificar, formato YYYYMMDDHHMMSS
    codigo = fields.Char(
        string = "Codigo del Paquete",
        help = "Codigo único que identifica al paquete",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%H%M%S'),
        readonly = True
    ) 

    name = fields.Char(
        string = "Descripción",
        required = True,
        help = "Descripción del paquete"
    )
   
    peso = fields.Float(
        string = "Peso (kg)",
        required = True,
        help = "Peso del paquete en kilogramos"
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    cliente_id = fields.Many2one(
        'res.partner',
        string = "Cliente",
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
        string = "Dron de Reparto",
        related = 'vuelo_id.dron_id.name',
        readonly = True
    )
#********************************************************************************
# Modelo VUELOS******************************************************************
#********************************************************************************
class vuelos_vic(models.Model):
    _name = 'dron_vic.vuelos_vic'
    _description = "Modelo para representar los vuelos realizados por los drones, incluyendo información sobre el piloto, el dron utilizado, el paquete transportado y la fecha del vuelo"

    codigo = fields.Char(
        string = "Codigo del Vuelo",
        help = "Codigo único que identifica el vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d%H%M%S'),
        readonly = True
    ) 

    name = fields.Char(
        string = "Denominación",
        required = True,
        help = "Denominación de la misión o propósito del vuelo",
        default = lambda self: fields.Datetime.now().strftime('%Y%m%d') + "_Vuelo"
        
    )

    paquetes_ids = fields.One2many(
        'dron_vic.paquetes_vic',
        'vuelo_id',
        string = "Paquetes",
        help = "Paquetes que se transportarán en el vuelo"
    )

    preparado = fields.Boolean(
        string = "Vuelo Preparado",
        help = "Indica si el vuelo está listo para ejecutarse"
    )

    realizado = fields.Boolean(
        string = "Vuelo Realizado",
        help = "Indica si el vuelo ha sido realizado"
    )
    # -----------------------------
    # Relaciones
    # -----------------------------
    dron_id = fields.Many2one(
        'dron_vic.drones_vic',
        string = "Dron",
        help = "Dron asignado para el vuelo",
        required = True
    )

    piloto_id = fields.Many2one(
        'res.partner',
        string = "Piloto",
        help = "Piloto asignado para el vuelo",
        domain = [('es_piloto', '=', True)],
        required = True
    )

    # -----------------------------
    # Computes y depends
    # -----------------------------
    peso_total = fields.Float(
        string = "Peso Total (kg)",
        compute = '_compute_peso_total',
        store = True
    )

    consumo_estimado = fields.Float(
        string = "Consumo Estimado (%)",
        compute = '_compute_consumo_estimado',
        store = True
    )

    @api.depends('paquetes_ids')
    def _compute_peso_total(self):
        for vuelo in self:
            vuelo.peso_total = sum(paquete.peso for paquete in vuelo.paquetes_ids)

    @api.depends('peso_total', 'piloto_id')
    def _compute_consumo_estimado(self):
        for vuelo in self:
            es_vip = any(vuelo.paquetes_ids.mapped('cliente_id.es_vip'))
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total, es_vip)
            
    # -----------------------------
    # Constraints
    # -----------------------------
    @api.constrains('preparado')
    def _validar_preparacion(self):
        for vuelo in self:
            if not vuelo.preparado:
                break
            if not vuelo.dron_id or not vuelo.piloto_id:
                raise ValidationError("El vuelo debe tener dron y piloto asignados.")
            if not vuelo.paquetes_ids:
                raise ValidationError("El vuelo debe tener al menos un paquete asignado.")
            if vuelo.peso_total > vuelo.dron_id.capacidad_max:
                raise ValidationError(f"¡ERROR DE CARGA! El peso total ({vuelo.peso_total}kg) supera la capacidad maxima del dron({vuelo.dron_id.capacidad_max}kg).")
            if vuelo.dron_id.estado != 'disponible':
                raise ValidationError(f"El dron {vuelo.dron_id.name} no está disponible para el vuelo. Estado actual: {vuelo.dron_id.estado}.")
            if not validar_estado_bateria(vuelo.dron_id.bateria, vuelo.consumo_estimado):
                raise ValidationError(f"¡BATERÍA INSUFICIENTE! Se requiere {vuelo.consumo_estimado}% y el dron solo tiene {vuelo.dron_id.bateria}%.")
            if vuelo.dron_id not in vuelo.piloto_id.dron_autorizado_ids:
                raise ValidationError(f"¡PILOTO NO AUTORIZADO PARA ESTE EQUIPO! El piloto {vuelo.piloto_id.name} no tiene certificación para manejar el dron {vuelo.dron_id.name}.")

    # -----------------------------
    # Botones
    # -----------------------------
    def action_preparar_vuelo(self):
        for vuelo in self:
            vuelo.preparado = True
            vuelo.dron_id.estado = "vuelo"
           

    def action_desbloquear(self):
        for vuelo in self:
           if vuelo.realizado:
               raise ValidationError("El vuelo ya ha sido realizado")
           vuelo.preparado = False
           vuelo.dron_id.estado = "disponible"
        
    def action_finalizar_vuelo(self):
        for vuelo in self:
            if not vuelo.preparado:
               raise ValidationError("El vuelo no ha sido preparado")
            vuelo.realizado = True
            vuelo.dron_id.bateria -= vuelo.consumo_estimado
            vuelo.dron_id.estado = "disponible"





    


