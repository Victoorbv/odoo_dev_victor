from datetime import timedelta
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
        default = 5.0,
        help = "Precio del plato en euros"
    )

    precio_con_iva = fields.Float(
        compute="_compute_precio_con_iva"
    )

    descuento = fields.Float(
        string = "Descuento (%)",
        default = 0.0,
        help = "Descuento aplicado al plato en porcentaje"
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

    def _get_categoria_defecto(self):
        return self.env['rest_victor.categoria_victor'].search([('name', '=', 'Sin Clasificar')], limit=1)
        
    categoria_id = fields.Many2one(
        'rest_victor.categoria_victor',
        string='Categoría',
        required=False,
        ondelete='cascade',
        default=_get_categoria_defecto,
        help='Categoría del plato'
    )

    menu = fields.Many2one(
        'rest_victor.menu_victor',
        string='Menú relacionado', 
        ondelete='set null', 
        help='Menú al que pertenece este plato'
    )

    rel_ingredientes = fields.Many2many(
        comodel_name='rest_victor.ingredients_victor',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes',
        ondelete='cascade'
    )

    chef = fields.Many2one(
        'rest_victor.chef_victor',
        string='Chef relacionado', 
        ondelete='set null', 
        help='Chef al que pertenece este plato'
    )

    chef_especializado = fields.Many2one(
        'rest_victor.chef_victor',
        string='Chef Especializado', 
        compute='_compute_chef_especializado',
        store=True,
        help='Chef especializado en la categoría del plato'
    )

    especialidad_chef = fields.Many2one(
        'rest_victor.categoria_victor',
        string='Especialidad del Chef',
        related='chef.especialidad',
        readonly=True,
        help='Categoría de especialidad del chef asignado al plato'
    )

    fecha_alta  = fields.Date(
        string="Fecha de Alta",
        default=lambda self: fields.Date.today(),
        help="Fecha en que el plato fue dado de alta"
    )

    es_caro = fields.Boolean(
        string="Es Caro",
        compute="_compute_es_caro",
        help="Indica si el plato es considerado caro (precio final > 20 euros)"
    )

    # Depends ************************************************************
    #**********************************************************************
    @api.depends('categoria_id')
    def _compute_chef_especializado(self):
        for plato in self:
            if plato.categoria_id:
                plato.chef_especializado = self.env['rest_victor.chef_victor'].search(
                    [('especialidad', '=', plato.categoria_id.id)], 
                    limit=1
                )
            else:
                plato.chef_especializado = False

    @api.depends('categoria_id')
    def _get_codigo(self):
        for plato in self:
            try:
                # Si la tarea no tiene categoria asignada
                if not plato.categoria_id:
                    plato.codigo = "PLT_" + str(plato.id)
                    _logger.warning(f"Plato {plato.id} sin categoría asignada")
                else:
                    # Si tiene categoria, usamos su nombre
                    plato.codigo = plato.categoria_id.name[:3].upper() + "_" + str(plato.id)
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

    @api.depends('precio_final')
    def _compute_es_caro(self):
        for plato in self:
            if plato.precio_final > 20:
                plato.es_caro = True
            else:
                plato.es_caro = False

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

    dias_disponibles = fields.Integer(
        string="Días Disponibles",
        default=7,
        help="Número de días que el menú estará disponible"
    )

    fecha_fin = fields.Date(
        string="Fecha de Fin",
        compute="_generar_fecha_fin",
        help="Fecha de fin de la validez del menú"
        
    )

    activo = fields.Boolean(
        string="Activo",
        default=False,
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
    
    creado_por = fields.Many2one(
        'res.users',
        string='Creado por',
        default=lambda self: self.env.user,
        readonly=True,
        help='Usuario que creó el menú'
    )

    camareros_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_cam_men',
        column1='menu_id',
        column2='camarero_id',
        string='Camareros Asignados'
    )

    proximo_vencimiento = fields.Boolean(
        string="Próximo a Vencer",
        compute="_compute_proximo_vencimiento",
        help="Indica si el menú está próximo a vencer (menos de 3 días restantes)"
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

    @api.depends('fecha_inicio','dias_disponibles')
    def _generar_fecha_fin(self):
        for menu in self:
            if menu.fecha_inicio and menu.dias_disponibles:
                menu.fecha_fin = menu.fecha_inicio + timedelta(days=menu.dias_disponibles)
            else:
                menu.fecha_fin = False
    
    @api.depends('fecha_fin')
    def _compute_proximo_vencimiento(self):
        for menu in self:
            if menu.fecha_fin:
                hoy = fields.Date.today()
                dias_restantes = (menu.fecha_fin - hoy).days
                menu.proximo_vencimiento = 0 <= dias_restantes < 3
            else:
                menu.proximo_vencimiento = False
    #Constrains ***********************************************************
    #**********************************************************************
    @api.constrains('fecha_inicio','fecha_fin')
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
class ingredients_victor(models.Model):
    _name = 'rest_victor.ingredients_victor'
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

#Modelo Categoria************************************************************
#**************************************************************************
class categoria_victor(models.Model):
    _name = 'rest_victor.categoria_victor'
    _description = 'Modelo de Categorías para Gestión de Restaurante'

    name = fields.Char(
        string = " Nombre de la Categoría",
        required = True,
        help = "Nombre de la categoría"
    )

    descripcion = fields.Text(
        string = "Descripción de la Categoría",
        required = False,
        help = "Descripción detallada de la categoría"
    )

    platos = fields.One2many(
        'rest_victor.platos_victor',
        'categoria_id',
        string='Platos de la Categoría',
    )

    ingredientes_comunes = fields.Many2many(
        'rest_victor.ingredients_victor',
        string='Ingredientes Comunes', 
        compute='_compute_ingredientes_comunes',
        store=True,
        help='Ingredientes comunes de todos los platos de la categoría'
    )

    #Depends *******************************************************************
    #***************************************************************************
    @api.depends('platos', 'platos.rel_ingredientes')
    def _compute_ingredientes_comunes(self):
        for categoria in self:
            # Inicializa recordset vacío de ingredientes
            ingredientes = self.env['rest_victor.ingredients_victor']
            # Itera sobre todos los platos de la categoría
            for plato in categoria.platos:
                # Acumula los ingredientes de cada plato
                ingredientes = ingredientes + plato.rel_ingredientes
            # Asigna el conjunto de ingredientes acumulados
            categoria.ingredientes_comunes = ingredientes
            

#Modelo Chef********************************************************************
#**************************************************************************
class chef_victor(models.Model):
    _name = 'rest_victor.chef_victor'
    _description = 'Modelo de Chef para Gestión de Restaurante'

    name = fields.Char(
        string = " Nombre de el Chef",
        required = True,
        help = "Nombre de el chef"
    )

    especialidad = fields.Many2one(
        'rest_victor.categoria_victor',
        string='Categoría',
        required=False,
        ondelete='cascade',
        help='Categoría del plato'
    )

    platos_asignados = fields.One2many(
        'rest_victor.platos_victor',
        'chef',
        string='Platos Asignados',
    )

# Modelo Camarero ********************************************************************
# **********************************************************************************
class camarero_victor(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    es_camarero = fields.Boolean(
        string = "Es Camarero"
    )

    turno = fields.Selection(
        string="Turno",
        selection=[
            ('manana', 'Mañana'),
            ('tarde', 'Tarde'),
            ('noche', 'Noche')],
        default='manana'        
    )

    seccion = fields.Char(
        string="Sección Asignada"
    )

    menus_especialidad = fields.Many2many(
        comodel_name='rest_victor.menu_victor',
        relation='rel_cam_men',
        column1='camarero_id',
        column2='menu_id',
        string='Menus de Especialidad',
    )

    @api.onchange('es_camarero')
    def _onchange_es_camarero(self):
        # Buscar la categoría "Camarero"
        categorias = self.env['res.partner.category'].search([('name', '=', 'Camarero')])

        if len(categorias) > 0:
            # Si existe, usar la primera encontrada
            category = categorias[0]
        else:
            # Si no existe, crearla
            category = self.env['res.partner.category'].create({'name': 'Camarero'})

        # Asignar la categoría al contacto
        self.category_id = [(4, category.id)]
