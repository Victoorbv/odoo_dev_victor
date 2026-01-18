"""
Migración para renombrar el modelo ingredientes_victor a ingredients_victor
"""
from odoo import api, SUPERUSER_ID
from odoo.sql_db import TestCursor
import logging

_logger = logging.getLogger(__name__)


def migrate_ingredientes_to_ingredients(cr, version):
    """
    Migración para renombrar ingredientes_victor a ingredients_victor
    """
    try:
        # Actualizar el modelo en ir_model
        cr.execute("""
            UPDATE ir_model 
            SET model = 'rest_victor.ingredients_victor'
            WHERE model = 'rest_victor.ingredientes_victor'
        """)
        
        # Actualizar las referencias en ir_model_fields
        cr.execute("""
            UPDATE ir_model_fields 
            SET relation = 'rest_victor.ingredients_victor'
            WHERE relation = 'rest_victor.ingredientes_victor'
        """)
        
        # Actualizar los permisos en ir_model_access
        cr.execute("""
            UPDATE ir_model_access 
            SET model_id = (SELECT id FROM ir_model WHERE model = 'rest_victor.ingredients_victor')
            WHERE model_id IN (SELECT id FROM ir_model WHERE model = 'rest_victor.ingredientes_victor')
        """)
        
        _logger.info("Migración completada: ingredientes_victor -> ingredients_victor")
    except Exception as e:
        _logger.error(f"Error en migración: {str(e)}")
        raise
