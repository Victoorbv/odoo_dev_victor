from odoo import models, fields, api


class platos_victor(models.Model):
    _name = 'rest_victor.platos_victor'
    _description = 'Modelo de Platos para Gestión de Restaurante'

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