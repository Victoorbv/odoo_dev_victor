from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


# Modelo platos ********************************************************************
# **********************************************************************************
class platos_victor(models.Model):
    _name = 'rest_victor.platos_victor'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    codigo = fields.Char(
       compute="_get_codigo"
    )

    name = fields.Char(
        string = " Nombre del Plato",
        required = True,
        help = "Nombre descripción del plato"
    )
    descripcion = fields.Text(
        string = "Descripción del Plato",
        required = False,
        help = "Descripción detallada del plato"
    )

    precio = fields.Float(
        string = "Precio del Plato",
        required = True,
        help = "Precio del plato en euros"
    )

    precio_con_iva = fields.Float(
        compute="_compute_precio_con_iva"
    )

    descuento = fields.Float(
        string = "Descuento (%)"
    )

    precio_final = fields.Float(
        compute="_compute_precio_final",
        store = True
    )

    tiempo_preparacion = fields.Integer(
        string="Tiempo de Preparación",
        required=False,
        help="Tiempo estimado de preparación en minutos"
    )
    
    disponible = fields.Boolean(
        string="Disponible",
        default=True,
        help="Indica si el plato está disponible para ordenar"
    )

    categoria = fields.Selection(
        string="Categoría",
        required=False,
        selection=[
            ('entrante', 'Entrante'),
            ('principal', 'Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida')
        ],
        help="Categoría del plato"
    )

    menu = fields.Many2one(
        'rest_victor.menu_victor',
        string='Menú relacionado', 
        ondelete='set null', 
        help='Menú al que pertenece este plato'
    )

    rel_ingredientes = fields.Many2many(
        comodel_name='rest_victor.ingredientes_victor',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes'
    )
    # Depends ************************************************************
    #**********************************************************************
    @api.depends('categoria')
    def _get_codigo(self):
        for plato in self:
            try:
                # Si la tarea no tiene categoria asignada
                if not plato.categoria:
                    plato.codigo = "PLT_" + str(plato.id)
                    _logger.warning(f"Plato {plato.id} sin categoría asignada")
                else:
                    # Si tiene categoria, usamos su nombre
                    plato.codigo = plato.categoria[:3].upper() + "_" + str(plato.id)
                _logger.debug(f"Código generado: {plato.codigo}")
            except Exception as e:
                _logger.error(f"Error generando código para plato {plato.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")


    @api.depends('precio')
    def _compute_precio_con_iva(self):
        for plato in self:
            if plato.precio:
                plato.precio_con_iva = plato.precio * 1.10
            else:
                plato.precio_con_iva = 0.0

    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            if not plato.precio:
                plato.precio_final = 0.0
            elif plato.descuento:
                descuento_decimal = plato.descuento / 100.0
                plato.precio_final = plato.precio * (1 - descuento_decimal)
            else:
                plato.precio_final = plato.precio
    #Constrains ***********************************************************
    #**********************************************************************
    @api.constrains('precio')
    def _verificar_precio(self):
        for plato in self:
            if plato.precio < 0:
                _logger.error(f"Precio inválido para el plato {plato.id}: {plato.precio}")
                raise ValidationError("El precio no puede ser inferior a 0")
            else:
                _logger.info(f"Precio válido para el plato {plato.id}: {plato.precio}")
            
    @api.constrains('tiempo_preparacion')
    def _verificar_tiempo_preparacion(self):
        for plato in self:
            if plato.tiempo_preparacion:
                if plato.tiempo_preparacion < 1:
                    _logger.error(f"Tiempo de preparación inválido para el plato {plato.id}: {plato.tiempo_preparacion}")
                    raise ValidationError("El tiempo de preparación no puede ser menor 1")
                if plato.tiempo_preparacion > 240:
                    _logger.error(f"Tiempo de preparación inválido para el plato {plato.id}: {plato.tiempo_preparacion}")
                    raise ValidationError("El tiempo de preparación no puede ser mayor 240")
            


# Modelo menu ********************************************************************
# **********************************************************************************
class menu_victor(models.Model):
    _name = 'rest_victor.menu_victor'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    name = fields.Char(
        string = " Nombre del Menú",
        required = True,
        help = "Nombre del menú"
    )
    descripcion = fields.Text(
        string = "Descripción del Menú",
        required = False,
        help = "Descripción detallada del menú"
    )
    fecha_inicio = fields.Date(
        string="Fecha de Inicio",
        required=True,
        help="Fecha de inicio de la validez del menú"
    )

    fecha_fin = fields.Date(
        string="Fecha de Fin",
        required=False,
        help="Fecha de fin de la validez del menú"
    )

    activo = fields.Boolean(
        string="Activo",
        default=True,
        help="Indica si el menú está activo"
    )

    platos = fields.One2many(
        'rest_victor.platos_victor',
        'menu',
        string='Platos del Menú',    
    )
    precio_total = fields.Float(
        compute="_compute_precio_total",
        store=True
    )

    # Depends ************************************************************
    #**********************************************************************
    @api.depends('platos','platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
        # Suma el precio_final de todos los platos relacionados
        # La función map() extrae los valores y sum() los agrega.
            precios = menu.platos.mapped('precio_final')
            menu.precio_total = sum(precios)
    #Constrains ***********************************************************
    #**********************************************************************
    @api.constrains('fecha_inicio','fecha_ini')
    def _comprobar_fecha(self):
        for menu in self:
            if menu.fecha_fin:
                if menu.fecha_inicio > menu.fecha_fin:
                    _logger.error(f"Fechas inválidas para el menú {menu.id}: inicio {menu.fecha_inicio}, fin {menu.fecha_fin}")
                    raise ValidationError("La fecha de inicio no puede ser posterior a la de fin")
    
    @api.constrains('platos','activo')
    def _comprobar_platos_activo(self):
        for menu in self:
            if len(menu.platos) == 0 and menu.activo:
                _logger.error(f"Menú activo sin platos para el menú {menu.id}")
                raise ValidationError("Un menú activo debe tener al menos un plato asignado")

    
    
   

# Modelo ingredientes ********************************************************************
# **********************************************************************************
class ingredientes_victor(models.Model):
    _name = 'rest_victor.ingredientes_victor'
    _description = 'Modelo de Ingredientes para Gestión de Restaurante'

    name = fields.Char(
        string = " Nombre del Ingrediente",
        required = True,
        help = "Nombre del ingrediente"
    )
    
    es_alergeno = fields.Boolean(
        string = "Es Alergeno",
        default = False,
    )

    descripcion = fields.Text(
        string = "Descripción del Ingrediente",
        required = False,
        help = "Descripción detallada del ingrediente"
    )

    rel_platos = fields.Many2many(
        comodel_name='rest_victor.platos_victor',
        relation='relacion_platos_ingredientes',
        column1='rel_ingredientes',
        column2='rel_platos',
        string='Platos'
    )