from odoo import models, fields, api


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
    @api.depends('categoria')
    def _get_codigo(self):
        for plato in self:
            # Si la tarea no tiene categoria asignada
            if not plato.categoria:
                plato.codigo = "PLT_" + str(plato.id)
            else:
                # Si tiene categoria, usamos su nombre
                plato.codigo = plato.categoria[:3].upper() + "_" + str(plato.id)
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

    @api.depends('platos','platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
        # Suma el precio_final de todos los platos relacionados
        # La función map() extrae los valores y sum() los agrega.
            precios = menu.platos.mapped('precio_final')
            menu.precio_total = sum(precios)
    
    
   

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